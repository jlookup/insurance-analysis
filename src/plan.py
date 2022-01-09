"""
Describes an insurance plan and its details.
"""
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

__all__ = ['Plan', 
        #    'ExpenseCategories', 
           'ExpenseCategory',]

@dataclass
class ExpenseCategory():
    name:str = None
    payment:float = None
    copay:float = None 
    coinsurance:float = None    
    deductable_applies:bool = True 


# @dataclass
# class ExpenseCategories():
#     pcp: ExpenseCategory = None
#     specialist: ExpenseCategory = None
#     prescription: ExpenseCategory = None
#     test: ExpenseCategory = None

        
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


    def add_expense(self, category:str, charge_amount:float):        
        c = self.categories[category]
        if self.oop_met:
            amt_due = 0
        elif c.copay: 
            amt_due = self.calculate_amt_due_copay(charge_amount, c.copay, 
                                                   c.deductable_applies)
        else: 
            amt_due = self.calculate_amt_due_coinsurance(charge_amount, c.coinsurance)

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


    # def add_expense(self, category:str, charge_amount:float):
    #     deductable_overage = self.update_deductable(charge_amount) 
    #     oop_overage = self.update_oop(charge_amount)        
    #     amt_due = self.calculate_amt_due(category, charge_amount,
    #                                      deductable_overage, oop_overage)
       

    #     return amt_due

    # def calculate_amt_due(self, category:str, charge_amount:float,
    #                       deductable_overage:float, oop_overage:float):
    #     c = self.categories[category]
    #     if c.copay:
    #         amt_due = self.calculate_amt_due_copay(charge_amount, c.copay, c.deductable_applies,
    #                                                deductable_overage, oop_overage) 
    #     else:
    #         amt_due = self.calculate_amt_due_coinsurance(charge_amount, c.coinsurance,
    #                                                      deductable_overage, oop_overage) 
    #     return amt_due

    # def calculate_amt_due_coinsurance(self, charge_amount:float, coinsurance_rate:float,
    #                                   deductable_overage:float, oop_overage:float):
    #     amt_due = 0
    #     amt_coinsurance = charge_amount * coinsurance_rate
    #     if self.oop_met:  
    #         # if yearly out-of-pocket (oop) has been met (inclusive of this charge)
    #         # then what is due is the lesser of: 
    #         #   any amount of this charge below the oop, 
    #         #   or the coinsurance
    #         amt_below_oop = charge_amount - oop_overage
    #         amt_due = min(amt_coinsurance, amt_below_oop)        
    #     elif self.deductable_met:
    #         # if yearly deducatble has been met (inclusive of this charge)
    #         # then what is due is the sum of: 
    #         #   any amount of this charge below the deductable, 
    #         #   and the remainder multiplied by the coinsurance rate
    #         amt_below_deduct = charge_amount - deductable_overage
    #         amt_above_deduct = charge_amount - amt_below_deduct
    #         amt_coinsurance = amt_above_deduct * coinsurance_rate
    #         amt_due = amt_below_deduct + amt_coinsurance 
    #     else:
    #         amt_due = charge_amount
    #     return amt_due

    # def update_deductable(self, charge_amount):
    #     overage = 0
    #     if self.deductable_met:
    #         overage = charge_amount
    #     else:
    #         if (self.deductable_rt + charge_amount) >= self.deductable:
    #             self.deductable_met = True
    #             self.deductable_rt = self.deductable
    #             overage = (self.deductable_rt + charge_amount) - self.deductable
    #         else:
    #             self.deductable_rt += charge_amount   
    #     return overage

    # def update_oop(self, charge_amount):
    #     overage = 0
    #     if self.oop_met:
    #         overage = charge_amount
    #     else:
    #         if (self.oop_rt + charge_amount) >= self.out_of_pocket_max:
    #             self.oop_met = True
    #             self.oop_rt = self.out_of_pocket_max
    #             overage = (self.oop_rt + charge_amount) - self.out_of_pocket_max
    #         else:
    #             self.oop_rt += charge_amount   
    #     return overage
