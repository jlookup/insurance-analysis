"""
Create a set of anticipated healthcare expenses for the upcoming year
In order to compare the costs of different health insurance plans.
"""

from datetime import date 
import random

import pandas as pd

def generate_calendar():
     
    start = get_start()
    premia = get_premia()
    pcp = get_pcp()
    therapist = get_therapist()
    pt = get_pt()
    neuro = get_neuro()
    tests = get_tests()
    scripts = get_scripts()
    
    calendar = pd.concat([start, premia, pcp, therapist, pt, neuro, tests, scripts]).set_index('date').sort_index()

    calendar = cal_get_extended_columns(calendar)

    return calendar


def get_start():
    return pd.DataFrame({'date': [pd.Timestamp('2021-12-31')],
                        'event': None, 'detail': None, 'self_pay_cost': 0})

def get_premia():
    return pd.DataFrame({'date': pd.date_range('2022-01-01', periods=24, freq='SM'),
                           'event': 'premium', 'detail': None, 'self_pay_cost': 0})

def get_pcp():
    random.seed(42)
    visits_pcp_unscheduled_doy = [f'2022{random.randint(1,365)}' for _ in range(1,5)]
    visits_pcp_unscheduled_ts = pd.to_datetime(visits_pcp_unscheduled_doy, format='%Y%j').to_series()
    visits_pcp_scheduled_ts = pd.date_range('2022-01-01', periods=4, freq='QS').to_series()
    visits_pcp_ts = visits_pcp_scheduled_ts.append(visits_pcp_unscheduled_ts)
    return pd.DataFrame({'date': visits_pcp_ts,
                        'event': 'pcp', 'detail': None, 'self_pay_cost': 90})

def get_therapist():
    return pd.DataFrame({'date': pd.date_range('2022-01-01', periods=52, freq='W').to_series(),
                              'event': 'specialist', 'detail': 'therapist', 'self_pay_cost': 150})

def get_pt():
    random.seed(52)
    visits_pt_doy = [f'2022{random.randint(1,365)}' for _ in range(1,16)]
    visits_pt_ts = pd.to_datetime(visits_pt_doy, format='%Y%j').to_series()
    return pd.DataFrame({'date': visits_pt_ts,
                       'event': 'specialist', 'detail': 'Physical Therapy', 'self_pay_cost': 225})

def get_neuro():
    random.seed(62)
    visits_neuro_doy = [f'2022{random.randint(1,365)}' for _ in range(1,7)]
    visits_neuro_ts = pd.to_datetime(visits_neuro_doy, format='%Y%j').to_series()
    return pd.DataFrame({'date': visits_neuro_ts,
                          'event': 'specialist', 'detail': 'neurologist', 'self_pay_cost': 250})

def get_tests():
    random.seed(72)
    tests_neuro_doy = [f'2022{random.randint(1,365)}' for _ in range(1,4)]
    tests_neuro_ts = pd.to_datetime(tests_neuro_doy, format='%Y%j').to_series()
    return pd.DataFrame({'date': tests_neuro_ts,
                          'event': 'tests', 'detail': None, 'self_pay_cost': 350})

def get_scripts():
    # scripts_ts = pd.date_range('2022-01-01', periods=12, freq='MS').to_series()
    return pd.DataFrame({'date': pd.date_range('2022-01-01', periods=12, freq='MS').to_series(),
                            'event': 'prescription', 'detail': None, 'self_pay_cost': 115})

def cal_get_extended_columns(cal):
    cal['insured_cost'] = 0
    cal['deductable_running_total'] = 0
    cal['out_of_pocket_running_total'] = 0
    cal['total_cost_running_total'] = 0
    cal['self_pay_running_total'] = 0    
    cal['deductable_met'] = False
    cal['out_of_pocket_met'] = False

    return cal





    if __name__ == '__main__':
        print(create_calendar())