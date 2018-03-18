#!/usr/bin/env python
import select
import signal
import socket
import os
import sys
import vars
from serverFunctions import parseCommand, init
from controllers.SocketController import *

class Server:
  def __init__(self, host, port, pw):
    self.host = host
    self.port = port
    self.sockets = []
    self.scontroller = SocketController()
    self.crypto = CryptoController()
    self.server = self.scontroller.connServer(self.host, self.port)
    vars.init()
    vars.keypair = self.crypto.genAsymKeys()
    vars.aeskey = self.crypto.genAesKey(pw)
    init()
    # Trap keyboard interrupts
    signal.signal(signal.SIGINT, self.sighandler)

  def sighandler(self, signum, frame):
    # Close the server
    print 'Shutting down server...'

    # Close existing client sockets
    for socket in self.sockets:
        socket.close()
    self.server.close()

  def exchangeKey(self, client):
    # send my public
    exportpub = vars.keypair.publickey().exportKey()
    self.scontroller.pubsend(client, exportpub)

    # accept their public
    importpub = self.scontroller.pubreceive(client)
    vars.pubkeys[client] = self.crypto.importKey(importpub)

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
          print(self.sockets)
          self.exchangeKey(client)
        elif s == sys.stdin:
          # handle standard input
          junk = sys.stdin.readline()
          running = 0

      # event from sockets
        else:
          cmd = self.scontroller.receive(s, vars.keypair)
          response = parseCommand(cmd, self, s)
          if (response is not ""):
            self.scontroller.send(s, vars.pubkeys[s], response)

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

  pw = raw_input("Enter server password: ")
  Server(host, port, pw).serve()
