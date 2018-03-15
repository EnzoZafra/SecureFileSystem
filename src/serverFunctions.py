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
    response = server_cd(splitCmd[1])
  elif cmd == "mv" or cmd == "move":
    response = server_mv(splitCmd[1])
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

def server_ls():
  #TODO
  list = os.listdir(vars.currentdir)
  print(vars.currentdir)
  # for testing
  return '%s' % ' '.join(map(str, list))

def server_cd(directory):
  #TODO
  vars.currentdir = vars.currentdir + "/" + directory
  os.chdir(vars.currentdir)
  vars.currentdir = os.getcwd()
  return "ACK"

def server_mv(destination):
  #TODO
  print("To be implemented")
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
  #TODO
  combined_dir = vars.currentdir + "/" + directory
  # print(combined_dir)
  os.makedirs(combined_dir)
  return "ACK"

def server_pwd():
  #TODO
  return vars.currentdir

