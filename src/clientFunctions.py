import os

def parseCommand(userInput):

  splitUserInput = userInput.split()
  inLength = len(splitUserInput)
  if inLength == 0:
    return
  elif inLength == 1:
    splitUserInput.append('')

  cmd = splitUserInput[0]

  toSend = ""

  if (cmd == "logout"):
    toSend = client_logout()
  elif (cmd == "pwd"):
    toSend = client_pwd()
  elif (cmd == "cd"):
    filename = splitUserInput[1]
    toSend = client_cd(filename)
  elif (cmd == "mkdir"):
    filename = splitUserInput[1]
    toSend = client_mkdir(filename)
  elif (cmd == "mv" or cmd == "move"):
    source = splitUserInput[1]
    dest = splitUserInput[2]
    toSend = client_mv(source, dest)
  elif (cmd == "cat"):
    toSend = client_cat(splitUserInput[1])
  elif (cmd == "open" or cmd == "vim" or cmd == "edit"):
    filename = splitUserInput[1]
    toSend = client_open(filename)
  elif (cmd == "ls"):
    toSend = client_ls(splitUserInput[1])
  elif (cmd == "chmod"):
    #TODO add chmod params
    params = "lol test"
    toSend = client_chmod(params)
  elif (cmd == "login"):
    toSend = client_login()
  elif (cmd == "reg"):
    toSend = client_register()
  else:
    return

  byteToSend = toSend.encode()
  return byteToSend

def client_ls(path):
  # print("inside client_ls")
  stringToSend = "ls|" + path
  return stringToSend

def client_cd(filename):
  stringToSend = "cd|" + filename
  return stringToSend

def client_mkdir(filename):
  # print("inside client_mkdir")
  stringToSend = "mkdir|" + filename
  return stringToSend

def client_mv(source, dest):
  # print("inside client_mv")
  stringToSend = "mv|" + source + " " + dest
  return stringToSend

def client_cat(filename):
 # print("inside client_cat")
  stringToSend = "cat|" + filename
  return stringToSend

def client_logout():
  # print("inside client_logout")
  stringToSend = "logout|"
  return stringToSend

def client_open(filename):
  # print("inside client_open")
  stringToSend = "open|" + filename
  return stringToSend

def client_pwd():
  # print("inside client_pwd")
  stringToSend = "pwd|"
  return stringToSend

def client_chmod(params):
  stringToSend = "chmod|" + params
  return stringToSend

def error_code(errorValue):
  if (errorValue == 1):
    #TODO
    print("some error")

def init():
  clientpath = "tmpcache/"
  if not os.path.isdir(clientpath):
    os.makedirs(clientpath)

def acceptFile(socket):
  #TODO decryption
  filename = "tmpcache/tmp"
  with open(filename, 'wb') as f:
    while True:
      data = socket.recv(1024)
      if not data:
        break
      # write data to a file
      f.write(data)
  f.close()
  return filename
