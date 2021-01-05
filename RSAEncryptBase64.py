pubkey = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnUy1nwiVvg77scK9ZmIE
dZbnRo7zf+xTs+mz/X5Uiwf1chh35yC/Yhsex1CNCku0mRrfjNbHvxCDvHrHZiD4
AFEGHM6yOmEWNAXNxT+HgZZnCuc0fPDWtC1GikI5LDE1beCjUmzMSPF77Ov5e4gk
HdU1NxonXR8pJwUKoRUmTbhH1QqYRPVnkNSQZAjZpvPVzGZPF5jLRZ8y77Be9UeL
YpPUd74JWMXvRK33CXuW12RrbyfxPSdjEWYdHOuZgpWdnJbDPXlqe15T4XI+oEYR
pRD64+Jgv/BrWsgLP8ua/sd4UH67BLyKj9gTwpHJaEAsAjJdvRCYA4ZPJm8xdGja
AwIDAQAB
-----END PUBLIC KEY-----"""

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from base64 import b64decode,b64encode

AppKey = "00000000000000000000000000000000"
print("AppKey:", AppKey)
keyPub = RSA.importKey(pubkey) # import the public key
cipher = Cipher_PKCS1_v1_5.new(keyPub)
# print(cipher.encrypt.__doc__)
cipher_text = cipher.encrypt(AppKey.encode()) # now we have the cipher
print("Encrypted AppKey:", cipher_text)


# keyPriv = RSA.importKey(prvkey) # import the private key
# cipher = Cipher_PKCS1_v1_5.new(keyPriv)
# #print(cipher.decrypt.__doc__)
# decrypt_text = cipher.decrypt(cipher_text, None).decode()
# print("decrypted msg->", decrypt_text)
# assert msg == decrypt_text # check that
# print("test passed")