

import unittest

from src import plans

class TestPlan(unittest.TestCase):
    p = plans[0]

    def test_plan_init(self):
        self.assertIsNotNone(self.p)
    def test_plan_attrs(self):
        self.assertEqual(self.p.deductable, 6350)



if __name__ == '__main__':
    unittest.main()