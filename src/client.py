# !/usr/bin/env python

import socket
import sys
import os
import select
from communication import send, receive
from clientFunctions import parseCommand
from clientFunctions import init
from clientFunctions import acceptFile
from controllers.CryptoController import *
from controllers.SocketController import *

MAX_BYTE = 1024

class Client:
  def __init__(self, host, port):
    self.cryptography = SocketController()
    self.host = host
    self.port = port
    self.username = ''
    init()
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((self.host, self.port))
    self.prompt = ''

  def signIn(self):
    while True:
      userInput = raw_input("what would you like to do? [1]: signin [2]: register : ")
      username = raw_input("Please input a username: ")
      password = raw_input("Please input a password: ")
      # passHash = cryptography.calculateHash(password)
      # print(passHash)
      check_id = username + " " + password
      if (userInput == "1"):
        request = "login"
        send(self.sock, request + "|" + check_id)
        verified = receive(self.sock)
        if(verified == "LOGIN_SUCCESS"):
          self.username = username
          self.prompt = '[' + '@'.join((self.username, socket.gethostname().split('.')[0])) + ']> '
          return True
        else:
          print("username or password incorrect")
      elif (userInput == "2"):
        request = "register"
        send(self.sock, request + "|" + check_id)
        verified = receive(self.sock)
        if verified == "REG_FAIL":
          print("Username already taken")

  def loop(self):
    inputs = [0, self.sock]

    signedIn = self.signIn()
    while signedIn:
      sys.stdout.write(self.prompt)
      sys.stdout.flush()

      inEvent, outEvent, exceptEvent = select.select(inputs, [], [])
      for event in inEvent:

        if event == 0:
          userInput = sys.stdin.readline().strip()
          toSend = parseCommand(userInput)
          if toSend is None:
            continue
          send(self.sock, toSend)

        elif event == self.sock:
          serverResponse = receive(self.sock)

          if (serverResponse != "ACK"):
            if (serverResponse == "READY_SEND"):
              send(self.sock, "CLIENT_READY")
              filepath = acceptFile(server)
              sererResponse = receive(self.sock)
              os.system('vi ' + filepath)
            elif (serverResponse == "READY_EDIT"):
              sererResponse = receive(self.sock)
              os.system('vi tmpcache/tmp')
            else:
              print(serverResponse)

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print("usage: python client.py [host] [portnumber]")
    exit()

  host = sys.argv[1]
  port = int(sys.argv[2])

  if port > 49151 or port < 1024:
    print("error: portnumber must be an integer between 1024-49151")
    exit()

  c = Client(host, port)
  c.loop()

