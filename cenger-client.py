import requests,json,time,os,getpass
from cenger_vars import *
print("Cenger Version "+cenger_version)
print("Based on MIT License")
print("By Cmd_MEMZ.")
print("Notes: Default protocal is HTTP (Port 80). We suggest HTTPS Protocal (if the server supports).")
server = "";
protocal = "HTTP";
user = ""
password = ""
connected = 0
log = 0

global f_log
f_log = ""
def ol(s):
    if(log):
        timeStr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        f_log.write("[" + timeStr + "] "+s+"\n")
while 1 :
    precommand = ""
    if cenger_advanced_command_prompt:
        if connected:
            if not(user == ""):
                precommand += "" + user + "@" + server + "(" + protocal + ") # "
            else:
                precommand += "_notLoginned@" + server + "(" + protocal + ") # "
        else:
            precommand += "" + getpass.getuser() + "@localhost # "
    
    precommand += cenger_command_prompt + " "
    raw_command = input(precommand)
    raw_command = raw_command.lower();
    command = raw_command.split(" ");
    if command[0] == "exit":
        print("Bye")
        ol("Session Ended.")
        f_log.close();
        exit(0)
    elif command[0] == "connect":
        if len(command) != 2:
            ol("Connected with wrong command")
            continue
        if connected != 0:
            print("Please Disconnect First!")
            ol("Connected before disconnection")
            continue
        checkrequest = requests.get(protocal+"://"+command[1]+"/cenger.php")
        if(checkrequest.status_code != 200):
            print("Connect Failed.")
            ol("Cannot connect to server"+command[1])
        else:
            print("Connect to "+command[1]+" successfully.")
            ol("Connected Successfully to "+command[1])
            connected = 1
            server = command[1]
    elif command[0] == "disconnect":
        if connected != 1:
            print("Please Connect First!")
            ol("Disconnected before connection.")
            continue
        server = ""
        user = ""
        password = ""
        connected = 0
        print("Disconnected.")
        ol("Disconneted Successfully.")
    elif command[0] == "protocal":
        if len(command) != 2:
            ol("Wrong command.")
            continue
        if (command[1] == "http" or command[1] == "https" or command[1] == "socks5"):
            print("Set to "+command[1].upper()+" protocal successfully.")
            ol("Set to "+command[1].upper()+" protocal successfully.")
            protocal = command[1]
        else:
            print("Protocal Error")
            ol("Protocal not allowed.")
    elif command[0] == "login":
        if len(command) != 2:
            ol("Wrong command.")
            continue
        if server == "":
            print("No Server!");
            ol("Login before connection.")
            continue
        uinfo = command[1].split(":")
        if len(uinfo) != 2:
            ol("Login information wrong.")
            continue
        datas = {"op":"login","username":uinfo[0],"password":uinfo[1]}
        check = requests.post(protocal+"://"+server+"/cenger.php",data=datas)
        if(check.text == "0"):
            print("Login Successful.")
            ol("Login successfully.")
            user = uinfo[0]
            password = uinfo[1]
        else:
            ol("Login failed.")
            print("Login Failed.")
    elif command[0] == "register":
        if len(command) != 2:
            ol("Wrong command.")
            continue
        uinfo = command[1].split(":")
        if len(uinfo) != 2:
            ol("Register information wrong.")
            continue
        datas = {"op":"register","username":uinfo[0],"password":uinfo[1]}
        check = requests.post(protocal+"://"+server+"/cenger.php",data=datas)
        if(check.text == "0"):
            print("Registration & Login Successful.")
            ol("Registration successfully.")
            user = uinfo[0]
            password = uinfo[1]
        else:
            print("Registration Failed.")
            ol("Registration Failed.")
    elif command[0] == "logout":
        user = ""
        password = ""
        print("Logout.")
        ol("Logouted.")
    elif command[0] == "send":
        if len(command) < 3:
            ol("Wrong command.")
            continue
        if server == "":
            print("No Server!");
            ol("No server.")
            continue
        if user == "":
            print("Please login first!")
            ol("Sent before login")
            continue
        texts = raw_command.split(" ",2)
        receiver = texts[1]
        text = texts[2]
        datas = {"op":"send","username":user, "password":password,"receiver":receiver,"text":text}
        send = requests.post(protocal+"://"+server+"/cenger.php",data=datas)
        if(send.text == "0"):
            print("Sending Successful.")
            ol("Sending successfully.")
        else:
            print("Sending Failed.")
            ol("Sending failed.")
    elif command[0] == "sr" or (len(command) >= 2 and command[0] == "show" and command[1] == "received"):
        if server == "":
            print("No Server!");
            ol("No server");
            continue
        if user == "":
            print("Please login first!")
            ol("Operations only user's.")
            continue
        texts = raw_command.split(" ")
        if len(texts) > 2:
            sender = texts[2]
        else:
            sender = ""
        datas = {"op":"showrec","username":user, "password":password,"sender":sender}
        send = requests.post(protocal+"://"+server+"/cenger.php",data=datas)
        if(send.text == "0"):
            print("Empty.")
            ol("Show received successfully but empty.")
        elif(send.text == "1" or send.text =="2"):
            print("Query Failed.")
            ol("Show received failed.")
        else:
            print(send.text)
            ol("Show received successfully with these informations:")
            ol(send.text)
    elif command[0] == "ss" or (len(command) >= 2 and command[0] == "show" and command[1] == "sended"):
        if server == "":
            print("No Server!");
            ol("No server.")
            continue
        if user == "":
            print("Please login first!")
            ol("Operations only user's.")
            continue
        texts = raw_command.split(" ")
        if len(texts) > 2:
            receiver = texts[2]
        else:
            receiver = ""
        datas = {"op":"showsnd","username":user, "password":password,"receiver":receiver}
        send = requests.post(protocal+"://"+server+"/cenger.php",data=datas)
        if(send.text == "0"):
            print("Empty.")
            ol("Show sended successfully but empty.")
        elif(send.text == "1" or send.text =="2"):
            print("Query Failed.")
            ol("Show sended failed.")
        else:
            print(send.text)
            ol("Show received successfully with these informations:")
            ol(send.text)
    elif command[0] == "susr" or (len(command) >= 2 and command[0] == "search" and command[1] == "user"):
        if server == "":
            print("No Server!");
            continue
        if user == "":
            print("Please login first!")
            continue
        texts = raw_command.split(" ")
        if len(texts) > 2:
            keyword = texts[2]
        else:
            keyword = ""
        datas = {"op":"searchusr","username":user, "password":password,"keyword":keyword}
        send = requests.post(protocal+"://"+server+"/cenger.php",data=datas)
        if(send.text == "0"):
            print("Empty.")
        elif(send.text == "1" or send.text =="2"):
            print("Query Failed.")
        else:
            print(send.text)
    elif command[0] == "whoami":
        if connected == 0:
            print("Localhost")
        elif connected == 1 and user == "":
            print("Connected at "+server+" by "+protocal+" protocal but not logined.")
        else:
            print("Connected at "+user+"@"+server+" by "+protocal+" protocal")
    elif command[0] == "log":
        if (len(command) > 1):
            if(command[1] == "off"):
                log = 0
                continue
            if(command[1] == "on"):
                if (len(command)) == 2:
                    f_log = open(".\cenger.log","a")
                else:
                    f_log = open(command[2],"a")
                continue
        log = 1 - log
        if(log == 0):
            continue
        
        if(len(command) == 1):
            f_log = open(".\cenger.log","a")
        else:
            f_log = open(command[1],"a")
    elif command[0] == "clear":
        os.system("cls")
    elif command[0] == "ver":
        print("Cenger Version "+cenger_version+" Build "+cenger_build)
    elif command[0] == "prompt":
        if len(command)>1 and command[1] == "advanced":
            cenger_advanced_command_prompt = True
        elif len(command)>1 and command[1] == "simple":
            cenger_advanced_command_prompt = False
        elif len(command) > 1:
            cenger_command_prompt = command[1]
        else:
            cenger_command_prompt = "Cenger>"
    elif command[0] == "":
        0
    else:
        print("Unrecognized command.")