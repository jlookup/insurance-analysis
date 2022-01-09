

import unittest
from copy import deepcopy

from generate_calendar import *

class TestGenerateCalendar(unittest.TestCase):
    c = generate_calendar()
    print(c.shape)
    print(c.columns) 
    print(c.dtypes)
    print(c.head())

    def test_create_calendar(self):
        c = generate_calendar()
        self.assertIsInstance(c, pd.DataFrame)

    def test_calendar_size(self):
        self.assertEqual((121,4), self.c.shape)





if __name__ == '__main__':
    unittest.main()