import socket
import sys
import os
from clientFunctions import parseCommand
from clientFunctions import init
from clientFunctions import acceptFile
#from controllers.CryptoController import *
from controllers.SocketController import *
MAX_BYTE = 1024

# nonblocking I/O
# server.setblocking(0)
#cryptography = CryptoController()
init()
c = SocketController()

def signIn():
  userExist = False
  while True:
    userInput = raw_input("what would you like to do? [1]: signin [2]: register  : ")
    if(userInput == "1"):
      request = "signIn"
      c.sendMsg(server,request)
      userName = raw_input("Please input a username: ")
      passWord = raw_input("Please input a password: ")
    #  passHash = cryptography.calculateHash(passWord)
    #  print(passHash)
      check_id = userName + " " + passWord
      c.sendMsg(server,check_id)
      userExist = c.recMsg(server)
      if(userExist == "T"):
        return True
      else:
        print("Username or Password Incorrect")
    elif(userInput == "2"):
      request = "createUser"
      c.sendMsg(server,request)
      userName = raw_input("Please input a new Username: ")
      passWord = raw_input("Please input a new Password: ")
    #  passHash = cryptography.calculateHash(passWord)
    #  print(passHash)
      check_id = userName + " " + passWord
      c.sendMsg(server,check_id)
      userExist = c.recMsg(server)
      if(userExist == "T"):
        print("Username already taken")
      else:
        print("Creating new user")
        c.sendMsg(server,check_id)
        return True

if len(sys.argv) < 3:
  print("usage: python client.py [host] [portnumber]")
  exit()

host = sys.argv[1]
port = int(sys.argv[2])

if port > 49151 or port < 1024:
  print("error: portnumber must be an integer between 1024-49151")
  exit()

server = c.connClient(host,port)
#TODO: no signin yet
signIn()

while True:
  userInput = raw_input("> ")
  toSend = parseCommand(userInput)
  c.sendMsg(server,toSend)
  serverResponse = c.recMsg(server)

  if (serverResponse != "ACK"):
    if (serverResponse == "READY_SEND"):
      c.send(server,"CLIENT_READY")
      filepath = acceptFile(server)
      serverResponse = c.recMsg(server)
      os.system('vi ' + filepath)
    elif (serverResponse == "READY_EDIT"):
      serverResponse = c.recMsg(server)
      os.system('vi tmpcache/tmp')
    else:
      print(serverResponse)
