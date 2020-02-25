"""
---------------------------------
Name: Dylan Stewart
UCID: 30024193
Class: CPSC526 - Winter 2020
Assignment: #2
File: enroll.py
---------------------------------
"""

DATABASE = ""

import sys, argon2

def enrollUser(username, password):
    return True

def passwordTooSimple(password):

    if password.isdigit():
        return True

    # dictionary given is weird, single letters are included (intentional?)
    words = set(line.strip() for line in open('words.txt'))
    for word in words:
        if password.find(word) != -1:
            return True
    
    return False


def usernameTaken(username):
    return False

def main():
    username = sys.argv[1]
    password = sys.argv[2]

    if (usernameTaken(username)) or (passwordTooSimple(password)):
        print("rejected.")
        sys.exit(-1)

    enrollUser(username, password)
    


if __name__ == "__main__":
    main()