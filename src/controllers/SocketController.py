#!/usr/bin/env python
import socket
import struct
import cPickle

MAX_BYTE = 1024
marshall = cPickle.dumps
unmarshall = cPickle.loads

class SocketController:

  def __init__(self):
    self

  def send(self, s, *args):
    buf = marshall(args)
    value = socket.htonl(len(buf))
    size = struct.pack("L", value)
    s.send(size)
    s.send(buf)

  def receive(self, s):
    size = struct.calcsize("L")
    size = s.recv(size)
    try:
      size = socket.ntohl(struct.unpack("L", size)[0])
    except struct.error, e:
      return ''

    buf = ""

    while len(buf) < size:
        buf = s.recv(size - len(buf))

    return unmarshall(buf)[0]

  # def sendMsg(self,socket, msg):
  #   msg = unicode(msg,errors = 'ignore')
  #   socket.send(msg.encode())

  # def recMsg(self,socket):
  #   msg = socket.recv(MAX_BYTE)
  #   return msg

  def connServer(self, host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    return server

  def connClient(self, host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host,port))
    return server

  def sendFile(self, socket, filename):
    #TODO encryption
    f = open(filename, 'rb')
    l = f.read()
    self.send(socket, l)
    f.close()

  def acceptFile(self, socket, filepath):
    #TODO decryption
    with open(filepath, 'wb') as f:
      data = self.receive(socket)
      f.write(data)
    f.close()
    return filepath

