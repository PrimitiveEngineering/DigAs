""" test_util
    * all basic-tests for util.py are implemented here
    author:     inf20086@lehre.dhbw-stuttgart.de
    date:       06.04.2023
    version:    0.0.1
    license:    MIT
"""

import unittest

from core.util import Speech2TextUtil

S2TU = Speech2TextUtil()


class TestUtil(unittest.TestCase):
    def test_user_termination_desired_true(self):
        correct_statement = True
        self.assertEqual(correct_statement, S2TU.user_termination_desired("cancel"))
        self.assertEqual(correct_statement, S2TU.user_termination_desired("terminate"))
        self.assertEqual(correct_statement, S2TU.user_termination_desired("We love to cancel Bing Chilling"))
        self.assertEqual(correct_statement, S2TU.user_termination_desired("We love to terminate Bing Chilling"))

    def test_user_termination_desired_true(self):
        correct_statement = False
        self.assertEqual(correct_statement, S2TU.user_termination_desired("Cancer"))
