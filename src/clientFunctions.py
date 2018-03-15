def parseCommand(userInput):

  splitUserInput = userInput.split()
  cmd = splitUserInput[0]
  toSend = ""

  if (cmd == "ls"):
    toSend = client_ls()
  elif (cmd == "cd"):
    filename = splitUserInput[1]
    toSend = client_cd(filename)
  elif (cmd == "mkdir"):
    filename = splitUserInput[1]
    toSend = client_mkdir(filename)
  elif (cmd == "mv" or cmd == "move"):
    filename = splitUserInput[1]
    toSend = client_mv(filename)
  elif (cmd == "cat"):
    toSend = client_cat()
  elif (cmd == "logout"):
    toSend = client_logout()
  elif (cmd == "open" or cmd == "vim" or cmd == "edit"):
    filename = splitUserInput[1]
    toSend = client_open(filename)
  elif(cmd == "pwd"):
    toSend = client_pwd()

  byteToSend = toSend.encode()
  return byteToSend


def client_ls():
  print("inside client_ls")
  stringToSend = "ls|"
  return stringToSend

def client_cd(filename):
  print("insdie client_cd")
  print(filename)
  stringToSend = "cd|" + filename
  return stringToSend


def client_mkdir(filename):
  print("inside client_mkdir")
  stringToSend = "mkdir|" + filename
  return stringToSend

def client_mv(filename):
  print("inside client_mv")
  stringToSend = "mv|" + filename
  return stringToSend

def client_cat():
 print("inside client_cat")

def client_logout():
  print("inside client_logout")
  stringToSend = "logout|"
  return stringToSend

def client_open(filename):
  print("inside client_open")
  stringToSend = "open|" + filename
  return stringToSend

def client_pwd():
  print("inside client_pwd")
  stringToSend = "pwd|"
  return stringToSend


def error_code(value):
  if (value == 1):
    print("ACK not received")
