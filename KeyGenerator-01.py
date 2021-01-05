# from key_generator.key_generator import generate
#
# key = generate()
# print(key.get_key())

import secrets

generated_key = secrets.token_hex(16)
print(generated_key)
print((generated_key.upper()))