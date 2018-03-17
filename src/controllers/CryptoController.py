#!/usr/bin/env python
import Crypto
import base64
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
    # message = self.pad(plaintext)
    # iv = Random.new().read(AES.block_size)
    # cipher = AES.new(key, AES.MODE_CBC, iv)
    # return iv + cipher.encrypt(message)
    plaintext = self._pad(plaintext)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(plaintext))

  def aesdecrypt(self, key, ciphertext):
    # iv = ciphertext[:AES.block_size]
    # cipher = AES.new(key, AES.MODE_CBC, iv)
    # plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    # return plaintext.rstrip(b"\0")
    ciphertext = base64.b64decode(ciphertext)
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
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
