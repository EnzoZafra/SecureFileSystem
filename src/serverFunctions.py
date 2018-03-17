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
      response = server_login(splitCmd[1])
    elif cmd == "register":
      response = server_register(splitCmd[1])
  else :
    if cmd == "ls":
      response = server_ls(server.crypto, splitCmd[1])
    elif cmd == "cd":
      response = server_cd(splitCmd[1])
    elif cmd == "mv" or cmd == "move":
      param = splitCmd[1].split()
      response = server_mv(param[0], param[1])
    elif cmd == "pwd":
      response = server_pwd()
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
      print(splitCmd)
      param = splitCmd[1].split()
      response = server_chmod(param[0],param[1])
    elif cmd == "acceptfile":
      response = server_acceptfile(splitCmd[1], server.scontroller, acceptor)
  return response

def encryptpath(crypto, path):
  splitpath = path.split("/")
  encrypted = []
  for dir in splitpath:
    if dir != '..' and dir != '.':
      dir = crypto.aesencrypt(vars.aeskey, dir)
    encrypted.append(dir)

  return "/".join(encrypted)

def server_ls(crypto, path):

  if path == '':
    path = os.getcwd()
  else:
    path = encryptpath(crypto, path)

  resulting = os.path.abspath(path)
  result = checkInjection(resulting)
  if result is True:
    return "specified path does not exist"

  list = os.listdir(path)
  if len(list) == 0:
    return ' '

  decrypted = []
  for i in list:
    if i[0] == '.':
      continue
    dir = crypto.aesdecrypt(vars.aeskey, i)
    decrypted.append(dir)

  return '%s' % ' '.join(map(str, decrypted))

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
  print(getFilePath(directory))
  if result is True:
    return "specified path does not exist"

  splitdirectory = directory.split("/")
  encrypted = []
  for dir in splitdirectory:
    if dir != '..' and dir != '.':
      dir = crypto.aesencrypt(vars.aeskey, dir)
    encrypted.append(dir)

  directory = "/".join(encrypted)
  basedir,filepath = getFilePath(directory)
  doesUserHavePerm = checkUserandFilePerm(basedir,"W",vars.user)
  if doesUserHavePerm == True:
    os.makedirs(directory)
    filePerm(directory)
    return "ACK"
  else:
    return "you do not have permission"

def server_pwd():
  #TODO encryption have to split and decrypt each hash
  workingdir = os.getcwd()
  return workingdir.replace(vars.realpath, '')

def server_logout(server, acceptor):
  server.sockets.remove(acceptor)
  vars.loggedin = False
  server_cd(vars.realpath + "/" + ROOT_DIR)
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


def server_chmod(source,permission):
  #TODO
  print("To be implemented")
  print(source)
  print(permission)
  isValid = checkValidPermission(permission)
  print(isValid)
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


  server_cd(ROOT_DIR)

def server_login(userInfo):
  vars.loggedin = verify(userInfo)
  if vars.loggedin:
    os.chdir(userInfo.split()[0])
    vars.user = userInfo.split()[0]
    return "LOGIN_SUCCESS"
  else:
    return "LOGIN_FAIL"

def server_register(userInfo):
  taken = userNameTaken(userInfo.split()[0])
  if not taken:
    createUser(userInfo)
    createBaseUserPerm(userInfo.split()[0])
    return "REG_SUCCESS"
  else:
    return "REG_FAIL"

def server_acceptfile(filename, scontroller, socket):
  scontroller.serverAcceptFile(socket, vars.keypair, filename, vars.aeskey)
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


def createUser(userId):
  splitUserID = userId.split()
  passpath = vars.realpath + "/rootdir/etc/passwd"
  file = open(passpath,"a")
  file.write("\n" + userId)
  file.close()
  permission = "default"
  setUserPerm(splitUserID[0],permission)
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
  file = open(passpath,"a")
  basedir,fileDir = getFilePath(fileName)
  owner = "RW"
  group = "N"
  other = "N"
  fileperm = fileDir + " " + owner + "," + group +","+other +" " + vars.user
  file.write(fileperm + "\n")
  file.close

def getFilePath(fileName):
  path = os.getcwd()
  splitPath = path.split("/")
  lengthSplitPath = len(splitPath)
  rootpath = "/"
  rootpathFound = False
  for i in range(0,lengthSplitPath):
    if(splitPath[i] == "rootdir"):
      rootpathFound  = True
      continue
    if(rootpathFound == True):
      rootpath =  rootpath + splitPath[i] + "/"
  newpath = rootpath + fileName
  basepath = rootpath[:-1]
  return basepath,newpath

def checkUserandFilePerm(filepath,cmd,currUser):
  print(filepath)
  owner,myFilePerm = grabFilePerm(filepath)
  print(myFilePerm)
  currUserGroup = getGroup(currUser)
  ownerGroup = getGroup(owner)
  valid = False
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
  passpath = vars.realpath + "/rootdir/etc/filePerm"
  file = open(passpath,"r+")
  filePermision = ""
  owner = ""
  with open(passpath) as fp:
        mylist = fp.read().splitlines()
        for line in mylist:
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
  file = open(passpath,"a")
  owner = "RW"
  group = "N"
  other = "N"
  fileperm = "/"+User + " " + owner + "," + group +","+other +" " + User
  file.write(fileperm + "\n")
  file.close

def checkValidPermission(permission):
  print("inside checkValidPermission")
  print(permission)
  splitPerm = permission.split(",")
  valid = 0
  if(len(splitPerm) == 3):
    print("inside len(splitPerm)")
    firstPerm = splitPerm[0]
    secondPerm = splitPerm[1]
    thirdPerm = splitPerm[2]
    if firstPerm[0] == "o" or firstPerm[0] == "O":
      if firstPerm[1] in "RWN":
        valid = valid + 1
        print(valid)
    if secondPerm[0] == "g" or secondPerm[0] == "G":
      if secondPerm[1] in "RWN":
        valid = valid + 1
        print(valid)
    if thirdPerm[0] == "o" or thirdPerm[0] == "O":
      if thirdPerm[1] in "RWN":
        valid = valid + 1
        print(valid)
    if valid == 3:
      return True
  else:
    return False

#TO FIX when prompt to login make sure that the input is a 1 or 2



