#!/usr/bin/env python
import os

def init():
  global realpath
  global loggedin
  global pubkeys
  global keypair

  realpath = os.path.dirname(os.path.realpath(__file__))
  loggedin = False
  pubkeys = {}
  keypair = None
  aeskey = None

