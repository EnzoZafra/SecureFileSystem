import socket

s = socket.socket()
host = "localhost"
port = 1337
MAX_BYTE = 1024
s.connect((host, port))


def signIn(userName ,passWord):
    print(userName)
    print(passWord)

    feedBackfromServer = True
    #sned username to server
    #send password to server to validate
    userName = userName.encode()
    passWord = passWord.encode()
    s.send(userName)
    print(s.recv(MAX_BYTE))
    s.send(passWord)
    print(s.recv(MAX_BYTE))
    #if true then connection is accepted
    if feedBackfromServer == True:
        print("userfound")
        #server sends ack and ends the function and proceed to the
        #else prompt user to register
    else:
        print("User was not found please register")
        newUser = input("Please input a new username: ")
        newPass = input("Please input a new password: ")
        print(newUser)
        print(newPass)
        newUser = newUser.encode()
        newPass = newPass.encode()
        s.send(newUser)
        print(s.recv(MAX_BYTE))
        s.send(newPass)
        print(s.recv(MAX_BYTE))
    #after sending the new user/pass server sends ack


print("Connected to :", host)
print("please sign in: ")
userName = input("input a username: ")
passWord = input("input a password: ")
signIn(userName, passWord)

while True:
    userInput = input("what would you like to do? ")
    splitUserInput = userInput.split()
    cmd = splitUserInput[0]
    if (len(userInput) == 0):
        print("Error Code")
    if (cmd == "ls"):
        stringToSend = "ls|"
        byteUserInput = stringToSend.encode()
        s.send(byteUserInput)
        print("Response from server ...")
        print(s.recv(MAX_BYTE))
    if (cmd == "cd"):
        filename = splitUserInput[1]
        stringToSend = "cd|" + filename
        byteUserInput = stringToSend.encode()
        s.send(byteUserInput)
        print("Response from server ...")
        print(s.recv(MAX_BYTE))
    if (cmd == "mkdir"):
        filename = splitUserInput[1]
        stringToSend = "mkdir|" + filename
        byteUserInput = stringToSend.encode()
        s.send(byteUserInput)
        print("Response from server ...")
        print(s.recv(MAX_BYTE))
