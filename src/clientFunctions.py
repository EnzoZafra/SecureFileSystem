def parseCommand(cmd,filename):

  if (cmd == "ls"):
    client_ls()
  elif (cmd == "cd"):
    client_cd(filename)
  elif (cmd == "mkdir"):
    client_mkdir(filename)
  elif (cmd == "mv"):
    client_mkdir()
  elif (cmd == "cat"):
    client_cat()
  elif (cmd == "logout"):
    client_logout()
  elif (cmd == "open"):
    client_open()

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

def client_mv():
 print("inside client_mv")

def client_cat():
 print("inside client_cat")

def client_logout():
 print("inside client_logout")

def client_open():
 print("inside client_open")


