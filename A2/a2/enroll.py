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

    # [Num]
    if password.isdigit():
        return True

    # dictionary given is weird, single letters are included (intentional?)
    words = set(line.strip() for line in open("words.txt"))
    for word in words:
        subIndex = password.find(word)
        if subIndex != -1:
            # [Word]
            if word == password:
                return True
            # [WordNum]
            if subIndex == 0:
                toCompare = password[word.__len__() :]
                if toCompare.isdigit():
                    return True
            # [NumWord]
            else:
                if subIndex + word.__len__() == password.__len__():
                    toCompare = password[0:subIndex]
                    if toCompare.isdigit():
                        return True

    return False


def usernameTaken(username):
    return False


def main():
    try:
        username = sys.argv[1]
        password = sys.argv[2]
    except IndexError:
        print("Usage: authenticate.py <username> <password>")
        exit(-1)

    if (usernameTaken(username)) or (passwordTooSimple(password)):
        print("rejected.")
        sys.exit(-1)

    if enrollUser(username, password):
        print("accepted.")
    else:
        print("rejected.")


if __name__ == "__main__":
    main()
