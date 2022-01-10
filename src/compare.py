'''
run the app in compare mode
    load several plan options
    load a calendar of expected healthcare services
    compare costs between plans


'''
# from os import path
from pathlib import Path
from datetime import datetime

import pandas as pd

from src import get_plans, generate_calendar




def load_calendar_into_plans(plans: list, calendar: pd.DataFrame) -> bool:
    '''Loads the mock data into each plan for comparison'''
    for index, row in calendar.iloc[1:].iterrows():
        for plan in plans:
            plan.add_expense(row.event, row.self_pay_cost, 
                             row.date, row.detail)
    return True

def compare_plans(plans: list) -> pd.DataFrame:
    '''Compares total costs for each plan by quarter'''
    hist = plans[0].history
    print(hist['total_cost_running_total'].groupby([pd.PeriodIndex(hist['date'], freq='Q')])\
                                      .agg('max'))
    return pd.DataFrame()

def save_to_file(plans: list, output_dir: Path) -> bool:
    '''Save the history for the plans to an Excel file'''
    now = datetime.now().strftime('%Y-%m-%d')
    output_path = output_dir / f'compare_insurance_{now}.xlsx'
    with pd.ExcelWriter(output_path, datetime_format="YYYY-MM-DD") as writer:
        for plan in plans:
            plan.history.to_excel(writer, index=False, sheet_name=plan.name, freeze_panes=(1,1))
        # writer.save()
    return True


plans, calendar = None, None
def compare():
    plan_path = Path.cwd().parent / 'plan-comparison.yml'
    plans = get_plans(plan_path)
    calendar = generate_calendar()
    # load_calendar_into_plans(plans, calendar)
    # compare_plans(plans)
    # save_to_file(plans, output_dir) 

    return plans, calendar

if __name__ == '__main__':
    pass