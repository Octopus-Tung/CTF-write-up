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

