import socket

s = socket.socket()
host = socket.gethostname()
port = 1337

s.connect((host, port))

print(s.recv(1024))
userInput = input("what would you like to do? ")
print(userInput)
splitUserInput = userInput.split()
print(splitUserInput)
cmd = splitUserInput[0]
filename = splitUserInput[1]
print(cmd)
print(filename)

if(len(userInput) == 0):
    print("Error Code")
if(cmd == 'cd'):
    print("cd|"+filename)
if(cmd == "mkdir"):
    print("mkdir|"+filename)
