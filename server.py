import socket

s = socket.socket()
host = socket.gethostname()
port = 1337
s.bind((host, port))

s.listen(5)
while True:
    client,address = s.accept()
    print( "connected from", address )
    client.sendall(b'Connected thank you')
    print(client.recv(1024))
