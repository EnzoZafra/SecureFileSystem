import os

def init():
  global currentdir
  currentdir = os.path.dirname(os.path.realpath(__file__))
