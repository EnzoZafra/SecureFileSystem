import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA224

#TODO: Use something other than RSA?

KEYSIZE = 1024
class CryptoController:
  def __init__(self):
    self.keysize = KEYSIZE

  def genAsymKeys(self):
    random = Random.new().read
    return RSA.generate(self.keysize, random)

  def getPublicKey(self, keypair):
    return keypair.publickey()

  def calculateHash(self, message):
    return SHA224.new(message).digest()

  def addSignature(self, keypair, hash):
    return keypair.sign(hash, '')

  def encrypt(self, pubkey, plaintext):
    return pubkey.encrypt(plaintext, 32)

  def decrypt(self, keypair, ciphertext):
    return keypair.decrypt(ciphertext)

  def validateSignature(self, decrypted, pubkey, signature):
    recalcHash = SHA224.new(decrypted).digest()

    if(pubkey.verify(recalcHash, signature)):
      return True
    return False


cryptography = CryptoController()

# Generate RSA private/public key pairs for both parties...
keypair_snowden = cryptography.genAsymKeys()
keypair_pytn = cryptography.genAsymKeys()

# Public key export for exchange between parties...
pubkey_snowden  = cryptography.getPublicKey(keypair_snowden)
pubkey_pytn     = cryptography.getPublicKey(keypair_pytn)

# Plain text messages...
message_to_snowden  = 'You are a patriot!'
message_to_pytn     = "Russia is really nice this time of year...\nUse encryption and make the NSA CPUs churn and burn!"

# Generate digital signatures using private keys...
hash_of_snowden_message = cryptography.calculateHash(message_to_snowden)
signature_pytn = cryptography.addSignature(keypair_pytn, hash_of_snowden_message)
hash_of_pytn_message    = cryptography.calculateHash(message_to_pytn)
signature_snowden = cryptography.addSignature(keypair_snowden, hash_of_pytn_message)

# Encrypt messages using the other party's public key...
encrypted_for_snowden   = cryptography.encrypt(pubkey_snowden, message_to_snowden)    #from PyTN
encrypted_for_pytn      = cryptography.encrypt(pubkey_pytn, message_to_pytn)          #from Snowden

# Decrypt messages using own private keys...
decrypted_snowden   = cryptography.decrypt(keypair_snowden, encrypted_for_snowden)
decrypted_pytn      = cryptography.decrypt(keypair_pytn, encrypted_for_pytn)

# Signature validation and console output...
# if(cryptography.validateSignature(decrypted_snowden, pubkey_pytn, signature_pytn)):
#     print "Edward Snowden received from PyTn:"
#     print decrypted_snowden
#     print ""

# if(cryptography.validateSignature(decrypted_pytn, pubkey_snowden, signature_snowden)):
#    print "PyTN received from Edward Snowden:"
#    print decrypted_pytn
