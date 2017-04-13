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
