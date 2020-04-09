import json
import sys

def main():
        
        countFailed = 0
        countSuccessful = 0
        
        usernames_succlogin = dict();
        
        usernames_failedlogin = dict();
        ip_failedlogin = dict();
        
        passwords_succlogin = dict();
        passwords_failedlogin = dict();
        
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
                # print(username + " : " + ip)
                
            if eventID == "cowrie.login.success":
                countSuccessful+=1
                username = line_object.get("username")
                password = line_object.get("password")
            
            if eventID == "cowrie.command.input":
                
        

if __name__ == "__main__":
    main()