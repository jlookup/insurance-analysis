

import unittest

from src import Plan

class TestPlan(unittest.TestCase):
    p = Plan(
        name='National POS 25-6350 F',
        premium=0,
        deductable=6350,
        out_of_pocket_max=6850,
        categories={}
    )

    def test_plan_init(self):
        p = Plan()
        self.assertIsNotNone(p)

    def test_plan_attrs(self):
        p = Plan(
            name='National POS 25-6350 F',
            premium=0,
            deductable=6350,
            out_of_pocket_max=6850,
            categories={}
        )
        self.assertIsNotNone(p)
        self.assertEqual(p.deductable, 6350)

    def test_add_categories(self):
        self.p.add_categories({'key':'value'})
        self.assertEqual(self.p.categories['key'], 'value')


if __name__ == '__main__':
    unittest.main()