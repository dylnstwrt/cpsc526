"""
---------------------------------
Name: Dylan Stewart
UCID: 30024193
Class: CPSC526 - Winter 2020
Assignment: #2
File: testing.py
---------------------------------
"""

import unittest, sys, os
from authenticate import authenticator
from enroll import database


# run from within the 'a2' directory
class testSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = database("resources/testdb.json")
        cls.auth = authenticator(cls.db)

    @classmethod
    def tearDownClass(cls):
        os.remove("resources/testdb.json")
    
    def test_a_goodCredentials(self):
        username = "user0"
        password = "123abcde123"
        self.db.enrollUser(username, password)
    
    def test_b_badNumericalPassword(self):
        username = "user1"
        password = "123"
        with self.assertRaises(Exception) as cm:
            self.db.enrollUser(username,password)
    
    def test_c_badDictWordPassword(self):
        username = "user1"
        password = "nacho"
        with self.assertRaises(Exception) as cm:
            self.db.enrollUser(username,password)
    
    def test_c_badWordNumPassword(self):
        username = "user1"
        password = "nacho123"
        with self.assertRaises(Exception) as cm:
            self.db.enrollUser(username,password)
    
    def test_d_badNumWordPassword(self):
        username = "user1"
        password = "123nacho"
        with self.assertRaises(Exception) as cm:
            self.db.enrollUser(username,password)
    
    def test_e_addSecondUser(self):
        username = "user1"
        password = "546fghij546"
        self.db.enrollUser(username, password)
    
    def test_f_logins(self):
        self.auth.login("user0", "123abcde123")
        self.auth.login("user1", "546fghij546")
        
    def test_g_ifUsernameTaken(self):
        username = "user0"
        password = "123abcde123"
        with self.assertRaises(Exception) as cm:
            self.db.enrollUser(username,"123abcde1234")
    
    def test_h_BadArgs(self):
        with self.assertRaises(Exception) as cm:
            self.db.enrollUser("","")
    
if __name__ == "__main__":
    unittest.main()