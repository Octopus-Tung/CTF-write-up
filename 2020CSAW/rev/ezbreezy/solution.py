enc = ['0x8e', '0x94', '0x89', '0x8f', '0xa3', '0x9d', '0x87', '0x90', '0x5c', '0x9e', '0x5b', '0x87', '0x9a', '0x5b', '0x8b', '0x58', '0x9e', '0x5b', '0x9a', '0x5b', '0x8c', '0x87', '0x95', '0x5b', '0xa5']

flag = ''
for i in enc:
    flag += chr(int(i, 16) - 40)
print(flag)
