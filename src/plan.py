"""
Describes an insurance plan and its details.
"""
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

__all__ = ['Plan', 'ExpenseCategories', 'ExpenseCategory']

@dataclass
class ExpenseCategory():
    name:str = ''
    type:str = ''
    deductable_applies:bool = False 
    deductable:float = 0 
    coinsurance:float = 0

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

    def add_category(self, category):
        self.categories.add_category(category)