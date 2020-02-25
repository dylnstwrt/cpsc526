"""
---------------------------------
Name: Dylan Stewart
UCID: 30024193
Class: CPSC526 - Winter 2020
Assignment: #2
File: authenticate.py
---------------------------------
"""

import argon2, sys

ph = argon2.PasswordHasher()

# TODO reimplement after performing enroll
def retrieveHash(username):
    hash = ph.hash("password1")
    return hash

def login(db, username, password):
    correctHash = retrieveHash(username)
    try:
        ph.verify(correctHash, password)
    except:
        print("access denied.")
    else:
        print("access granted.")
        sys.exit(0)

def main():
    login(0, sys.argv[1], sys.argv[2])
    sys.exit(-1)


if __name__ == "__main__":
    main()
