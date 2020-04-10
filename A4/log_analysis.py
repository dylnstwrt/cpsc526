import json
import sys

def main():
        
        countFailed = 0
        countSuccessful = 0
        root_1st_try = 0
        max_root_attempts = 0;
        
        usernames_succlogin = dict();
        
        usernames_failedlogin = dict();
        ip_failedlogin = dict();
        
        passwords_attempted = dict();
        ip_firsttime = set();
        
        commands_entered = dict();
        
        file_name = sys.argv[1];
        file = open(file_name)
        for line in file.readlines():
            
            line_object = json.loads(line)
            eventID = line_object.get("eventid")
            
            if eventID == "cowrie.login.failed":
                countFailed+=1
                ip = line_object.get("src_ip")
                username = line_object.get("username")
                password = line_object.get("password")
                #print(ip, username, password)
                
                if username in usernames_failedlogin:
                    usernames_failedlogin[username] = usernames_failedlogin[username] + 1
                else:
                    usernames_failedlogin[username] = 1
                    
                if ip in ip_failedlogin:
                    ip_failedlogin[ip] = ip_failedlogin[ip] + 1
                else:
                    ip_failedlogin[ip] = 1
                
                if password in passwords_attempted:
                    passwords_attempted[password] = passwords_attempted[password] + 1
                else:
                    passwords_attempted[password] = 1
                
                
            if eventID == "cowrie.login.success":
                countSuccessful+=1
                username = line_object.get("username")
                password = line_object.get("password")
                ip = line_object.get("src_ip")
                
                if username in usernames_succlogin:
                    usernames_succlogin[username] = usernames_succlogin[username] + 1
                else:
                    usernames_succlogin[username] = 1
                
                if password in passwords_attempted:
                    passwords_attempted[password] = passwords_attempted[password] + 1
                else:
                    passwords_attempted[password] = 1
                
                if username == "root":
                    if (not(ip in ip_failedlogin)) & (not(ip in ip_firsttime)):
                        ip_firsttime.add(ip)

            if eventID == "cowrie.command.input":
                cmd = line_object.get("input")
                if cmd in commands_entered:
                    commands_entered[cmd] = commands_entered[cmd] + 1
                else:
                    commands_entered[cmd] = 1
        
        file.close()
        
        print("Failed attempts:\n\t", countFailed)
        print("Successful attempts:\n\t", countSuccessful)
        print("Most common username for failed attempts:\n\t",max(usernames_failedlogin, key=lambda k: usernames_failedlogin[k]))
        print("Top ten passwords for all attempts (descending):")
        for i in range(10):
            toPop = max(passwords_attempted, key=lambda k: passwords_attempted[k])
            print("\t",toPop)
            passwords_attempted.pop(toPop)
        print("Most common username for successful attempts:\n\t",max(usernames_succlogin, key=lambda k: usernames_succlogin[k]))
        print("Source IP with most unsuccessful logins:\n\t",max(ip_failedlogin, key=lambda k: ip_failedlogin[k]))
        print("Unique addresses with root login on first attempt:\n\t", ip_firsttime.__len__())
        print("Top five most performed commands post-login:")
        for i in range(5):
            toPop = max(commands_entered, key=lambda k: commands_entered[k])
            print("\t", toPop)
            commands_entered.pop(toPop)
        print("See line 4697 for attempted public key write to authorized_keys")

if __name__ == "__main__":
    main()