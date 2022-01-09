

import unittest
from copy import deepcopy

from src import *

class TestPlan(unittest.TestCase):
    def get_plan(self):
        plans = get_plans('src/tests/test-plan.yml')
        return plans[0]

    def test_plan_init(self):
        p = self.get_plan()
        self.assertIsNotNone(p)

    def test_plan_attrs(self):
        p = self.get_plan()
        self.assertEqual(p.deductable, 6350)
        self.assertEqual(p.categories['pcp'].copay, 25)
        self.assertEqual(p.categories['test'].copay, None)

    def test_add_charge_copay(self):
        p = self.get_plan()
        amt = p.add_expense('pcp', 103)
        self.assertEqual(amt, 25)
        amt = p.add_expense('prescription', 250)
        self.assertEqual(amt, 45)

    def test_increment_deductable_rt_copay(self):
        p = self.get_plan()
        p.add_expense('pcp', 103)
        p.add_expense('prescription', 250)
        self.assertEqual(70, p.deductable_rt)

    def test_increment_oop_rt_copay(self):
        p = self.get_plan()
        p.add_expense('pcp', 103)
        p.add_expense('prescription', 250)
        self.assertEqual(70, p.oop_rt)

    def test_deductable_oop_met_copay(self):
        p = self.get_plan()
        for _ in range(1,91):
            p.add_expense('pcp', 103)
            p.add_expense('prescription', 250)
        self.assertEqual(6300, p.deductable_rt)
        self.assertEqual(6300, p.oop_rt)
        self.assertEqual(False, p.deductable_met)   
        self.assertEqual(False, p.oop_met) 

        p.add_expense('pcp', 103)
        p.add_expense('prescription', 250)
        self.assertEqual(6350, p.deductable_rt)
        self.assertEqual(6370, p.oop_rt)
        self.assertEqual(True, p.deductable_met)   
        self.assertEqual(False, p.oop_met) 

        for _ in range(92,99):
            p.add_expense('pcp', 103)
            p.add_expense('prescription', 250)
        self.assertEqual(6350, p.deductable_rt)
        self.assertEqual(6850, p.oop_rt)
        self.assertEqual(True, p.deductable_met)   
        self.assertEqual(True, p.oop_met) 


    def test_add_charge_coinsurance(self):
        p = self.get_plan()
        amt = p.add_expense('specialist', 150)
        self.assertEqual(amt, 150)
        amt = p.add_expense('specialist', 250)
        self.assertEqual(amt, 250)

        p.deductable_rt = 6350
        p.deductable_met = True
        amt = p.add_expense('specialist', 250)
        self.assertEqual(amt, 50)        

        p.oop_rt = 6850
        p.oop_met = True
        amt = p.add_expense('specialist', 250)
        self.assertEqual(amt, 0) 

    def test_increment_deductable_rt_coinsurance(self):
        p = self.get_plan()
        p.add_expense('specialist', 103)
        p.add_expense('specialist', 250)
        self.assertEqual(353, p.deductable_rt)

    def test_increment_oop_rt_coinsurance(self):
        p = self.get_plan()
        p.add_expense('specialist', 103)
        p.add_expense('specialist', 250)
        self.assertEqual(353, p.oop_rt)

    def test_deductable_oop_met_coinsurance(self):
        p = self.get_plan()
        for _ in range(1,22):
            p.add_expense('specialist', 50)
            p.add_expense('specialist', 250)
        self.assertEqual(6300, p.deductable_rt)
        self.assertEqual(6300, p.oop_rt)
        self.assertEqual(False, p.deductable_met)   
        self.assertEqual(False, p.oop_met) 

        amt = p.add_expense('specialist', 50)
        self.assertEqual(50, amt)
        self.assertEqual(6350, p.deductable_rt)
        self.assertEqual(6350, p.oop_rt)
        self.assertEqual(True, p.deductable_met)   
        self.assertEqual(False, p.oop_met) 

        amt = p.add_expense('specialist', 250)
        self.assertEqual(50, amt)
        self.assertEqual(6350, p.deductable_rt)
        self.assertEqual(6400, p.oop_rt)
        self.assertEqual(True, p.deductable_met)   
        self.assertEqual(False, p.oop_met) 

        amt = p.add_expense('specialist', 2500)
        self.assertEqual(450, amt)
        self.assertEqual(6350, p.deductable_rt)
        self.assertEqual(6850, p.oop_rt)
        self.assertEqual(True, p.deductable_met)   
        self.assertEqual(True, p.oop_met) 

    def test_deductable_oop_met_coinsurance_single_charge(self):
        p = self.get_plan()
        amt = p.add_expense('specialist', 10000)
        self.assertEqual(6850, amt)
        self.assertEqual(6350, p.deductable_rt)
        self.assertEqual(6850, p.oop_rt)
        self.assertEqual(True, p.deductable_met)   
        self.assertEqual(True, p.oop_met) 

    def test_deductable_oop_met_mix(self):
        p = self.get_plan()
        for _ in range(1,25):
            p.add_expense('pcp', 50)
            p.add_expense('pcp', 50)
            p.add_expense('specialist', 200)
        self.assertEqual(6000, p.deductable_rt)
        self.assertEqual(6000, p.oop_rt)
        self.assertEqual(False, p.deductable_met)   
        self.assertEqual(False, p.oop_met) 

        amt = p.add_expense('specialist', 500)
        self.assertEqual(380, amt)
        self.assertEqual(6350, p.deductable_rt)
        self.assertEqual(6380, p.oop_rt)
        self.assertEqual(True, p.deductable_met)   
        self.assertEqual(False, p.oop_met) 

        amt = p.add_expense('prescription', 500)
        self.assertEqual(45, amt)
        self.assertEqual(6350, p.deductable_rt)
        self.assertEqual(6425, p.oop_rt)
        self.assertEqual(True, p.deductable_met)   
        self.assertEqual(False, p.oop_met) 

        amt = p.add_expense('specialist', 5000)
        self.assertEqual(425, amt)
        self.assertEqual(6350, p.deductable_rt)
        self.assertEqual(6850, p.oop_rt)
        self.assertEqual(True, p.deductable_met)   
        self.assertEqual(True, p.oop_met) 

        amt = p.add_expense('specialist', 2500)
        self.assertEqual(0, amt)
        self.assertEqual(6350, p.deductable_rt)
        self.assertEqual(6850, p.oop_rt)
        self.assertEqual(True, p.deductable_met)   
        self.assertEqual(True, p.oop_met) 

        amt = p.add_expense('pcp', 103)
        self.assertEqual(0, amt)
        self.assertEqual(6350, p.deductable_rt)
        self.assertEqual(6850, p.oop_rt)
        self.assertEqual(True, p.deductable_met)   
        self.assertEqual(True, p.oop_met) 

    def test_premuim(self):
        p = self.get_plan()
        amt = p.add_expense('premium', None)
        self.assertEqual(200, amt)
        self.assertEqual(0, p.deductable_rt)
        self.assertEqual(0, p.oop_rt)
        self.assertEqual(False, p.deductable_met)   
        self.assertEqual(False, p.oop_met)        

    def test_increment_total_paid(self):
        p = self.get_plan()
        p.add_expense('pcp', 103)
        p.add_expense('prescription', 250)
        self.assertEqual(70, p.total_paid)

        p.add_expense('specialist', 230)
        self.assertEqual(300, p.total_paid)



if __name__ == '__main__':
    unittest.main()