# Secure File System (SFS)

Secure file system is a file server that allows users to store their data on an untrusted machine.
The machine encrypts user's data and is only provided to the internal users of the system. The system
uses the following cryptography tools:

1. AES Encryption for encrypting files on the server
    * The files are encrypted by calculating a key using the server's passphrase on login
    * Every time the client requests a file, filenames or directory names the server decrypts the data
    before passing it on to the RSA encryptor for communication
    * When the server receives data to save, the server encrypts it with its key before its stored
2. RSA assymetric encryption when communicating between the client and server
	* All data transfer between the server and the client is encrypted.
	* Keys are generated when the Client registers and the public key is shared on login
	* Data outgoing is always encrypted with the receiver's public key
	* Data incoming is decrypted with the receiver's private key
	
3. SHA-2 for hashing passwords and creating certificates
	* The client's password is hashed before it's sent in the socket for verification. The server then checks the hash if it matches the username and password that is stored on registry.
	* When the user successfully logs in, the server computes the checksum of its files and directories. If the checksum does not match, it sends a warning to the user.
	* Whenever an internal user modifies, creates or deletes a file, the checksum of the files are recalculated and stored to be verified later

## Authors

* **Lorenzo Zafra** - [enzozafra](https://github.com/enzozafra)
* **Alexander Nguyen** - [ahnguyen03](https://github.com/ahnguyen03)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.


### Prerequisites
To install, you will need Python 2.7, and Pip

On Ubuntu, they can be installed with

```
sudo apt-get install python-pip python-dev build-essential 
```
then update
```
sudo pip install --upgrade pip 
```

### Installing
clone the project

```
git clone https://github.com/EnzoZafra/SecureFileSystem.git
```

go to the projects directory

```
cd SecureFileSystem/
```

install packages

```
pip install -r requirements.txt
```

### Deploying
change directory into the src folder
```
ch src/
```
deploy the server on a machine
```
python server.py [portnumber]
```
* make sure that [portnumber] is accepting Ingress communication on the server

run the client and connect to the server
```
python client.py [serverhost] [portnumber]
```
* where [serverhost] is the hostname of the server and [portnumber] is the opened port in the server

### Instructions
1. When the server is launched, input a password. This password is used to generate an AES key
that will be used to encrypt the files and data in the server.

2. Deploy a client and connect to the server. The shell will ask you to register and log-in with a
username and password
```
what would you like to do? [1]: signin [2]: register :
Please input a username:
Please input a password:
```

3. When logged in, you will be able to use the following commands (in the client):
list the files and directories
```
ls [path]
```

change directory
```
cd [path]
```

create directory
```
mkdir [path]
```

remove file/directory
```
rm [path]
```

print current directory
```
pwd
```

move/rename files or directory
```
mv/move [source] [destination]
```

print file contents
```
cat [path]
```

open/edit files
```
vim/open/edit [filename]
```

change permissions for a file
```
chmod [permission]
```
* permission is in the form of 'OWNER,GROUP,OTHER'
for example (to set owner = RW, GROUP = R, OTHER = -):
```
chmod RW,R,N
```

logout of the client
```
logout
```

4. In the server, the administrator can change the group that a user belongs to using the following:
```
chgroup [username] [groupname]
```


## Built With

* [Python](https://www.python.org/) - Language used
* [PyCrypto](https://pypi.python.org/pypi/pycrypto) - Encryption library
* [ChecksumDir](https://pypi.python.org/pypi/checksumdir) - Checksum Integrity Checker

