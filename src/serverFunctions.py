import vars
import os

def parseCommand(cmd):
  splitCmd = cmd.split("|")
  cmd = splitCmd[0]

  # test
  print("The command: " + cmd)

  if cmd == "ls":
    response = server_ls()
  elif cmd == "cd":
    response = server_cd(cmd[1])
  elif cmd == "mv" or cmd == "move":
    response = server_mv(cmd[1])
  elif cmd == "cat":
    response = server_cat(cmd[1])
  elif cmd == "logout":
    response = server_logout()
  elif cmd == "open" or cmd == "vim" or cmd == "edit":
    response = server_edit(cmd[1])
  elif cmd == "mkdir":
    response = server_mkdir(cmd[1])
  elif cmd == "pwd":
    response = server_pwd()

  return response

def server_ls():
  #TODO
  list = os.listdir(vars.currentdir)
  # for testing
  return '%s' % ' '.join(map(str, list))

def server_cd(directory):
  #TODO
  vars.currentdir = directory
  return ""

def server_mv(destination):
  #TODO
  print("To be implemented")
  return ""

def server_cat(filename):
  #TODO
  print("To be implemented")
  return ""

def server_logout():
  #TODO
  print("To be implemented")
  return ""

def server_open(filename):
  #TODO
  print("To be implemented")
  return ""

def server_mkdir(directory):
  #TODO
  print("To be implemented")
  return ""

def server_pwd():
  #TODO
  return vars.currentdir
