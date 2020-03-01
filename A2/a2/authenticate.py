"""
---------------------------------
Name: Dylan Stewart
UCID: 30024193
Class: CPSC526 - Winter 2020
Assignment: #2
File: authenticate.py
---------------------------------
"""

DATABASE = "resources/database.json"

import sys
from enroll import database
from argon2 import PasswordHasher

class authenticator:
    def __init__(self, database):
        self.db = database
    
    def login(self, username, password):
        ph = PasswordHasher()
        try:
            if ph.verify(self.db.retrieveHash(username), password):
                print("access granted.")
            
        except:
            print("access denied.")
            raise Exception

def main():
    db = database()
    auth = authenticator(db)
    try:
        auth.login(sys.argv[1], sys.argv[2])
    except:
        sys.exit(-1)

if __name__ == "__main__":
    main()
