"""
---------------------------------
Name: Dylan Stewart
UCID: 30024193
Class: CPSC526 - Winter 2020
Assignment: #2
File: authenticate.py
---------------------------------
"""

import sys
from enroll import database
from argon2 import PasswordHasher

class authenticator:
    def __init__(self, database):
        self.db = database
    
    def login(self, username, password):
        ph = PasswordHasher()
        if ph.verify(self.db.retrieveHash(username), password):
            print("access granted.")
        return True
        
def main():
    db = database("resources/database.json")
    auth = authenticator(db)
    try:
        username = sys.argv[1]
        password = sys.argv[2]
        auth.login(username, password)
    except:
        print("access denied.")
        exit(-1)

if __name__ == "__main__":
    main()
