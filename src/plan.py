"""
Describes an insurance plan and its details.
"""
from dataclasses import dataclass
from pathlib import Path
from datetime import date, datetime

import yaml

import pandas as pd

__all__ = ['get_plans',
 'Plan',
 'ExpenseCategory',
]

def get_plans(file_name:str) -> list:
    '''Import all plans from yaml file'''
    plans = []
    plan_yml = Path.cwd() / file_name
    with open(plan_yml) as f:
        for data in yaml.safe_load_all(f):
            p = Plan(**data)
            p.categories = dict(**p.categories)
            p.categories['premium'] =      ExpenseCategory(**p.categories['premium'])
            p.categories['pcp'] =          ExpenseCategory(**p.categories['pcp'])
            p.categories['specialist'] =   ExpenseCategory(**p.categories['specialist'])
            p.categories['prescription'] = ExpenseCategory(**p.categories['prescription'])
            p.categories['test'] =         ExpenseCategory(**p.categories['test'])
            plans.append(p)
    return plans


@dataclass
class ExpenseCategory():
    name:str = None
    payment:float = None
    copay:float = None 
    coinsurance:float = None    
    deductable_applies:bool = True 

      
@dataclass
class Plan():
    name: str = ''
    # premium: float = 0
    deductable: float = 0
    out_of_pocket_max: float = 0
    categories: dict = None

    deductable_met: bool = False
    oop_met: bool = False
    deductable_rt: float = 0
    oop_rt: float = 0
    total_paid: float = 0
    self_pay_total: float = 0

    history: pd.DataFrame = None


    def __post_init__(self):
        '''
        Create the DataFrame to track and report on expenses
        '''
        columns = [
            'date',
            'event',
            'detail',
            'self_pay_cost',
            'insured_cost',
            'deductable_running_total',
            'out_of_pocket_running_total',
            'total_cost_running_total',
            'self_pay_running_total',
            'deductable_met',
            'out_of_pocket_met',
        ]

        # TODO: work out passing types to dataframe
        # dtypes = {
        #     'event': str,
        #     'detail': str,
        #     'self_pay_cost':  int,
        #     'insured_cost':  int,
        #     'deductable_running_total':  int,
        #     'out_of_pocket_running_total':  int,
        #     'total_cost_running_total':  int,
        #     'self_pay_running_total':  int,
        #     'deductable_met':   bool,
        #     'out_of_pocket_met':   bool,
        # }

        self.history = pd.DataFrame(
            columns=columns, 
            # dtype=dtypes,
            # index=pd.DatetimeIndex([],name='date'),
        )

    
    def update_history(self, category, charge_amount, date, amt_due):
        '''
        Adds a new expense to the calendar and captures the current state.
        '''
        line = {
            'date': date,
            'event': category,
            'detail': None,  # For future use
            'self_pay_cost':  charge_amount,
            'insured_cost':  amt_due,
            'deductable_running_total':  self.deductable_rt,
            'out_of_pocket_running_total':  self.oop_rt,
            'total_cost_running_total':  self.total_paid,
            'self_pay_running_total':  self.self_pay_total,
            'deductable_met': self.deductable_met,
            'out_of_pocket_met': self.oop_met,
        }
        self.history = self.history.append(line, ignore_index=True)
        return True

    def add_expense(self, category:str, charge_amount:float, date:date=None, detail:str=None):        
        '''Adds a new expense to the insured's ledger. 
        Calculates amount due by insured, updates running totals, 
        and makes an entry in the history table.'''
        c = self.categories[category]
        if category != 'premium':
            self.self_pay_total += charge_amount

        if category == 'premium':
            amt_due = c.payment
        elif self.oop_met:
            amt_due = 0
        elif c.copay: 
            amt_due = self.calculate_amt_due_copay(charge_amount, c.copay, 
                                                   c.deductable_applies)
        else: 
            amt_due = self.calculate_amt_due_coinsurance(charge_amount, c.coinsurance)

        self.total_paid += amt_due

        self.update_history(category, charge_amount, date, amt_due)

        return amt_due


    def calculate_amt_due_copay(self, charge_amount:float, 
                                copay:float, deductable_applies:bool):
        running_amt_cash = charge_amount
        running_amt_copay = 0

        if not self.deductable_met:
            if not deductable_applies:
                running_amt_cash = 0
                running_amt_copay = copay
                if running_amt_copay + self.deductable_rt >= self.deductable:
                    self.deductable_met = True
            elif running_amt_cash + self.deductable_rt >= self.deductable:
                self.deductable_met = True
                running_amt_copay = min(copay,
                                        self.deductable - (self.deductable_rt + running_amt_cash))
                running_amt_cash = self.deductable - self.deductable_rt
        elif not self.oop_met:
            running_amt_cash = 0
            running_amt_copay = copay
            if running_amt_copay + self.oop_rt >= self.out_of_pocket_max:
                self.oop_met = True 

        amt_due = running_amt_cash + running_amt_copay
        self.deductable_rt = min(self.deductable, self.deductable_rt + amt_due)
        self.oop_rt = min(self.out_of_pocket_max, self.oop_rt + amt_due)

        return amt_due


    def calculate_amt_due_coinsurance(self, charge_amount:float, 
                                      coinsurance:float):
        running_amt_cash = charge_amount
        running_amt_coinsurance = 0
        # print('mark0: ', running_amt_cash, running_amt_coinsurance)
        if running_amt_cash + self.deductable_rt >= self.deductable:
            self.deductable_met = True
            running_amt_cash = self.deductable - self.deductable_rt                
            running_amt_coinsurance = (charge_amount - running_amt_cash) * coinsurance
            # print('mark1: ', running_amt_cash, running_amt_coinsurance) 
        if running_amt_cash + running_amt_coinsurance + self.oop_rt >= self.out_of_pocket_max:
            self.oop_met = True
            running_amt_coinsurance = self.out_of_pocket_max - self.oop_rt - running_amt_cash
            # print('mark2: ', running_amt_cash, running_amt_coinsurance)
        amt_due = running_amt_cash + running_amt_coinsurance
        self.deductable_rt = min(self.deductable, self.deductable_rt + amt_due)
        self.oop_rt = min(self.out_of_pocket_max, self.oop_rt + amt_due)
        # print('mark3: ', running_amt_cash, running_amt_coinsurance, amt_due)
        return amt_due
