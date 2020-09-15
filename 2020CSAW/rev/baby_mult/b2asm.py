from pwn import *

context.arch = 'amd64'

with open('program.txt', 'r') as fp:
    codes = fp.read()[:-1].split(',')

code = ''.join([chr(int(i.strip())) for i in codes])
print(disasm(code))
