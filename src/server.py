import socket
import os
import sys
import vars
from serverFunctions import parseCommand
from serverFunctions import init
from serverFunctions import verify
from serverFunctions import createUser

# define constants
MAX_BYTE = 1024

# initialize global vars
vars.init()
init()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) < 2:
  print("usage: python server.py [portnumber]")
  exit()

host = ''
port = int(sys.argv[1])
if port > 49151 or port < 1024:
  print("error: portnumber must be an integer between 1024-49151")
  exit()

s.bind((host, port))
s.listen(5)

client = None
while True:
    if client is None:
        print("Still connecting")
        client, address = s.accept()
        print( "connected from", address )

        while True:
          userId = client.recv(MAX_BYTE).decode()
          doesUserExist = verify(userId)
          if(doesUserExist == "T"):
            client.send(doesUserExist.encode())
            break;
          else:
            client.send("F".encode())
            continue
    else:
        cmd = client.recv(MAX_BYTE).decode()
        response = parseCommand(cmd)
        if (response is not ""):
          byteinputToClient = response.encode()
          client.send(response)
