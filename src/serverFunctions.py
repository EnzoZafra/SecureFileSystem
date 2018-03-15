import vars
import os
import shutil

ROOT_DIR = "rootdir"

def parseCommand(cmd):
  splitCmd = cmd.split("|")
  cmd = splitCmd[0]

  if cmd == "ls":
    response = server_ls(splitCmd[1])
  elif cmd == "cd":
    response = server_cd(splitCmd[1])
  elif cmd == "mv" or cmd == "move":
    param = splitCmd[1].split()
    response = server_mv(param[0], param[1])
  elif cmd == "cat":
    response = server_cat(splitCmd[1])
  elif cmd == "logout":
    response = server_logout()
  elif cmd == "open" or cmd == "vim" or cmd == "edit":
    response = server_open(splitCmd[1])
  elif cmd == "mkdir":
    response = server_mkdir(splitCmd[1])
  elif cmd == "pwd":
    response = server_pwd()
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

  print(sourcepath)
  print(destpath)
  shutil.move(sourcepath, destpath)
  return "ACK"

def server_cat(filename):
  #TODO
  print("To be implemented")
  return "ACK"

def server_logout():
  #TODO
  print("To be implemented")
  return "ACK"

def server_open(filename):
  #TODO
  print("To be implemented")
  return "ACK"

def server_mkdir(directory):
  #TODO encryption
  os.makedirs(directory)
  return "ACK"

def server_pwd():
  #TODO encryption
  workingdir = os.getcwd()
  return workingdir.replace(vars.realpath, '')


def init():
  etcdir = ROOT_DIR + "/etc"
  if(not os.path.isdir(etcdir)):
    os.makedirs(etcdir)

  if not os.path.exists(etcdir + "/passwd"):
    with open(etcdir + "/passwd", 'w'): pass

  server_cd(ROOT_DIR)

def verify(userId):
  splitUserID = userId.split(" ")
  passpath = vars.realpath + "/rootdir/etc/passwd"
  userExist  = "F"
  with open(passpath) as fp:
    mylist = fp.read().splitlines()
    for line in mylist:
      splitLine = line.split(" ")
      if(splitUserID[0] == splitLine[0]):
        if(splitUserID[1] == splitLine[1]):
          userExist = "T"
          return userExist
        else:
          return userExist
  fp.close()
  return userExist


def createUser(userId):
  splitUserID = userId.split(" ")
  passpath = vars.realpath + "/rootdir/etc/passwd"
  file = open(passpath,"a")
  file.write("\n" + userId)
  file.close()

def userNameTaken(userID):
  splitUserID = userID.split(" ")
  passpath = vars.realpath + "/rootdir/etc/passwd"
  userExist  = "F"
  with open(passpath) as fp:
    mylist = fp.read().splitlines()
    for line in mylist:
      splitLine = line.split(" ")
      if(splitUserID[0] == splitLine[0]):
        userExist = "T"
  fp.close()
  return userExist