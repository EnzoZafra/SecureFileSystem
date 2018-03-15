import socket
import os
import sys
import vars
from serverFunctions import parseCommand
from serverFunctions import server_cd

# define constants
MAX_BYTE = 1024
ROOT_DIR = "rootdir"

# initialize global vars
vars.init()

# initialize directory for the file system
if(not os.path.isdir(ROOT_DIR)):
  os.makedirs(ROOT_DIR)
else:
  # os.chdir(ROOT_DIR)
  server_cd(ROOT_DIR)

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
    else:
        cmd = client.recv(MAX_BYTE).decode()
        response = parseCommand(cmd)
        if (response is not ""):
          byteinputToClient = response.encode()
          client.send(response)
