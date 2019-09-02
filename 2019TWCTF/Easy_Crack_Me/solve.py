from z3 import *
import os

flag = []

for i in range(32):
    flag.append(BitVec(i, 7))

s = Solver()

a = [0, 1, 3, 8, 11, 12, 15, 18, 20, 21, 26, 30]

for i in range(32):
    if i in a:
        s.add(flag[i] > 96, flag[i] < 103)
    else:
        s.add(flag[i] > 47, flag[i] < 58, flag[i] != 51)

a = 0
b = 0
x = 0
y = [0x15e, 0xda, 0x12f, 0x131, 0x100, 0x131, 0xfb, 0x102]
z = [0x52, 0xc, 0x1, 0xf, 0x5c, 0x5, 0x53, 0x58]
for i in range(8):
    for j in range(4):
        x = flag[4 * i] + j
        a = a + x
        b = b ^ x
    #print(4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3, hex(y[i]), hex(z[i]))
    s.add(flag[4 * i] + flag[4 * i + 1] + flag[4 * i + 2] + flag[4 * i + 3] == y[i])
    s.add(flag[4 * i] ^ flag[4 * i + 1] ^ flag[4 * i + 2] ^ flag[4 * i + 3] == z[i])

a = 0
b = 0
x = 0
y = [0x129, 0x103, 0x12b, 0x131, 0x135, 0x10b, 0xff, 0xff]
z = [0x1, 0x57, 0x7, 0xd, 0xd, 0x53, 0x51, 0x51]
for i in range(8):
    for j in range(4):
        x = flag[8 * j] + i
        a = a + x
        b = b ^ x
    #print(i, i + 8, i + 16, i + 24, hex(y[i]), hex(z[i]))
    s.add(flag[i] + flag[i + 8] + flag[i + 16] + flag[i + 24] == y[i])
    s.add(flag[i] ^ flag[i + 8] ^ flag[i + 16] ^ flag[i + 24] == z[i])

s.add(flag[1] == 102, flag[5] == 56, flag[6] == 55, flag[17] == 50, flag[25] == 52, flag[31] == 53)
s.add(flag[0] + flag[2] + flag[4] + flag[6] + flag[8] + flag[10] + flag[12] + flag[14] + flag[16] + flag[18] + flag[20] + flag[22] + flag[24] + flag[26] + flag[28] + flag[30] == 1160)
s.add(flag[0] + flag[1] + flag[3] + flag[8] + flag[11] + flag[12] + flag[15] + flag[18] + flag[20] + flag[21] + flag[26] + flag[30] == 1198)

while s.check() == sat:
    f1a9 = 'TWCTF{' + ''.join([chr(s.model()[each].as_long()) for each in flag]) + '}'
    if os.popen('./easy_crack_me ' + f1a9).read().split()[0] == 'Correct:':
        print f1a9
        break
    s.add(Or(flag[0] != s.model()[flag[0]], flag[4] != s.model()[flag[4]], flag[8] != s.model()[flag[8]], flag[12] != s.model()[flag[12]], flag[16] != s.model()[flag[16]], flag[20] != s.model()[flag[20]], flag[24] != s.model()[flag[24]], flag[28] != s.model()[flag[28]]))

