def parseCommand(cmd,filename):

  if (cmd == "ls"):
    client_ls()
  elif (cmd == "cd"):
    client_cd(filename)
  elif (cmd == "mkdir"):
    client_mkdir(filename)
  elif (cmd == "mv" or cmd == "move"):
    client_mv(filename)
  elif (cmd == "cat"):
    client_cat()
  elif (cmd == "logout"):
    client_logout()
  elif (cmd == "open" or cmd == "vim" or cmd == "edit"):
    client_open(filename)

def client_ls():
  print("inside client_ls")
  stringToSend = "ls|"
  byteUserInput = stringToSend.encode()
  return byteUserInput


def client_cd(filename):
  print("insdie client_cd")
  print(filename)
  stringToSend = "cd|" + filename
  byteUserInput = stringToSend.encode()
  print(byteUserInput)
  return byteUserInput


def client_mkdir(filename):
  print("inside client_mkdir")
  stringToSend = "mkdir|" + filename
  byteUserInput = stringToSend.encode()
  print(byteUserInput)
  return byteUserInput

def client_mv(filename):
  print("inside client_mv")
  stringToSend = "mv|" + filename
  byteUserInput = stringToSend.encode()
  print(byteUserInput)
  return byteUserInput

def client_cat():
 print("inside client_cat")

def client_logout():
  print("inside client_logout")
  stringToSend = "logout|"
  byteUserInput = stringToSend.encode()
  return byteUserInput

def client_open(filename):
  print("inside client_open")
  stringToSend = "open|" + filename
  byteUserInput = stringToSend.encode()
  return byteUserInput

