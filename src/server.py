import socket
import sys
from serverFunctions import parseCommand

MAX_BYTE = 1024
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
        print(" Response from Client")
        cmd = client.recv(MAX_BYTE).decode()
        inputToClient = "Command Recieved was: " + cmd
        parseCommand(cmd)
        byteinputToClient = inputToClient.encode()
        client.send(byteinputToClient)

