#!/usr/bin/env python
import socket
import struct
import cPickle
from CryptoController import *

marshall = cPickle.dumps
unmarshall = cPickle.loads

class SocketController:

  def __init__(self):
    self
    self.crypto = CryptoController()

  def send(self, s, pubkey, *args):
    buf = marshall(args)
    # encryptbuf = self.crypto.encrypt(pubkey, buf)
    encryptbuf = self.crypto.encrypt(pubkey, buf).encode('hex')

    value = socket.htonl(len(encryptbuf))
    size = struct.pack("L", value)

    s.send(size)
    s.send(encryptbuf)

    #TODO: remove test
    # print(encryptbuf)

  def receive(self, s, keypair):
    size = struct.calcsize("L")
    size = s.recv(size)
    try:
      size = socket.ntohl(struct.unpack("L", size)[0])
    except struct.error, e:
      return ''

    buf = ""

    while len(buf) < size:
      buf = s.recv(size - len(buf))

    buf = buf.decode('hex')

    decryptbuf = self.crypto.decrypt(keypair, buf)

    return unmarshall(decryptbuf)[0]

  def pubsend(self, s, *args):
    buf = marshall(args)
    value = socket.htonl(len(buf))
    size = struct.pack("L", value)

    s.send(size)
    s.send(buf)

  def pubreceive(self, s):
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

  def connServer(self, host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    return server

  def connClient(self, host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host,port))
    return server

  def sendFile(self, socket, pubkey, filename):
    f = open(filename, 'rb')
    buf = f.read()
    self.send(socket, pubkey, buf)
    f.close()

  def acceptFile(self, socket, keypair, filepath):
    with open(filepath, 'wb') as f:
      data = self.receive(socket, keypair)
      f.write(data)
    f.close()
    return filepath

  def serverSendFile(self, socket, pubkey, filename, aeskey):
    f = open(filename, 'rb')
    buf = f.read()
    decryptbuf = self.crypto.aesdecrypt(aeskey, buf)
    self.send(socket, pubkey, decryptbuf)
    f.close()

  def serverAcceptFile(self, socket, keypair, filepath, aeskey):
    with open(filepath, 'wb') as f:
      data = self.receive(socket, keypair)
      encryptdata = self.crypto.aesencrypt(aeskey, data)
      f.write(encryptdata)
    f.close()
    return filepath
