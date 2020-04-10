import json
import sys
import ipinfo
from tqdm import tqdm

def main():
    
    
    access_token = '6736a407f8b7a6'
    handler = ipinfo.getHandler(access_token)
    
     
    countFailed = 0
    countSuccessful = 0
    
    root_1st_try = 0
    max_root_attempts = 0;
    
    usernames_failedlogin = dict()
    usernames_succlogin = dict()
    
    ip_failedlogin = dict()
    ip_firsttime = set()
    unique_ips = set()

    commands_entered = dict()
    passwords_attempted = dict()
    connections_by_country = dict()
    
    file_name = sys.argv[1];
    file = open(file_name)
    
    for line in tqdm(file.readlines()):
        
        line_object = json.loads(line)
        
        eventID = line_object.get("eventid")
        ip = line_object.get("src_ip")
        username = line_object.get("username")
        password = line_object.get("password")
        
        if (eventID == "cowrie.session.connect") & (not(ip in unique_ips)):
            
            unique_ips.add(ip)
            details = handler.getDetails(ip)
            country = details.country_name
            
            if (country in connections_by_country):
                connections_by_country[country] = connections_by_country[country] + 1
            else:
                connections_by_country[country] = 1
            continue
        
        if eventID == "cowrie.login.failed":
            countFailed+=1
            
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
            continue
            
            
        if eventID == "cowrie.login.success":
            countSuccessful+=1
            
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
                if (ip in ip_failedlogin):
                    count = ip_failedlogin[ip]
                    if count > max_root_attempts:
                        max_root_attempts = count
            continue
        
        if eventID == "cowrie.command.input":
            cmd = line_object.get("input")
            if cmd in commands_entered:
                commands_entered[cmd] = commands_entered[cmd] + 1
            else:
                commands_entered[cmd] = 1
            continue
    
    file.close()
    
    print("Failed attempts:\n\t", countFailed)
    print("Successful attempts:\n\t", countSuccessful)
    print("Most common username for failed attempts:\n\t",\
            max(usernames_failedlogin, key=lambda k: usernames_failedlogin[k]))
    print("Most common username for successful attempts:\n\t",\
            max(usernames_succlogin, key=lambda k: usernames_succlogin[k]))
    print("Top ten passwords for all attempts (descending):")
    for i in range(10):
        toPop = max(passwords_attempted, key=lambda k: passwords_attempted[k])
        print("\t",toPop)
        passwords_attempted.pop(toPop)
    print("Source IP with most unsuccessful logins:\n\t",\
            max(ip_failedlogin, key=lambda k: ip_failedlogin[k]))
    print("Unique addresses with root login on first attempt:\n\t", ip_firsttime.__len__())
    print("Max amount of failed root logins before a successful login (assuming a single IP):\n\t",max_root_attempts)
    print("Top five most performed commands post-login:")
    for i in range(5):
        toPop = max(commands_entered, key=lambda k: commands_entered[k])
        print("\t", toPop)
        commands_entered.pop(toPop)
    print("See line 4697 for attempted public key write to authorized_keys")
    
    #'''
    #This data will be included in report
    print("Country, Count")
    for key in connections_by_country:
        print(key,",",connections_by_country[key])
    #'''

if __name__ == "__main__":
    main()