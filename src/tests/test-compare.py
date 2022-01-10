

import unittest

import pandas as pd

from src import get_plans, Plan 
from src.compare import *

class TestCompare(unittest.TestCase):
    def get_plan(self):
        plans = get_plans('src/tests/test_plan.yml')
        return plans[0]

    def test_load_plan_definitions(self):
        plans, calendar = compare()
        self.assertEqual(3, len(plans))
        self.assertIsInstance(plans[0], Plan)

    def test_get_calendar(self):
        plans, calendar = compare()
        self.assertIsInstance(calendar, pd.DataFrame)
        self.assertEqual((121,4), calendar.shape)

    def test_load_calendar_into_plans(self):
        plans, calendar = compare()
        x = load_calendar_into_plans(plans, calendar)
        self.assertTrue(x)
        self.assertTrue(plans[0].deductable_met)

    def test_save_comparison(self):
        plans, calendar = compare()
        load_calendar_into_plans(plans, calendar)
        x = save_to_file(plans, Path.cwd() / 'tests')
        self.assertTrue(x)

    def test_compare_plans(self):
        plans, calendar = compare()
        load_calendar_into_plans(plans, calendar)
        x = compare_plans(plans)
        self.assertIsInstance(x, pd.DataFrame)


if __name__ == '__main__':
    unittest.main()