from pwn import *

r = remote('crypto.chal.csaw.io', 5001)

flag = ''
r.recvline()

for i in range(200):

    r.recv()

    r.sendline('0' * 47)
    cipher = r.recvline()
    
    cipher = cipher[len('Ciphertext is:  '):]
    r.recvline()

    if cipher[:32] == cipher[32:64]:
        mode = 'ECB'
        flag += '0'
    else:
        mode = 'CBC'
        flag += '1'
    
    r.sendline(mode)
    if len(flag) == 8:
        print(chr(int(flag, 2)), end = '')
        flag = ''

r.close()
