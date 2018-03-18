#!/usr/bin/env python
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES


KEYSIZE = 4096

class CryptoController:
  def __init__(self):
    self.keysize = KEYSIZE
    self.bs = 32
    self.iv = '47fb388f6fb0ae2492d5c08691131e2c'.decode('hex')

  def genAsymKeys(self):
    random = Random.new().read
    return RSA.generate(self.keysize, random)

  def getPublicKey(self, keypair):
    return keypair.publickey()

  def importKey(self, textkey):
    return RSA.importKey(textkey)

  def calculateHash(self, message):
    return SHA256.new(message).digest().encode("hex")

  def addSignature(self, keypair, hash):
    return keypair.sign(hash, '')

  def encrypt(self, pubkey, plaintext):
    cipher = PKCS1_OAEP.new(pubkey)
    return cipher.encrypt(plaintext)

  def decrypt(self, keypair, ciphertext):
    cipher = PKCS1_OAEP.new(keypair)
    return cipher.decrypt(ciphertext)

  def aesencrypt(self, key, plaintext):
    plaintext = self._pad(plaintext)
    cipher = AES.new(key, AES.MODE_CBC, self.iv)
    return (self.iv + cipher.encrypt(plaintext)).encode('hex')

  def aesdecrypt(self, key, ciphertext):
    try:
      ciphertext = ciphertext.decode('hex')
    except TypeError:
      return "error: this file has been tampered with"
    self.iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, self.iv)
    return self._unpad(cipher.decrypt(ciphertext[AES.block_size:])).decode('utf-8')

  def validateSignature(self, decrypted, pubkey, signature):
    recalcHash = SHA256.new(decrypted).digest().encode("hex")

    if(pubkey.verify(recalcHash, signature)):
      return True
    return False

  def genAesKey(self, passphrase):
    return SHA256.new(passphrase).digest()

  def pad(self, s):
      return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

  def _pad(self, s):
    return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

  def _unpad(self, s):
    return s[:-ord(s[len(s)-1:])]


  def encryptpath(self, key, path):
    splitpath = path.split("/")
    encrypted = []
    for dir in splitpath:
      if dir == '':
        continue
      if dir != '..' and dir != '.':
        dir = self.aesencrypt(key, dir)
      encrypted.append(dir)

    return "/".join(encrypted)

  def decryptpath(self, key, path):
    splitpath = path.split("/")
    decrypted = []
    for dir in splitpath:
      if dir == '':
        continue
      if dir != '..' and dir != '.':
        try:
          int(dir, 16)
          dir = self.aesdecrypt(key, dir)
        except ValueError:
          print("found tampered files")
          dir = dir + "*"
      decrypted.append(dir)

    return "/".join(decrypted)
