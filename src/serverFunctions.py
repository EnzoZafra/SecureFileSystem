#!/usr/bin/env python
import vars
import re
import os
import fileinput
import shutil

from checksumdir import dirhash

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
    elif cmd == "rm":
      resposne = server_rm(server.crypto, splitCmd[1])
    elif cmd == "mv" or cmd == "move":
      param = splitCmd[1].split()
      response = server_mv(param[0], param[1], server.crypto)
    elif cmd == "pwd":
      response = server_pwd(server.crypto)
    elif cmd == "mkdir":
      response = server_mkdir(splitCmd[1], server.crypto)
    elif cmd == "cat":
      response = server_cat(splitCmd[1], server.crypto)
    elif cmd == "open" or cmd == "vim" or cmd == "edit":
      response = server_open(splitCmd[1], server.scontroller, acceptor,server.crypto)
    elif cmd == "logout":
      response = server_logout(server, acceptor)
    elif cmd == "chmod":
      #TODO add params
      param = splitCmd[1].split()
      response = server_chmod(param[0],param[1],server.crypto)
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

def server_mv(source, dest, crypto):
  #TODO fix moving directories and filenames (rename) then update checksum
  source = crypto.encryptpath(vars.aeskey, source)
  dest = crypto.encryptpath(vars.aeskey,dest)

  basepath, filepath = getFilePath(source)
  basepath_dest, filepath_dest = getFilePath(dest)

  if os.path.exists(filepath_dest):
    return "a file with the given name already exists"

  isValidSource = checkUserandFilePerm(filepath, "W", vars.user)
  isValidDest = checkUserandFilePerm(filepath_dest, "W", vars.user)
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

def server_rm(crypto, filename):
  filename = crypto.encryptpath(vars.aeskey, filename)
  resulting = os.path.abspath(filename)
  result = checkInjection(resulting)
  if result is True:
    return "specified path does not exist"

  basedir, filepath = getFilePath(filename)
  doesUserHavePerm = checkUserandFilePerm(filepath, "W", vars.user)
  if doesUserHavePerm == True:
    if(os.path.exists(filename)):
      if os.path.isfile(filename):
        os.remove(filename)
      if os.path.isdir(filename):
        shutil.rmtree(filename)
      updateChecksum(basedir, basedir[1:])
      removefilePerm(filename)
      return "ACK"
    else:
      return "file does not exist"
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
      updateChecksum(basedir, basedir[1:])
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
  if acceptor in server.sockets:
    server.sockets.remove(acceptor)
    print(server.sockets)
  vars.loggedin = False
  os.chdir(vars.realpath + "/" + ROOT_DIR)
  vars.user = None
  return "LOGOUT"

def server_open(filename, scontroller, acceptor,crypto):
  resulting = os.path.abspath(filename)
  result = checkInjection(resulting)
  print("the filename is : "+ filename)
  if result is True or os.path.isdir(filename):
    return "specified path does not exist"

  if not os.path.exists(filename):
    filename = crypto.aesencrypt(vars.aeskey, filename)
    basedir,filepath = getFilePath(filename)
    doesUserHavePerm = checkUserandFilePerm(filepath, "W", vars.user)
    if(doesUserHavePerm == True):
      response = "READY_EDIT|" + filename
      scontroller.send(acceptor, vars.pubkeys[acceptor], response)
  
      response = "READY_SEND"
      response = "READY_SEND|" + filename
      scontroller.send(acceptor, vars.pubkeys[acceptor], response)

      # wait for client to get ready to accept file
      resp = scontroller.receive(acceptor, vars.keypair)
      if (resp == "CLIENT_READY"):
        scontroller.serverSendFile(acceptor, vars.pubkeys[acceptor], filename, vars.aeskey)
      return "ACK"
    else:
      return "you do not have permission"

def server_chmod(source,permission,crypto):
  #TODO
  source = crypto.encryptpath(vars.aeskey, source)
  newFilePerm,isValid = checkValidPermission(permission)
  if(isValid == True):
    basepath,filepath = getFilePath(source)
    owner, myFilePerm = grabFilePerm(filepath)
    replaceFilePerm(filepath,newFilePerm)
  else:
    return "Incorrect permissions were inputed"
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

  if not os.path.exists(etcdir + "/checksum"):
    with open(etcdir + "/checksum", 'w'): pass

  os.chdir(ROOT_DIR)

def server_login(userInfo, crypto):
  vars.loggedin = verify(userInfo)
  if vars.loggedin:
    encrypted = crypto.aesencrypt(vars.aeskey, userInfo.split()[0])
    os.chdir(encrypted)
    vars.user = encrypted
    if(not checkintegrity(encrypted)):
      return "INTEGRITY_FAIL"
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
  basedir = filePerm(filename)
  updateChecksum(basedir, basedir[1:])
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
  file.write(userId + "\n")
  file.close()
  permission = "default"

  cryptUser = crypto.aesencrypt(vars.aeskey, splitUserID[0])
  setUserPerm(cryptUser, permission)
  os.makedirs(cryptUser)

  cspath = vars.realpath + "/rootdir/etc/checksum"
  file = open(cspath, "a")
  file.write(cryptUser + " " + dirhash(cryptUser, 'sha256') + "\n")
  file.close()
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
  return basedir

def removefilePerm(fileName):
  passpath = vars.realpath + "/rootdir/etc/filePerm"
  copy = passpath + "copy"
  shutil.copyfile(passpath, copy)

  basedir, filepath = getFilePath(fileName)
  with open(copy) as oldfile, open(passpath, 'w') as newfile:
    mylist = oldfile.read().splitlines()
    for line in mylist:
      splitLine = line.split(" ")[0]
      if not splitLine.startswith(filepath):
        newfile.write(line)
        newfile.write("\n")
  newfile.close()
  oldfile.close()
  os.remove(copy)

def getFilePath(fileName):
  pattern = "(" + vars.realpath + "/rootdir" + ")(.*)"
  fileName = os.path.abspath(fileName)
  match = re.search(pattern, fileName)

  newpath = match.group(2)
  basepath = "/" + newpath.split('/')[1]
  return basepath, newpath

def checkUserandFilePerm(filepath, cmd, currUser):
  owner, myFilePerm = grabFilePerm(filepath)
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
  filePermision = ""
  owner = ""
  with open(passpath) as fp:
    mylist = fp.read().splitlines()
    for line in mylist:
      splitLine = line.split(" ")
      if(filepath == splitLine[0]):
        filePermision = splitLine[1]
        owner = splitLine[2]
  return owner,filePermision

def getGroup(User):
  passpath = vars.realpath + "/rootdir/etc/groups"
  currUserPerm = ""
  with open(passpath) as fp:
    mylist = fp.read().splitlines()
    for line in mylist:
      splitLine = line.split(" ")
      if(splitLine[0] == User ):
        currUserPerm = splitLine[1]
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

def checkValidPermission(permission):
  splitPerm = permission.split(",")
  valid = 0
  newFilePerm = ""
  if(len(splitPerm) == 3):
    firstPerm = splitPerm[0].split("=")
    secondPerm = splitPerm[1].split("=")
    thirdPerm = splitPerm[2].split("=")
    if firstPerm[0] == "o" or firstPerm[0] == "O":
      if firstPerm[1] in "RWN":
        valid = valid + 1
        newFilePerm = firstPerm[1] +","
    if secondPerm[0] == "g" or secondPerm[0] == "G":
      if secondPerm[1] in "RWN":
        valid = valid + 1
        newFilePerm = newFilePerm + secondPerm[1] +","
    if thirdPerm[0] == "o" or thirdPerm[0] == "O":
      if thirdPerm[1] in "RWN":
        valid = valid + 1
        newFilePerm = newFilePerm + thirdPerm[1]
    if valid == 3:
      return newFilePerm,True
  else:
    return newFilePerm,False

def replaceFilePerm(filepath,newPerm):
  passpath = vars.realpath + "/rootdir/etc/filePerm"
  owner, myFilePerm = grabFilePerm(filepath)
  oldLine = filepath+" "+myFilePerm+" "+owner
  newLine = filepath+" "+newPerm + " "+owner
  with open(passpath, 'r') as file:
    filedata = file.read()
  filedata = filedata.replace(oldLine,newLine)
  with open(passpath,'w') as file:
    file.write(filedata)
  file.close()

def updateChecksum(basedir, username):
  basedir = vars.realpath + "/rootdir" + basedir
  newchecksum = dirhash(basedir, 'sha256')

  cspath = vars.realpath + "/rootdir/etc/checksum"
  copy = cspath + "copy"
  shutil.copyfile(cspath, copy)

<<<<<<< HEAD
=======
  with open(copy) as oldfile, open(cspath, 'w') as newfile:
    mylist = oldfile.read().splitlines()
    for line in mylist:
      splitLine = line.split(" ")
      userentry = splitLine[0]
      oldchecksum = splitLine[1]
      if not userentry == username:
        newfile.write(line)
      else:
        newfile.write(username + " " + newchecksum)
      newfile.write("\n")
  newfile.close()
  oldfile.close()
  os.remove(copy)

def checkintegrity(username):
  newchecksum = dirhash('.', 'sha256')
  cspath = vars.realpath + "/rootdir/etc/checksum"
  with open(cspath) as fp:
    mylist = fp.read().splitlines()
    for line in mylist:
      splitLine = line.split(" ")
      userentry = splitLine[0]
      oldchecksum = splitLine[1]

      if(username == userentry):
        if(oldchecksum != newchecksum):
          return False
        else:
          return True
>>>>>>> b13427afced742f567d9ad9522a985c88926a15a
