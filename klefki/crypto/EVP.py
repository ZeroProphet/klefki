import os
import base64
import M2Crypto


class SymmetricEncryption(object):

    def __init__(self, key, iv, alg="aes_128_cbc"):
        self.iv = iv
        self.key = key
        self.alg = alg

    def encrypt(self, plaintext):
        ENCRYPT = 1
        cipher = M2Crypto.EVP.Cipher(alg=self.alg, key=self.key, iv=self.iv, op=ENCRYPT)
        ciphertext = cipher.update(plaintext) + cipher.final()
        return base64.b64encode(ciphertext)

    def decrypt(self, cyphertext):
        DECRYPT = 0
        cipher = M2Crypto.EVP.Cipher(alg=self.alg, key=self.key, iv=self.iv, op=DECRYPT)
        plaintext = cipher.update(base64.b64decode(cyphertext)) + cipher.final()
        return plaintext
