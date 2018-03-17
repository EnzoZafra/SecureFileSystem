# !/usr/bin/env python

import socket
import sys
import os
import select
import subprocess
from clientFunctions import parseCommand, init
from controllers.CryptoController import *
from controllers.SocketController import *

class Client:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.username = ''
    self.prompt = ''
    init()
    self.scontroller = SocketController()
    self.crypto = CryptoController()
    self.serverpub = None
    self.keypair = self.crypto.genAsymKeys()
    self.sock = self.scontroller.connClient(self.host, self.port)

  def signIn(self):
    userInput = raw_input("what would you like to do? [1]: signin [2]: register : ")
    username = raw_input("Please input a username: ")
    password = raw_input("Please input a password: ")

    hashedpass = self.crypto.calculateHash(password)
    check_id = username + " " + hashedpass
    if (userInput == "1"):
      request = "login"
      self.scontroller.send(self.sock, self.serverpub, request + "|" + check_id)
      verified = self.scontroller.receive(self.sock, self.keypair)
      if(verified == "LOGIN_SUCCESS"):
        self.username = username
        self.prompt = '[' + '@'.join((self.username, socket.gethostname().split('.')[0])) + ']> '
        return True
      else:
        print("username or password incorrect")
    elif (userInput == "2"):
      request = "register"
      self.scontroller.send(self.sock, self.serverpub, request + "|" + check_id)
      verified = self.scontroller.receive(self.sock, self.keypair)
      if verified == "REG_FAIL":
        print("Username already taken")

  def exchangeKey(self, server):
    # send my public
    exportpub = self.keypair.publickey().exportKey()
    self.scontroller.pubsend(server, exportpub)

    # accept their public
    importpub = self.scontroller.pubreceive(server)
    self.serverpub = self.crypto.importKey(importpub)

  def loop(self):
    self.exchangeKey(self.sock)

    inputs = [0, self.sock]
    while True:
      signedIn = False
      while not signedIn:
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
            self.scontroller.send(self.sock, self.serverpub, toSend)

          elif event == self.sock:
            serverResponse = self.scontroller.receive(self.sock, self.keypair)

            if (serverResponse != "ACK"):
              tmp = serverResponse.split("|")
              if (tmp[0] == "READY_SEND"):
                self.scontroller.send(self.sock, self.serverpub, "CLIENT_READY")
                filename = tmp[1]
                filepath = "tmpcache/" + filename
                self.scontroller.acceptFile(self.sock, filepath)
                serverResponse = self.scontroller.receive(self.sock, self.keypair)
                subprocess.Popen("vi " + filepath, shell=True).wait()

                #TODO: send file back and then delete from client
                self.scontroller.send(self.sock, self.serverpub, "acceptfile|" + filename)
                self.scontroller.sendFile(self.sock, self.serverpub, filepath)

              elif (tmp[0] == "READY_EDIT"):
                realpath = os.path.dirname(os.path.realpath(__file__))
                filename = tmp[1]
                cachepath = realpath + "/tmpcache/" + filename
                subprocess.Popen("vi " + cachepath, shell=True).wait()

                #TODO: send file back and then delete from client
                self.scontroller.send(self.sock, self.serverpub, "acceptfile|" + filename)
                self.scontroller.sendFile(self.sock, self.serverpub, cachepath)

              elif (tmp[0] == "LOGOUT"):
                signedIn = False

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

