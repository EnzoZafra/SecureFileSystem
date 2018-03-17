#!/usr/bin/env python
import os

def parseCommand(userInput):

  splitUserInput = userInput.split()
  inLength = len(splitUserInput)
  if inLength == 0:
    return
  elif inLength == 1:
    splitUserInput.append('')

  cmd = splitUserInput[0]

  toSend = ""

  if (cmd == "logout"):
    toSend = client_logout()
  elif (cmd == "pwd"):
    toSend = client_pwd()
  elif (cmd == "cd"):
    filename = splitUserInput[1]
    toSend = client_cd(filename)
  elif (cmd == "mkdir"):
    filename = splitUserInput[1]
    toSend = client_mkdir(filename)
  elif (cmd == "mv" or cmd == "move"):
    source = splitUserInput[1]
    dest = splitUserInput[2]
    toSend = client_mv(source, dest)
  elif (cmd == "cat"):
    toSend = client_cat(splitUserInput[1])
  elif (cmd == "open" or cmd == "vim" or cmd == "edit"):
    filename = splitUserInput[1]
    toSend = client_open(filename)
  elif (cmd == "ls"):
    toSend = client_ls(splitUserInput[1])
  elif (cmd == "chmod"):
    #TODO add chmod params
    params = "lol test"
    toSend = client_chmod(params)
  elif (cmd == "login"):
    toSend = client_login()
  elif (cmd == "reg"):
    toSend = client_register()
  else:
    return

  byteToSend = toSend.encode()
  return byteToSend

def client_ls(path):
  stringToSend = "ls|" + path
  return stringToSend

def client_cd(filename):
  stringToSend = "cd|" + filename
  return stringToSend

def client_mkdir(filename):
  stringToSend = "mkdir|" + filename
  return stringToSend

def client_mv(source, dest):
  stringToSend = "mv|" + source + " " + dest
  return stringToSend

def client_cat(filename):
  stringToSend = "cat|" + filename
  return stringToSend

def client_logout():
  stringToSend = "logout|"
  return stringToSend

def client_open(filename):
  stringToSend = "open|" + filename
  return stringToSend

def client_pwd():
  stringToSend = "pwd|"
  return stringToSend

def client_chmod(params):
  stringToSend = "chmod|" + params
  return stringToSend

def error_code(errorValue):
  if (errorValue == 1):
    #TODO
    print("some error")

def init():
  clientpath = "tmpcache/"
  if not os.path.isdir(clientpath):
    os.makedirs(clientpath)
