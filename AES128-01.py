# Import the Fernet class.
from cryptography.fernet import Fernet

# Use Fernet to generate the key file.
# key = Fernet.generate_key()
key = b'0-jpGXRBcs3DbSPYcmZOA8tO8E1rB3FBpUGaZG7YtG4='

# Store the file to disk to be accessed for en/de:crypting later.
# with open('secret.key', 'wb') as new_key_file:
#     new_key_file.write(key)

print("Key:", key.decode("utf-8"))

msg = "Hello, World!"
print("Message:", msg)

# Encode this as bytes to feed into the algorithm.
# (Refer to Encoding types above).
msg = msg.encode()

# Instantiate the object with your key.
f = Fernet(key)

# Pass your bytes type message into encrypt.
ciphertext = f.encrypt(msg)
print("Cipher Text:", ciphertext.decode("utf-8"))

# Load the private key from a file.
# with open('secret.key', 'rb') as my_private_key:
#     key = my_private_key.read()
# Instantiate Fernet on the recip system.

f = Fernet(key)
# Decrypt the message.

cleartext = f.decrypt(ciphertext)
# Decode the bytes back into a string.

cleartext = cleartext.decode()
print("Clear Text:", cleartext)