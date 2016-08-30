CTF(x) Write-up
===================

Just finish two challenge, **crash** in forensics and **lambda** in crypto.

crash
-------------

At first, the given file is **flag.zip**.
unzip it, and get **flag.txt** in **flag/**.
Open it with vim, it show up some message about **flag.txt.swp**.
Recover it.

![flag](http://i.imgur.com/MaI7SfQ.png)

---------------------------------

lambda
-------------

The given file is **λ.py**, and a ciphertext : **n1s4_t1An(f1ctdb@mpl_h3)m3lp3y__Eas**

```
#λ.py
for index in range(100):
	print = (lambda j,m:(lambda f,t:t if len(t) <= 1 else j([f(f,x)for x in m(j,m(reversed,(lambda s:zip(*[iter(s)]*(len(s)/2)))(t+"\x01"*(len(t)%2))))]))(lambda f,t:t if len(t) <= 1 else j([f(f,x)for x in m(j,m(reversed,(lambda s: zip(*[iter(s)]*(len(s)/2)))(t+"\x01"*(len(t)%2))))]),raw_input("Plaintext:")))(''.join,map).replace("\x01","")
```

> **Note:**
> 
>  - According to the ciphertext, it seems to be encrypted by **substiution**.(I swear, I do not understand what the python code doing.)

Umm...maybe we can just encrypt it again and again, the result of this encryption might be a circlic chain.
I make another similar python program to deal with it.

```
#lambda.py
x = "n1s4_t1An(f1ctdb@mpl_h3)m3lp3y__Eas"
for index in range(100):
	x = (lambda j,m:(lambda f,t:t if len(t) <= 1 else j([f(f,x)for x in m(j,m(reversed,(lambda s:zip(*[iter(s)]*(len(s)/2)))(t+"\x01"*(len(t)%2))))]))(lambda f,t:t if len(t) <= 1 else j([f(f,x)for x in m(j,m(reversed,(lambda s: zip(*[iter(s)]*(len(s)/2)))(t+"\x01"*(len(t)%2))))]),x))(''.join,map).replace("\x01","")
	print x
```

And I need to collect all the result to find out the flag.

```
#cmd
python lambda.py > result
grep -e 'ctf(' result
```

Output : 
>ctf(1m@db4_1nsnAt1_y_h3asElp3pl_m3)
ctf(1@mbd4_1nsAn1ty__p3asEh_3lplm3)
ctf(1m@db4_1nsnAt1_yl_3asEp_3plhm3)
ctf(1@mbd4_1nsAn1ty_h_3asE_l3lppm3)
ctf(1m@db4_1nsnAt1_ypl3asE_h3pl_m3)
ctf(1@mbd4_1nsAn1ty__h3asElp3lp_m3)
ctf(1m@db4_1nsnAt1_y_p3asEh_3pllm3)
ctf(1@mbd4_1nsAn1ty_l_3asEp_3lphm3)
ctf(1m@db4_1nsnAt1_yh_3asE_l3plpm3)
**ctf(1@mbd4_1nsAn1ty_pl3asE_h3lp_m3)** <--true flag
ctf(1m@db4_1nsnAt1_y_h3asElp3pl_m3)
ctf(1@mbd4_1nsAn1ty__p3asEh_3lplm3)
ctf(1m@db4_1nsnAt1_yl_3asEp_3plhm3)
ctf(1@mbd4_1nsAn1ty_h_3asE_l3lppm3)
ctf(1m@db4_1nsnAt1_ypl3asE_h3pl_m3)
ctf(1@mbd4_1nsAn1ty__h3asElp3lp_m3)


