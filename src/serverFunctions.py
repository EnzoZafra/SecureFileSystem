import vars
import re
import os
import shutil

ROOT_DIR = "rootdir"

def parseCommand(cmd, server, acceptor):
  splitCmd = cmd.split("|")
  cmd = splitCmd[0]
  response= ""

  if not vars.loggedin:
    if cmd == "login":
      response = server_login(splitCmd[1])
    elif cmd == "register":
      response = server_register(splitCmd[1])
  else :
    if cmd == "ls":
      response = server_ls(splitCmd[1])
    elif cmd == "cd":
      response = server_cd(splitCmd[1])
    elif cmd == "mv" or cmd == "move":
      param = splitCmd[1].split()
      response = server_mv(param[0], param[1])
    elif cmd == "pwd":
      response = server_pwd()
    elif cmd == "mkdir":
      response = server_mkdir(splitCmd[1])
    elif cmd == "cat":
      response = server_cat(splitCmd[1])
    elif cmd == "open" or cmd == "vim" or cmd == "edit":
      response = server_open(splitCmd[1], server.scontroller, acceptor)
    elif cmd == "logout":
      response = server_logout(server, acceptor)
    elif cmd == "chmod":
      #TODO add params
      response = server_chmod()
    elif cmd == "acceptfile":
      response = server_acceptfile(splitCmd[1], server.scontroller, acceptor)
  return response

def server_ls(path):
  #TODO encryption
  if path == '':
    path = os.getcwd()

  resulting = os.path.abspath(path)
  result = checkInjection(resulting)
  if result is True:
    return "specified path does not exist"

  list = os.listdir(path)

  if len(list) == 0:
    return ' '

  return '%s' % ' '.join(map(str, list))

def server_cd(directory):
  #TODO encryption
  resulting = os.path.abspath(directory)

  result = checkInjection(resulting)
  if result is True:
    return "specified path does not exist"

  os.chdir(directory)
  return "ACK"

def server_mv(source, dest):
  #TODO encryption

  if source[0] == '/':
    sourcepath = vars.realpath + "/rootdir" + source
  else:
    sourcepath = os.getcwd() + "/" + source

  if dest[0] == '/':
    destpath = vars.realpath + "/rootdir" + dest
  else:
    destpath = os.getcwd() + "/" + dest


  resulting = os.path.abspath(sourcepath)
  result = checkInjection(resulting)
  if result is True:
    return "specified source does not exist"

  resulting = os.path.abspath(destpath)
  result = checkInjection(resulting)
  if result is True:
    return "specified destination does not exist"

  shutil.move(sourcepath, destpath)
  return "ACK"

def server_cat(filename):
  #TODO encryption

  resulting = os.path.abspath(filename)
  result = checkInjection(resulting)
  if result is True:
    return "specified file does not exist"

  with open(filename, 'rb') as com:
    return com.read()

def server_mkdir(directory):
  #TODO encryption
  resulting = os.path.abspath(directory)
  result = checkInjection(resulting)
  if result is True:
    return "specified path does not exist"

  os.makedirs(directory)
  return "ACK"

def server_pwd():
  #TODO encryption
  workingdir = os.getcwd()
  return workingdir.replace(vars.realpath, '')

def server_logout(server, acceptor):
  server.sockets.remove(acceptor)
  vars.loggedin = False
  server_cd(vars.realpath + "/" + ROOT_DIR)
  return "LOGOUT"

def server_open(filename, scontroller, acceptor):
  #TODO encryption

  resulting = os.path.abspath(filename)
  result = checkInjection(resulting)
  if result is True:
    return "specified path does not exist"

  if not os.path.exists(filename):
    response = "READY_EDIT|" + filename
    scontroller.send(acceptor, response)
  else:
    response = "READY_SEND"
    response = "READY_SEND|" + filename
    scontroller.send(acceptor, response)

    # wait for client to get ready to accept file
    resp = scontroller.receive(acceptor)
    if (resp == "CLIENT_READY"):
      scontroller.sendFile(acceptor, filename)
  return "ACK"

def server_chmod():
  #TODO
  print("To be implemented")
  return "ACK"

def init():
  etcdir = ROOT_DIR + "/etc"
  if(not os.path.isdir(etcdir)):
    os.makedirs(etcdir)

  if not os.path.exists(etcdir + "/passwd"):
    with open(etcdir + "/passwd", 'w'): pass

  server_cd(ROOT_DIR)

def server_login(userInfo):
  vars.loggedin = verify(userInfo)
  if vars.loggedin:
    os.chdir(userInfo.split()[0])
    return "LOGIN_SUCCESS"
  else:
    return "LOGIN_FAIL"

def server_register(userInfo):
  taken = userNameTaken(userInfo.split()[0])
  if not taken:
    createUser(userInfo)
    return "REG_SUCCESS"
  else:
    return "REG_FAIL"

def server_acceptfile(filename, scontroller, socket):
  scontroller.acceptFile(socket, filename)
  return "ACK"

def verify(userId):
  splitUserID = userId.split()
  passpath = vars.realpath + "/rootdir/etc/passwd"
  userExist  = False
  with open(passpath) as fp:
    mylist = fp.read().splitlines()
    for line in mylist:
      splitLine = line.split(" ")
      if(splitUserID[0] == splitLine[0]):
        if(splitUserID[1] == splitLine[1]):
          userExist = True
          return userExist
        else:
          return userExist
  fp.close()
  return userExist


def createUser(userId):
  splitUserID = userId.split()
  passpath = vars.realpath + "/rootdir/etc/passwd"
  file = open(passpath,"a")
  file.write("\n" + userId)
  file.close()

  os.makedirs(splitUserID[0])

def userNameTaken(userID):
  passpath = vars.realpath + "/rootdir/etc/passwd"
  userExist  = False
  with open(passpath) as fp:
    mylist = fp.read().splitlines()
    for line in mylist:
      splitLine = line.split(" ")
      if(userID == splitLine[0]):
        userExist = True
  fp.close()
  return userExist

def checkInjection(path):
  pattern = re.compile(vars.realpath + "/rootdir")
  match = pattern.match(path)
  if not match:
    return True
  return False
