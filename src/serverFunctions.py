def parseCommand(cmd):
  splitCmd = cmd.split("|")
  cmd = cmd[0]

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

def server_ls():
  print("To be implemented")

def server_cd(directory):
  print("To be implemented")

def server_mv(destination):
  print("To be implemented")

def server_cat(filename):
  print("To be implemented")

def server_logout():
  print("To be implemented")

def server_open(filename):
  print("To be implemented")

def server_mkdir(directory):
  print("To be implemented")

