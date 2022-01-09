
import yaml
from pathlib import Path

from .plan import *

# '''Import all plans from yaml file'''
# plans = []
# # plan_yml = Path.cwd() / 'src' / 'plans' / 'plans.yml'
# plan_yml = Path.cwd() / 'plans.yml'
# with open(plan_yml) as f:
#     for data in yaml.safe_load_all(f):
#         p = Plan(**data)
#         p.categories = dict(**p.categories)
#         p.categories['premium'] =      ExpenseCategory(**p.categories['premium'])
#         p.categories['pcp'] =          ExpenseCategory(**p.categories['pcp'])
#         p.categories['specialist'] =   ExpenseCategory(**p.categories['specialist'])
#         p.categories['prescription'] = ExpenseCategory(**p.categories['prescription'])
#         p.categories['test'] =         ExpenseCategory(**p.categories['test'])
#         plans.append(p)

if __name__ == '__main__':
    plans = get_plans('plans.yml')