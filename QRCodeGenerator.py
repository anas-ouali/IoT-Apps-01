# import qrcode
# img = qrcode.make('Some data here')
# img.save()


import pyqrcode
# url = pyqrcode.create('Hello, World!')
url = pyqrcode.create('LW:D0:1122334455667788:AABBCCDDEEFF0011:AABB1122:OAABBCCDDEEFF:SYYWWNNNNNN:PFOOBAR:CAF2C')
# url = pyqrcode.create('Anas Ouali @ 3S')
# url.svg('uca-url.svg', scale=8)
# url.eps('uca-url.eps', scale=2)
# url.png('url-url.png', scale=8)
print(url.terminal(quiet_zone=1))