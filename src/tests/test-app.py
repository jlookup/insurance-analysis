

import unittest

import pandas as pd

from src.plan import get_plans, Plan 

class TestPlan(unittest.TestCase):
    def get_plan(self):
        plans = get_plans('src/tests/test_plan.yml')
        return plans[0]





if __name__ == '__main__':
    unittest.main()