"""CSCA08: Fall 2025 -- Assignment 3: Social Media Data Analyst

Starter code for tests to test function get_quantile in
data_analyst.py.

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2025 Dominik Luszczynski,
Jacqueline Smith, David Liu, and Anya Tafliovich

def get_quantile(num_list: list[int], percentage: float) -> int:
Returns the quantile value from num_list at the given percentage.
    The percentage is a float between 0 and 1 inclusive.
    
    precondition: num_list is a list of integers
                  percentage is a float between 0 and 1 inclusive
                  
    >>> get_quantile([11, 12, 13, 14, 15, 16, 17], 0.0)
    11
    >>> get_quantile([11, 12, 13, 14, 15, 16, 17], 0.3)
    12
    >>> get_quantile([11, 12, 13, 14, 15, 16, 17], 1)
    17
    >>> get_quantile([], 0.6)
    -1
    >>> get_quantile([1, 2, 3, 4, 5], -0.6)
    -1
    >>> get_quantile([1, 2, 3, 4, 5], 1.2)
    -1

    if not 0 <= percentage <= 1 or not num_list:
        return -1
    num_list.sort()
    divider = len(num_list) - 1
    i = int(percentage * divider)
    return num_list[i]
        def test_unique_list_p0_#(self):
   
        expected = 
        actual = get_quantile(self.unique_list, #)
        msg = message([self.unique_list, #], expected, actual)
        self.assertEqual(actual, expected, msg)
"""

import copy
import unittest
from data_analyst import get_quantile


class TestGetQuantile(unittest.TestCase):
    """Test the function get_quantile."""

    def setUp(self):
        self.unique_list = [5, 2, 1, 3, 4]

    def test_unique_list_p0_5(self):
        """Test that we obtain the median from a unique list
        when p = 0.5.
        """
        expected = 3
        actual = get_quantile(self.unique_list, 0.5)
        msg = message([self.unique_list, 0.5], expected, actual)
        self.assertEqual(actual, expected, msg)
        
    def test_unique_list_p0_0(self):
        """
        """
        expected = 1
        actual = get_quantile(self.unique_list, 0)
        msg = message([[self.unique_list], 0], expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_unique_list_p1(self):
        """
        """
        expected = 5
        actual = get_quantile(self.unique_list, 1)
        msg = message([self.unique_list, 1], expected, actual)
        self.assertEqual(actual, expected, msg)






def message(test_case: list[list[int], float], expected: int, actual: object) -> str:
    """Return an error message saying the function call
    get_quantile(test_case) resulted in the value
    actual, when the correct value is expected.

    """

    return ("When we called get_quantile(" + str(test_case) +
            ") we expected " + str(expected) +
            ", but got " + str(actual))


if __name__ == '__main__':
    unittest.main(exit=False)
