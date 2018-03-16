import os

def init():
  global realpath
  global loggedin

  realpath = os.path.dirname(os.path.realpath(__file__))
  loggedin = False
