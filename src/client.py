import socket
import sys
from clientFunctions import parseCommand
from clientFunctions import error_code

ERR_ACK = 1
MAX_BYTE = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# nonblocking I/O
# server.setblocking(0)

def signIn(userName ,passWord):
  print(userName)
  print(passWord)

  feedBackfromServer = True
  #sned username to server
  #send password to server to validate
  userName = userName.encode()
  passWord = passWord.encode()
  server.send(userName)
  print(server.recv(MAX_BYTE))
  server.send(passWord)
  print(server.recv(MAX_BYTE))
  #if true then connection is accepted
  if feedBackfromServer == True:
    print("userfound")
        #server sends ack and ends the function and proceed to the
        #else prompt user to register
  else:
    print("User was not found please register")
    newUser = input("Please input a new username: ")
    newPass = input("Please input a new password: ")
    print(newUser)
    print(newPass)
    newUser = newUser.encode()
    newPass = newPass.encode()
    server.send(newUser)
    print(server.recv(MAX_BYTE))
    server.send(newPass)
    print(server.recv(MAX_BYTE))
    #after sending the new user/pass server sends ack




if len(sys.argv) < 3:
  print("usage: python client.py [host] [portnumber]")
  exit()

host = sys.argv[1]
port = int(sys.argv[2])

if port > 49151 or port < 1024:
  print("error: portnumber must be an integer between 1024-49151")
  exit()

server.connect((host, port))
userName = raw_input("Input a Username ")
passWord = raw_input("Input a Password ")
#signIn(userName,passWord)

while True:
  userInput = raw_input("what would you like to do? ")
  toSend = parseCommand(userInput)
  #   #TODO: give user input
  #   filename = "NONE"
  # else:
  #   filename = splitUserInput[1]
  server.send(toSend)
  print("Response from server ...")
  serverResponse = server.recv(MAX_BYTE).decode()
  if(serverResponse != "ACK"):
    error_code(ERR_ACK)
  else:
    print("ACK recieved")







