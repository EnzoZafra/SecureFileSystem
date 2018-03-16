import socket
import os
import sys
import vars
from serverFunctions import parseCommand
from serverFunctions import init
from serverFunctions import verify
from serverFunctions import userNameTaken
from serverFunctions import createUser
from controllers.SocketController import *
# define constants
MAX_BYTE = 1024

# initialize global vars
vars.init()
init()
s = SocketController()


if len(sys.argv) < 2:
  print("usage: python server.py [portnumber]")
  exit()

host = ''
port = int(sys.argv[1])
if port > 49151 or port < 1024:
  print("error: portnumber must be an integer between 1024-49151")
  exit()

client = None
while True:

  if client is None:
      print("Still connecting")
      client, address = s.connServer(host,port)
      print( "connected from", address )
      while True:
        request = s.recMsg(client)
        print(request)
        if(request == "signIn"):
          userId = s.recMsg(client)
          doesUserExist = verify(userId)
          if(doesUserExist == "T"):
            s.sendMsg(client,doesUserExist)
            print("in hare")
            break
          else:
            s.sendMsg(client,"F")
        if(request == "createUser"):
          userId = s.recMsg(client)
          doesUserExist = userNameTaken(userId)
          if(doesUserExist == "T"):
            s.sendMsg(client,doesUserExist)
          else:
            s.sendMsg(client,"F")
            userId = s.recMsg(client)
            createUser(userId)
            print("lol")
            break

  else:
    print("BUSY WAITING")
    cmd = s.recMsg(client)
    response = parseCommand(cmd, client)
    if (response is not ""):
      s.sendMsg(client,response)
