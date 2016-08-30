Bosten Key Party CTF Write-up
===================

Well, it's my first time to play CTF, and I just soluted des-ofb in crypto.

----------

des-ofb
-------------

At first, there are two given files, **des-ofb.py** and **ciphertext**.

```
#des-ofb.py
from Crypto.Cipher import DES

f = open('key.txt', 'r')
key_hex = f.readline()[:-1] # discard newline
f.close()
KEY = key_hex.decode("hex")
IV = '13245678'
a = DES.new(KEY, DES.MODE_OFB, IV)

f = open('plaintext', 'r')
plaintext = f.read()
f.close()

ciphertext = a.encrypt(plaintext)
f = open('ciphertext', 'w')
f.write(ciphertext)
f.close()
```

des-ofb.py is the encrypt program, and ciphertext is the encrypted message.

> **Note:**
> 
> - Obviously, it's DES encryption with OFB mode.
> - The initialization vector has already exists.
> - Key is unknow, but the weakness of DES encryption is weak key.

I write a decryption program, and google the weak key.

```
#decrypt.py
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
```

After test mounts of weak key, there's one could crack the encrypted message.

> E0E0E0E0F1F1F1F1

The flag would be found on the last line of plaintext.

> Be all my sins remembered. BKPCTF{so_its_just_a_short_repeating_otp!}


