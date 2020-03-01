"""
---------------------------------
Name: Dylan Stewart
UCID: 30024193
Class: CPSC526 - Winter 2020
Assignment: #2
File: enroll.py
---------------------------------
"""

DATABASE = "resources/database.json"

import sys, json
from argon2 import PasswordHasher

class database:
    def __init__(self):
        try:
            self.dct = json.load(open(DATABASE))
        except FileNotFoundError:
            read = open(DATABASE, 'a')
            read.close()
            self.dct = dict()
        except json.JSONDecodeError:
            self.dct = dict()
            
    def usernameTaken(self, username):
        if username in self.dct:
            return True
        else:
            return False
            
    def enrollUser(self, username, password):
        if self.usernameTaken(username) or self.simplisticPassword(password):
            raise Exception
        ph = argon2.PasswordHasher()
        hash = ph.hash(password)
        self.dct.update({username: hash})
        with open(DATABASE, 'w') as json_file:
            json.dump(self.dct, json_file)
        return True
        
    def simplisticPassword(self, password):
        # [Num]
        if password.isdigit():
            return True
        words = set(line.strip() for line in open("resources/words.txt"))
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
    
    def retrieveHash(self, username):
        return self.dct.get(username)



def main():
    try:
        username = sys.argv[1]
        password = sys.argv[2]
    except IndexError:
        print("Usage: authenticate.py <username> <password>")
        exit(-1)
    
    db = database()
    
    try:
        if db.enrollUser(username, password):
            print("accepted.")
    except:
        print("rejected.")
        sys.exit(-1)


if __name__ == "__main__":
    main()
