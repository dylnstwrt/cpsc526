"""
---------------------------------
Name: Dylan Stewart
UCID: 30024193
Class: CPSC526 - Winter 2020
Assignment: #2
File: enroll.py
Version: 1.0
Language: Python 3.7.6
---------------------------------
"""

import sys, json
from argon2 import PasswordHasher

class database:

    def __init__(self, path):
        """
        Constructor for database class

        Parameters:
        path (str): String of path pointing to .json file

        Returns:
        database: instansiation of database class
        """
        try:
            self.path = path
            self.dct = json.load(open(self.path))
        except FileNotFoundError:
            read = open(self.path, 'a')
            read.close()
            self.dct = dict()
        except json.JSONDecodeError:
            self.dct = dict()

    def enrollUser(self, username, password):
        """
        Validates username and password, then serializes username and password
        hash

        Checks if username is already taken, and if password is too simplistic,
        then will update the dict in the instance with the username as the key
        and the password hash as the data.

        The password hash is encoded by the
        argon2-cffi library, which includes a salt, along with other information
        used by the PasswordHasher Class.

        If the credentials fail either check, an exception is raised.

        Returns:
        bool: Returns true if user is enrolled. Will raise exception in any other
        case (hopefully)
        """
        if self.usernameTaken(username) or self.simplisticPassword(password):
            raise Exception
        ph = PasswordHasher()
        hash = ph.hash(password)
        self.dct.update({username: hash})
        with open(self.path, 'w') as json_file:
            json.dump(self.dct, json_file)
        return True

    def simplisticPassword(self, password):
        """
        Check if password falls under the guidelines of restricted passwords

        The method will perform string comparisions, starting with the presence
        of a strictly numerical password, or if the password is a null string.

        Then it will check to see that the password is not an exact match for
        for any words in the words.txt file of forbidden words

        Then it will check to see that it is neither a set of numbers either acting
        as either a suffix or prefix for any word in the file of forbidden words.

        Returns:
        bool: Returns false if password does not fail any checks. Returns
        true if password fails.
        """
        # [Num] or NULL
        if password.isdigit() or password == "":
            return True
        words = set(line.strip() for line in open("resources/words.txt"))
        for word in words:
            subIndex = password.casefold().find(word)
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

    def usernameTaken(self, username):
        """
        Checks if username is taken and returns corresponding bool

        Searches through the instances dict for the presence of the username
        parameter.

        Return:
        bool: Returns true if username is taken, otherwise returns false.
        """
        if username in self.dct:
            return True
        else:
            return False

    def retrieveHash(self, username):
        """
        Retrieves the password hash for the specific username parameter

        Returns:
        unicode: Returns a unicode hash encoded for the argon2-cffi library.
        Raises KeyError Exception if the username is not enrolled.
        """
        return self.dct[username]



def main():
    """
    Runner for enroll.py.

    Takes exactly two commandline inputs as username and password respectively;
    Instansiates the database class, and attempts to enroll the username
    and password into the database, which then writes back to the json file.

    If any exception occurs, "rejected." is printed and program
    exits with code -1.

    """
    try:
        if sys.argv.__len__() != 3:
            raise Exception
        username = sys.argv[1]
        password = sys.argv[2]
        db = database("resources/database.json")
        if db.enrollUser(username, password):
            print("accepted.")
    except:
        print("rejected.")
        sys.exit(-1)


if __name__ == "__main__":
    main()
