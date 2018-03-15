import socket
import sys
import os
from clientFunctions import parseCommand
from clientFunctions import init
from clientFunctions import acceptFile
from controllers.CryptoController import *

MAX_BYTE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# nonblocking I/O
# server.setblocking(0)
cryptography = CryptoController()

init()

def signIn():
  userExist = False
  while True:
    userInput = raw_input("what would you like to do? [1]: signin [2]: register  : ")
    if(userInput == "1"):
      request = "signIn"
      server.send(request.encode())
      userName = raw_input("Please input a username: ")
      passWord = raw_input("Please input a password: ")
      passHash = cryptography.calculateHash(passWord)
      print(passHash)
      check_id = userName + " " + passWord
      server.send(check_id.encode())
      userExist = server.recv(MAX_BYTE).decode()
      if(userExist == "T"):
        return True
      else:
        print("Username or Password Incorrect")
    elif(userInput == "2"):
      request = "createUser"
      server.send(request.encode())
      userName = raw_input("Please input a new Username: ")
      passWord = raw_input("Please input a new Password: ")
      passHash = cryptography.calculateHash(passWord)
      print(passHash)
      check_id = userName + " " + passHash
      server.send(check_id.encode())
      userExist = server.recv(MAX_BYTE).decode('utf-8')
      if(userExist == "T"):
        print("Username already taken")
      else:
        print("Creating new user")
        server.send(check_id.encode())
        return True

if len(sys.argv) < 3:
  print("usage: python client.py [host] [portnumber]")
  exit()

host = sys.argv[1]
port = int(sys.argv[2])

if port > 49151 or port < 1024:
  print("error: portnumber must be an integer between 1024-49151")
  exit()

server.connect((host, port))

#TODO: no signin yet
signIn()

while True:
  userInput = raw_input("> ")
  toSend = parseCommand(userInput)
  server.send(toSend)

  serverResponse = server.recv(MAX_BYTE).decode()

  if (serverResponse != "ACK"):
    if (serverResponse == "READY_SEND"):
      acknowledge = "CLIENT_READY".encode()
      server.send(acknowledge)
      filepath = acceptFile(server)
      serverResponse = server.recv(MAX_BYTE).decode()
      os.system('vi ' + filepath)
    elif (serverResponse == "READY_EDIT"):
      serverResponse = server.recv(MAX_BYTE).decode()
      os.system('vi tmpcache/tmp')
    else:
      print(serverResponse)
