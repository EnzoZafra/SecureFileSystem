import socket

s = socket.socket()
host = socket.gethostname()
port = 1337

s.connect((host, port))
print("Connected to :", host)
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
        print(s.recv(1024))
    if (cmd == "cd"):
        filename = splitUserInput[1]
        stringToSend = "cd|" + filename
        byteUserInput = stringToSend.encode()
        s.send(byteUserInput)
        print("Response from server ...")
        print(s.recv(1024))
    if (cmd == "mkdir"):
        filename = splitUserInput[1]
        stringToSend = "mkdir|" + filename
        byteUserInput = stringToSend.encode()
        s.send(byteUserInput)
        print("Response from server ...")
        print(s.recv(1024))