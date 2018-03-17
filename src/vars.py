#!/usr/bin/env python
import os

def init():
  global realpath
  global loggedin
  global users
  realpath = os.path.dirname(os.path.realpath(__file__))
  loggedin = False
  users = None
