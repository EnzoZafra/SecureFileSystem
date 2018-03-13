import socket

s = socket.socket()
host = socket.gethostname()
port = 1337
s.bind((host, port))
s.listen(5)
client = None
while True:
    if client is None:
        print("Still connecting")
        client, address = s.accept()
        print( "connected from", address )
    else:
        print(" Response from Client")
        inputToClient = "Command Recieved was: " + client.recv(1024).decode()
        byteinputToClient = inputToClient.encode()
        client.send(byteinputToClient)

