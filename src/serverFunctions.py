import vars
import os

def parseCommand(cmd):
  splitCmd = cmd.split("|")
  cmd = splitCmd[0]

  # test
  print("The command: " + cmd)

  if cmd == "ls":
    server_ls()
  elif cmd == "cd":
    server_cd(cmd[1])
  elif cmd == "mv" or cmd == "move":
    server_mv(cmd[1])
  elif cmd == "cat":
    server_cat(cmd[1])
  elif cmd == "logout":
    server_logout()
  elif cmd == "open" or cmd == "vim" or cmd == "edit":
    server_edit(cmd[1])
  elif cmd == "mkdir":
    server_mkdir(cmd[1])
  elif cmd == "pwd":
    server_pwd()

def server_ls():
  #TODO
  list = os.listdir(vars.currentdir)
  # for testing
  print('%s' % ' '.join(map(str, list)))
  print("To be implemented")

def server_cd(directory):
  #TODO
  vars.currentdir = directory

def server_mv(destination):
  #TODO
  print("To be implemented")

def server_cat(filename):
  #TODO
  print("To be implemented")

def server_logout():
  #TODO
  print("To be implemented")

def server_open(filename):
  #TODO
  print("To be implemented")

def server_mkdir(directory):
  #TODO
  print("To be implemented")

def server_pwd():
  #TODO
  print(vars.currentdir)


