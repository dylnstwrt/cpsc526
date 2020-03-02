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

# requires that the database.json be empty.
class testSuite(unittest.TestCase):
    def setUp(self):
        self.db = database("resources/testdb.json")
        self.auth = authenticator(self.db)
    
    def tearDown(self):
        os.remove("resources/testdb.json")
    
    def test_goodUser(self):
        username = "user0"
        password = "123abcde123"
        self.db.enrollUser(username, password)
    
    def test_NumericPassword(self):
        username = "user1"
        password = "123"
        with self.assertRaises(Exception) as cm:
            self.db.enrollUser(username,password)
    
    def test_WordPassword(self):
        username = "user1"
        password = "nacho"
        with self.assertRaises(Exception) as cm:
            self.db.enrollUser(username,password)
    
    def test_wordNumPassword(self):
        username = "user1"
        password = "nacho123"
        with self.assertRaises(Exception) as cm:
            self.db.enrollUser(username,password)
    
    def test_numWordPassword(self):
        username = "user1"
        password = "123nacho"
        with self.assertRaises(Exception) as cm:
            self.db.enrollUser(username,password)
    
    def test_addSecondUser(self):
        username = "user1"
        password = "546fghij546"
        self.db.enrollUser(username, password)
        username = "user0"
        password = "123abcde123"
        self.db.enrollUser(username, password)
    
    def test_logins(self):
        username = "user1"
        password = "546fghij546"
        self.db.enrollUser(username, password)
        username = "user0"
        password = "123abcde123"
        self.db.enrollUser(username, password)
        self.auth.login("user0", "123abcde123")
        self.auth.login("user1", "546fghij546")
        
    def test_usernameTaken(self):
        username = "user0"
        password = "123abcde123"
        self.db.enrollUser(username,password)
        with self.assertRaises(Exception) as cm:
            self.db.enrollUser(username,"123abcde1234")
    
    def test_BadArgs(self):
        with self.assertRaises(Exception) as cm:
            self.db.enrollUser("","")
    
if __name__ == "__main__":
    unittest.main()