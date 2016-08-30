from Crypto.Cipher import DES

f = open('key.txt', 'r')
key_hex = f.readline()[:-1] # discard newline
f.close()
KEY = key_hex.decode("hex")
IV = '13245678'
a = DES.new(KEY, DES.MODE_OFB, IV)

f = open('ciphertext', 'r')
ciphertext = f.read()
f.close()

plaintext = a.decrypt(ciphertext)
f = open('plaintext', 'w')
f.write(plaintext)
f.close()
