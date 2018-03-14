import socket
import sys
from clientFunctions import parseCommand
MAX_BYTE = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "localhost"

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

print(sys.argv[0])
print(sys.argv[1])
print(sys.argv[2])

#host = sys.argv[1]
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
  splitUserInput = userInput.split()
  cmd = splitUserInput[0]
  if cmd == "ls":
    filename = "NONE"
    parseCommand(cmd, filename)
  else:
    filename = splitUserInput[1]
    print(filename)
    toSend = parseCommand(cmd, filename)
    print(toSend)
    #server.send(toSend)
    print("Response from server ...")
    print(server.recv(MAX_BYTE))




