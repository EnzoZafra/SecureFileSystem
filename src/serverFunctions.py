import vars
import os
import shutil

ROOT_DIR = "rootdir"

def parseCommand(cmd, client):
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
      response = server_open(splitCmd[1], client)
    elif cmd == "logout":
      response = server_logout()
    elif cmd == "chmod":
      #TODO add params
      response = server_chmod()
  return response

def server_ls(path):
  #TODO encryption
  if path == '':
    path = os.getcwd()
  list = os.listdir(path)

  if len(list) == 0:
    return ' '

  return '%s' % ' '.join(map(str, list))

def server_cd(directory):
  #TODO encryption
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

  shutil.move(sourcepath, destpath)
  return "ACK"

def server_cat(filename):
  #TODO encryption
  with open(filename, 'rb') as com:
    return com.read()

def server_mkdir(directory):
  #TODO encryption
  os.makedirs(directory)
  return "ACK"

def server_pwd():
  #TODO encryption
  workingdir = os.getcwd()
  return workingdir.replace(vars.realpath, '')

def server_logout():
  #TODO
  print("To be implemented")
  return "ACK"

def server_open(filename, client):
  if not os.path.exists(filename):
    response = "READY_EDIT"
    byteinputToClient = response.encode()
    client.send(response)
  else:
    response = "READY_SEND"
    byteinputToClient = response.encode()
    client.send(response)

    # wait for client to get ready to accept file
    resp = client.recv(1024).decode()
    if (resp == "CLIENT_READY"):
      print("recieved CLIENT_READY")
      sendFile(client, filename)
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

def sendFile(socket, filename):
  print(os.getcwd())
  print(filename)
  #TODO encryption
  f = open(filename,'rb')
  l = f.read(1024)
  while (l):
    socket.send(l)
    l = f.read(1024)
  f.close()

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

def verify(userId):
  splitUserID = userId.split()
  passpath = vars.realpath + "/rootdir/etc/passwd"
  userExist  = False
  print(splitUserID[1])
  with open(passpath) as fp:
    mylist = fp.read().splitlines()
    for line in mylist:
      splitLine = line.split(" ")
      print(line)
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
  print(userId)
  passpath = vars.realpath + "/rootdir/etc/passwd"
  file = open(passpath,"a")
  file.write("\n" + userId)
  file.close()
  userDir = ROOT_DIR +"/" + splitUserID[0]
  print("the user dir is " + userDir)
  os.makedirs(userDir)

def userNameTaken(userID):
  passpath = vars.realpath + "/rootdir/etc/passwd"
  userExist  = False
  with open(passpath) as fp:
    mylist = fp.read().splitlines()
    for line in mylist:
      splitLine = line.split(" ")
      print(line)
      if(userID == splitLine[0]):
        userExist = True
  fp.close()
  return userExist
