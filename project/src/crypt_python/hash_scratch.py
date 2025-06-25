import hashlib

h = hashlib.sha256()
h.update(b"Hello World")
print(h.hexdigest())
print('hehehehehe')
h1 = hashlib.new('sha256')
h1.update(b"Hello World")
print(h1.hexdigest())