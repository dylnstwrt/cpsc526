"""
---------------------------------
Name: Dylan Stewart
UCID: 30024193
Class: CPSC526 - Winter 2020
Assignment: #2
File: authenticate.py
Version: 1.0
Language: Python 3.7.6
---------------------------------
"""

import sys
from enroll import database
from argon2 import PasswordHasher


class authenticator:
    def __init__(self, database):
        """
        Constructor for authenticator class

        Set the instance's database to the database instance
        that is passed.
        """
        self.db = database

    def login(self, username, password):
        """
        Login function for authenticator class

        Retrives password hash for username in dict if it exists,
        then attempts to verify the password and the hash using
        the argon2-cffi library's verify function in PasswordHasher.

        Prints "access granted." if the password is verified against
        the hash.

        Returns:
        bool: Returns true if password is correct for the username;
        will raise an exception in all other cases.
        """
        try:
            ph = PasswordHasher()
            if ph.verify(self.db.retrieveHash(username), password):
                print("access granted.")
            return True
        except:
            print("access denied.")
            raise Exception


def main():
    """
    Runner for authenticate.py

    Checks for the correct number of command line args,
    then creates an instance of the database class to pass into
    the authenticator class constructor.

    Assume that the command line args are the username and password
    respectively, and attempts to login using those credentials.

    If any exception occurs, "access denied." is printed and program
    exits with code -1.
    """
    try:
        if sys.argv.__len__() != 3:
            print("access denied.")
            raise Exception
        db = database("resources/database.json")
        auth = authenticator(db)
        username = sys.argv[1]
        password = sys.argv[2]
        auth.login(username, password)
    except:
        exit(-1)


if __name__ == "__main__":
    main()
