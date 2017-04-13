Volga CTF Write-up

keypass
---

>題目敘述：For reasons unknown an amature cryptographer wrote an application to generate “strong encryption keys”. One of these keys was used to encrypt a tar archive with the flag. They used openssl command line util with -aes-128-cbc. Could you please get the flag? It shouldn’t take much time…

>檔案：flag.zip.enc、keypass

首先逆向keypass得知輸出結果不會超出256組

其程式以python改寫為keypass.py

```
#keypass.py
pass_phrase = raw_input('pass_phrase:')
rdx = 0
rcx = len(pass_phrase)

for i in range(rcx):
	rdx = ord(pass_phrase[i]) ^ rdx

rsi = 0x7fffffff
rcx = 0x52
rax = rdx * 0x40f7 + 0x7cc8b
str = '2FuMlX%3kBJ:.N*epqA0Lh=En/diT1cwyaz$7SH,OoP;rUsWv4g\Z<tx(8mf>-#I?bDYC+RQ!K5jV69&)G'
result = ''

for j in range(17):
	rdx = rax % rsi
	offset = rdx % rcx
	rax = rdx * 0x40f7
	rax += 0x7cc8b
	result += str[offset]

print result
```

其256組輸出被我紀錄於strong_keys中

再寫一支python程式decrypt.py暴力破解

```
#decrypt.py
import os

f = open('strong_keys', 'r')

for i in range(256):
	key = f.readline()
	temp = 'openssl enc -aes128 -md sha256 -d -in flag.zip.enc -out a -pass pass:"'
	temp += key[:17] + '"'
	print temp
	os.system(temp)
	if os.system('unzip a') == 0:
		break

```

flag為VolgaCTF{L0ve_a11_trust_@_few_d0_not_reinvent_the_wh33l}
