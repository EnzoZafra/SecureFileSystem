import socket
MAX_BYTE = 1024

class SocketController:

  def __init__(self):
    self

  def sendMsg(self,socket, msg):
		msg = unicode(msg,errors = 'ignore')
		socket.send(msg.encode())
		#TODO
		print("TODO")

  def recMsg(self,socket):
    msg = socket.recv(MAX_BYTE)
    return msg

  def connServer(self,host, port):
    server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    client,adress = server.accept()
    #TODO
    return client,adress


  def connClient(self,host, port):
    #TODO
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host,port))
    print("TODO")
    return server

