import hashlib
from hashlib import pbkdf2_hmac as pb
# from hashlib import sha256, shake_256

h = hashlib.sha256()
h.update(b"Hello World")
h = hashlib.shake_256(b"Hello World")

print(h.hexdigest(20))
print('\n')
print(h.hexdigest(100))


print('hehehehehe')

h1 = hashlib.new('sha256')
h1.update(b"Hello World")
print(h1.hexdigest())

our_app_iters = 500_000
dk = pb('sha256', b'password', b'salt' * 2, our_app_iters)
dk.hex()