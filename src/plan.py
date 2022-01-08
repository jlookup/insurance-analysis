"""
Describes an insurance plan and its details.
"""
from dataclasses import dataclass
from collections import namedtuple

import pandas as pd

@dataclass
class ExpenseCategory():
    name:str = ''
    type:str = ''
    deductable_applies:bool = False 
    deductable_amt:float = 0 
    coinsuance_pct:float = 0

@dataclass
class ExpenseCategories():
    pcp: ExpenseCategory = None
    specialist: ExpenseCategory = None
    prescription: ExpenseCategory = None
    test: ExpenseCategory = None

    def add_category(self, name:str, category:ExpenseCategory):
        setattr(self, name, category)
        

@dataclass
class Plan():
    name: str = ''
    premium: float = 0
    deductable: float = 0
    out_of_pocket_max: float = 0
    categories: ExpenseCategories = None

    deductable_rt: float = 0
    oop_rt: float = 0
    total_paid: float = 0

    def add_categories(self, categories:dict):
        self.categories.update(categories)