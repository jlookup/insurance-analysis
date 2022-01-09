

import unittest
from copy import deepcopy

from generate_calendar import *

class TestCalendar(unittest.TestCase):
    c = create_calendar()
    print(c.shape)
    print(c.columns)    
    print(c.head())


    def test_create_calendar(self):
        c = create_calendar()
        self.assertIsInstance(c, pd.DataFrame)

    def test_calendar_size(self):
        self.assertEqual((121,10), self.c.shape)





if __name__ == '__main__':
    unittest.main()