for index in range(100):
	print = (lambda j,m:(lambda f,t:t if len(t) <= 1 else j([f(f,x)for x in m(j,m(reversed,(lambda s:zip(*[iter(s)]*(len(s)/2)))(t+"\x01"*(len(t)%2))))]))(lambda f,t:t if len(t) <= 1 else j([f(f,x)for x in m(j,m(reversed,(lambda s: zip(*[iter(s)]*(len(s)/2)))(t+"\x01"*(len(t)%2))))]),raw_input("Plaintext:")))(''.join,map).replace("\x01","")
