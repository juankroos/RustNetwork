import hashlib

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