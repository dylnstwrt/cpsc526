"""
---------------------------------
Name: Dylan Stewart
UCID: 30024193
Class: CPSC526 - Winter 2020
Assignment: #2
File: tests.py
Version: 1.0
Language: Python 3.7.6
---------------------------------
"""

import unittest, sys, os
from authenticate import authenticator
from enroll import database


# run from within the 'a2' directory
class testSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Setup for testSuite

        Create example database and set authentictor to the created database
        """
        cls.db = database("resources/testdb.json")
        cls.auth = authenticator(cls.db)

    @classmethod
    def tearDownClass(cls):
        """
        Cleanup for testSuite

        Removes the residual database
        """
        os.remove("resources/testdb.json")

    def test_a_goodCredentials(self):
        """
        Tests to see that normal user is able to enroll

        Expected: exit with no errors
        """
        username = "user0"
        password = "123abcde123"
        self.db.enrollUser(username, password)

    def test_b_badNumericalPassword(self):
        """
        Tests for exception when numerical password is used

        Expected: exception is raised
        """
        username = "user1"
        password = "123"
        with self.assertRaises(Exception) as cm:
            self.db.enrollUser(username,password)

    def test_c_badDictWordPassword(self):
        """
        Tests for exception when dictionary word is used as password
        
        Expected: exception is raised
        """
        username = "user1"
        password = "nacho"
        with self.assertRaises(Exception) as cm:
            self.db.enrollUser(username,password)

    def test_c_badWordNumPassword(self):
        """
        Tests for exception when a dictionary word with numeric suffix is used.
        
        Expected: exception is raised
        """
        username = "user1"
        password = "nacho123"
        with self.assertRaises(Exception) as cm:
            self.db.enrollUser(username,password)

    def test_d_badNumWordPassword(self):
        """
        Tests for exception when a dictionary word with a numeric prefix is used.

        Expected: exception is raised.
        """
        username = "user1"
        password = "123nacho"
        with self.assertRaises(Exception) as cm:
            self.db.enrollUser(username,password)

    def test_e_addSecondUser(self):
        """
        Tests to see that a 2nd user is able to be added successfully

        Expected: no exceptions raised
        """
        username = "user1"
        password = "546fghij546"
        self.db.enrollUser(username, password)

    def test_f_logins(self):
        """
        Tests to see that both enrolled users are able to log in successfully.

        Expected: no exceptions raised
        """
        self.auth.login("user0", "123abcde123")
        self.auth.login("user1", "546fghij546")

    def test_g_ifUsernameTaken(self):
        """
        Tests to see that attempting to enroll a new user with an occupied
        username raises an exception.

        Expected: an exception is raised
        """

        with self.assertRaises(Exception) as cm:
            self.db.enrollUser("user0","123abcde1234")

    def test_h_BadArgs(self):
        """
        Tests for exception when a blank username and password are used.

        Expected: Exception is Raised
        """
        with self.assertRaises(Exception) as cm:
            self.db.enrollUser("","")
    
    def test_i_BadCreds(self):
        """
        Tests for exception with non valid credentials

        Expected: exception is raised
        """

        with self.assertRaises(Exception) as cm:
            self.auth.login("doesn't", "exist")
    
    def test_j_LargeCreds(self):
        """
        Tests to make sure that big credentials don't crash anything

        Expected: no exception or runtime issues
        """
        username = "A"*99999
        password = "b"+str(os.urandom(256))+"b"
        self.db.enrollUser(username, password)
        self.auth.login(username, password)

if __name__ == "__main__":
    unittest.main()