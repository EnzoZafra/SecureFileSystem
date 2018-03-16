import socket
import sys
import os
import select
from communication import send, receive
from clientFunctions import parseCommand
from clientFunctions import init
from clientFunctions import acceptFile
#from controllers.CryptoController import *
from controllers.SocketController import *
MAX_BYTE = 1024

# nonblocking I/O
# server.setblocking(0)
#cryptography = CryptoController()

class Client:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    init()
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((self.host, self.port))

  def signIn():
    userExist = False
    while True:
      userInput = raw_input("what would you like to do? [1]: signin [2]: register  : ")
      if(userInput == "1"):
        request = "signIn"
        sock.sendMsg(server,request)
        userName = raw_input("Please input a username: ")
        passWord = raw_input("Please input a password: ")
      #  passHash = cryptography.calculateHash(passWord)
      #  print(passHash)
        check_id = userName + " " + passWord
        sock.sendMsg(server,check_id)
        userExist = sock.recMsg(server)
        if(userExist == "T"):
          return True
        else:
          print("Username or Password Incorrect")
      elif(userInput == "2"):
        request = "createUser"
        sock.sendMsg(server,request)
        userName = raw_input("Please input a new Username: ")
        passWord = raw_input("Please input a new Password: ")
      #  passHash = cryptography.calculateHash(passWord)
      #  print(passHash)
        check_id = userName + " " + passWord
        sock.sendMsg(server,check_id)
        userExist = sock.recMsg(server)
        if(userExist == "T"):
          print("Username already taken")
        else:
          print("Creating new user")
          sock.sendMsg(server,check_id)
          return True

  def loop(self):
    inputs = [0, self.sock]
    while True:
      inEvent, outEvent, exceptEvent = select.select(inputs, [], [])
      # userInput = raw_input("> ")
      print("> ")

      for event in inEvent:
        print("Read event")
        if event == 0:
          userInput = sys.stdin.readline().strip()
          toSend = parseCommand(userInput)
          print(toSend)
          send(self.sock, toSend)
        elif event == self.sock:
          serverResponse = receive(self.sock)

          print("waiting for response from server")

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

