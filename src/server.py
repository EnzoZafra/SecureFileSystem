import select
import signal
import socket
import os
import sys
import vars
from communication import send, receive

from serverFunctions import parseCommand
from serverFunctions import init
from serverFunctions import verify
from serverFunctions import userNameTaken
from serverFunctions import createUser
from controllers.SocketController import *
# define constants
MAX_BYTE = 1024

class Server:
  def __init__(self, host, port):
    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.host = host
    self.port = port
    self.sockets = []
    self.server.bind((host, port))
    self.server.listen(5)
    vars.init()
    init()
    # Trap keyboard interrupts
    signal.signal(signal.SIGINT, self.sighandler)

  def sighandler(self, signum, frame):
    # Close the server
    print 'Shutting down server...'
    #TODO
    # # Close existing client sockets
    for socket in self.sockets:
        socket.close()
    self.server.close()

  def serve(self):
    inputs = [self.server, sys.stdin]

    running = 1
    while running:
      try:
        inEvent, outEvent, exceptEvent = select.select(inputs, self.sockets, [])
      except select.error, e:
        break
      except socket.error, e:
        break

      for s in inEvent:
        if s == self.server:
          client, address = self.server.accept()
          print("connected from: ", address)
          inputs.append(client)
          self.sockets.append(client)
          # while True:
          #   request = s.recMsg(client)
          #   print(request)
          #   if(request == "signIn"):
          #     userId = s.recMsg(client)
          #     doesUserExist = verify(userId)
          #     if(doesUserExist == "T"):
          #       s.sendMsg(client,doesUserExist)
          #       print("in hare")
          #       break
          #     else:
          #       s.sendMsg(client,"F")
          #   if(request == "createUser"):
          #     userId = s.recMsg(client)
          #     doesUserExist = userNameTaken(userId)
          #     if(doesUserExist == "T"):
          #       s.sendMsg(client,doesUserExist)
          #     else:
          #       s.sendMsg(client,"F")
          #       userId = s.recMsg(client)
          #       createUser(userId)
          #       print("lol")
          #       break
        elif s == sys.stdin:
          # handle standard input
          junk = sys.stdin.readline()
          running = 0

      # event from sockets
        else:
          print("READ EVENT")
          cmd = receive(s)
          response = parseCommand(cmd, s)
          if (response is not ""):
            send(s, response)

    self.server.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
      print("usage: python server.py [portnumber]")
      exit()

    host = ''
    port = int(sys.argv[1])
    if port > 49151 or port < 1024:
      print("error: portnumber must be an integer between 1024-49151")
      exit()

    Server(host, port).serve()
