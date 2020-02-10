# line endings
# encoding stuff

ct = open("transmission1", "rb")
pt = open("pt.txt", "rb")

c_bytes = ct.read()
p_bytes = pt.read()

keystream = ""
for i in range(100):
    keyint = (c_bytes[i] ^ p_bytes[i]) # or 127?
    keystream += (chr(keyint))

print(keystream)   
ct.close()
pt.close()


ct = open("transmission2", 'rb')
c_bytes = ct.read()
plaintext = ""

for i in range(100):
    keyint = (c_bytes[i] ^ ord(keystream[i]))
    plaintext += (chr(keyint)) 

print(plaintext)

ct = open("transmission3",'rb')
c_bytes = ct.read()

print(c_bytes)