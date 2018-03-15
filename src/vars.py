import os

def init():
  global realpath
  realpath = os.path.dirname(os.path.realpath(__file__))
