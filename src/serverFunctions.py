#!/usr/bin/env python
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
      response = server_login(splitCmd[1], server.crypto)
    elif cmd == "register":
      response = server_register(splitCmd[1], server.crypto)
  else :
    if cmd == "ls":
      response = server_ls(server.crypto, splitCmd[1])
    elif cmd == "cd":
      response = server_cd(server.crypto, splitCmd[1])
    elif cmd == "mv" or cmd == "move":
      param = splitCmd[1].split()
      response = server_mv(param[0], param[1])
    elif cmd == "pwd":
      response = server_pwd(server.crypto)
    elif cmd == "mkdir":
      response = server_mkdir(splitCmd[1], server.crypto)
    elif cmd == "cat":
      response = server_cat(splitCmd[1], server.crypto)
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

def server_ls(crypto, path):

  if path == '':
    path = os.getcwd()
  else:
    path = crypto.encryptpath(vars.aeskey, path)

  resulting = os.path.abspath(path)
  result = checkInjection(resulting)
  if result is True:
    return "specified path does not exist"

  list = os.listdir(path)
  if len(list) == 0:
    return ' '

  decrypted = []
  for i in list:
    if i[0] == '.' or i == 'etc':
      continue
    dir = crypto.aesdecrypt(vars.aeskey, i)
    decrypted.append(dir)

  return '%s' % ' '.join(map(str, decrypted))

def server_cd(crypto, directory):
  directory = crypto.encryptpath(vars.aeskey, directory)

  resulting = os.path.abspath(directory)

  result = checkInjection(resulting)
  if result is True or not os.path.isdir(directory):
    return "specified path does not exist"

  os.chdir(directory)
  return "ACK"

def server_mv(source, dest):
  #TODO encryption
  basepath,filepath = getFilePath(source)
  basepath_dest,filepath_dest = getFilePath(dest)
  isValidSource = checkUserandFilePerm(filepath,"W",vars.user)
  isValidDest = checkUserandFilePerm(filepath_dest,"W",vars.user)
  if isValidDest and isValidSource == True:
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
  else:
    return "you do not have permission"

def server_cat(filename, crypto):
  resulting = os.path.abspath(filename)
  result = checkInjection(resulting)
  filename = crypto.aesencrypt(vars.aeskey, filename)
  checkexist = os.path.isfile(filename)
  if result is True or checkexist is not True:
    return "specified file does not exist"
  else:
    basedir,filepath = getFilePath(filename)
    doesUserHavePerm = checkUserandFilePerm(filepath,"R",vars.user)
    if doesUserHavePerm == True:
      with open(filename, 'rb') as com:
        encrypted = com.read()
        return crypto.aesdecrypt(vars.aeskey, encrypted)
    else:
      return "you do not have permission"

def server_mkdir(directory, crypto):
  resulting = os.path.abspath(directory)
  result = checkInjection(resulting)
  if result is True:
    return "specified path does not exist"

  directory = crypto.encryptpath(vars.aeskey, directory)

  basedir,filepath = getFilePath(directory)
  doesUserHavePerm = checkUserandFilePerm(basedir, "W", vars.user)
  if doesUserHavePerm == True:
    if(not os.path.isdir(directory)):
      os.makedirs(directory)
      filePerm(directory)
      return "ACK"
    else:
      return "directory already exists"
  else:
    return "you do not have permission"

def server_pwd(crypto):
  workingdir = os.getcwd().replace(vars.realpath, '')
  return crypto.decryptpath(vars.aeskey, workingdir)


def server_logout(server, acceptor):
  server.sockets.remove(acceptor)
  vars.loggedin = False
  os.chdir(vars.realpath + "/" + ROOT_DIR)
  vars.user = None
  return "LOGOUT"

def server_open(filename, scontroller, acceptor):
  resulting = os.path.abspath(filename)
  result = checkInjection(resulting)
  if result is True:
    return "specified path does not exist"

  if not os.path.exists(filename):
    response = "READY_EDIT|" + filename
    scontroller.send(acceptor, vars.pubkeys[acceptor], response)
  else:
    response = "READY_SEND"
    response = "READY_SEND|" + filename
    scontroller.send(acceptor, vars.pubkeys[acceptor], response)

    # wait for client to get ready to accept file
    resp = scontroller.receive(acceptor, vars.keypair)
    if (resp == "CLIENT_READY"):
      scontroller.serverSendFile(acceptor, vars.pubkeys[acceptor], filename, vars.aeskey)
  return "ACK"


def server_chmod():
  #TODO
  print("To be implemented")
  return "ACK"

def init():
  etcdir = ROOT_DIR + "/etc"
  if(not os.path.isdir(etcdir)):
    os.makedirs(etcdir)
  if not os.path.exists(etcdir + "/groups"):
    with open(etcdir + "/groups", 'w'):pass

  if not os.path.exists(etcdir + "/passwd"):
    with open(etcdir + "/passwd", 'w'): pass

  if not os.path.exists(etcdir + "/filePerm"):
    with open(etcdir + "/filePerm", 'w'): pass


  os.chdir(ROOT_DIR)

def server_login(userInfo, crypto):
  vars.loggedin = verify(userInfo)
  if vars.loggedin:
    encrypted = crypto.aesencrypt(vars.aeskey, userInfo.split()[0])
    os.chdir(encrypted)
    vars.user = crypto.aesencrypt(vars.aeskey, userInfo.split()[0])
    return "LOGIN_SUCCESS"
  else:
    return "LOGIN_FAIL"

def server_register(userInfo, crypto):
  taken = userNameTaken(userInfo.split()[0])
  if not taken:
    createUser(userInfo, crypto)
    return "REG_SUCCESS"
  else:
    return "REG_FAIL"

def server_acceptfile(filename, scontroller, socket):
  filename = scontroller.serverAcceptFile(socket, vars.keypair, filename, vars.aeskey)
  # print(filename)
  filePerm(filename)
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


def createUser(userId, crypto):
  splitUserID = userId.split()
  passpath = vars.realpath + "/rootdir/etc/passwd"
  file = open(passpath,"a")
  file.write("\n" + userId)
  file.close()
  permission = "default"

  cryptUser = crypto.aesencrypt(vars.aeskey, splitUserID[0])
  setUserPerm(cryptUser, permission)
  os.makedirs(cryptUser)
  createBaseUserPerm(cryptUser)

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

def setUserPerm(userId, Perm):
  splitUserId = userId.split()
  passpath = vars.realpath + "/rootdir/etc/groups"
  file = open(passpath,"r+")
  UserExist = False
  with file as fp:
    mylist = fp.read().splitlines()
    for line in mylist:
      splitLine = line.split(" ")
      if(userId == splitLine[0]):
        print("user ALREADY EXIST FOUND")
        UserExist = True
        break
  if(UserExist == False):
    file = open(passpath,"a")
    file.write(userId + " " + Perm + "\n")
  file.close

def filePerm(fileName):
  passpath = vars.realpath + "/rootdir/etc/filePerm"
  basedir, filepath = getFilePath(fileName)
  file = open(passpath,"a")
  default = "RW,N,N"
  fileperm = filepath + " " + default + " " + vars.user
  file.write(fileperm + "\n")
  file.close

def getFilePath(fileName):

  test = "(" + vars.realpath + "/rootdir" + ")(.*)"
  fileName = os.getcwd() + "/" + fileName
  match = re.search(test, fileName)

  # path = os.getcwd()
  # splitPath = path.split("/")
  # lengthSplitPath = len(splitPath)
  # rootpath = "/"
  # rootpathFound = False
  # for i in range(0,lengthSplitPath):
  #   if(splitPath[i] == "rootdir"):
  #     rootpathFound  = True
  #     continue
  #   if(rootpathFound == True):
  #     rootpath =  rootpath + splitPath[i] + "/"
  newpath = match.group(2)
  basepath = "/" + newpath.split('/')[1]
  return basepath, newpath

def checkUserandFilePerm(filepath, cmd, currUser):
  owner, myFilePerm = grabFilePerm(filepath)
  currUserGroup = getGroup(currUser)
  ownerGroup = getGroup(owner)
  valid = False
  # print(myFilePerm)
  myFilePermSplit = myFilePerm.split(",")
  fileOwnerPerm = myFilePermSplit[0]
  fileGroupPerm = myFilePermSplit[1]
  fileOtherPerm = myFilePermSplit[2]
  if(currUser == owner):
    if(cmd in fileOwnerPerm):
      valid = True
  elif(fileOtherPerm == "N"):
    if(currUserGroup == ownerGroup):
      if(cmd in fileGroupPerm):
        valid = True
  else:
      if(cmd in "RW"):
        valid = True
  return valid

def grabFilePerm(filepath):
  # print("filepath:" + filepath)
  passpath = vars.realpath + "/rootdir/etc/filePerm"
  file = open(passpath,"r+")
  filePermision = ""
  owner = ""
  with open(passpath) as fp:
    mylist = fp.read().splitlines()
    for line in mylist:
      # print(line)
      splitLine = line.split(" ")
      if(filepath == splitLine[0]):
        filePermision = splitLine[1]
        owner = splitLine[2]
  file.close()
  return owner,filePermision

def getGroup(User):
  passpath = vars.realpath + "/rootdir/etc/groups"
  currUserPerm = ""
  file = open(passpath,"r+")
  with open(passpath) as fp:
    mylist = fp.read().splitlines()
    for line in mylist:
      splitLine = line.split(" ")
      if(splitLine[0] == User ):
        currUserPerm = splitLine[1]
  file.close()
  return currUserPerm

def createBaseUserPerm(User):
  passpath = vars.realpath + "/rootdir/etc/filePerm"
  file = open(passpath, "a")
  owner = "RW"
  group = "N"
  other = "N"
  fileperm = "/"+ User + " " + owner + "," + group +","+other +" " + User
  file.write(fileperm + "\n")
  file.close

#TO FIX when prompt to login make sure that the input is a 1 or 2



