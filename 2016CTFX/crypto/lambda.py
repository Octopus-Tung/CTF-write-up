x = "n1s4_t1An(f1ctdb@mpl_h3)m3lp3y__Eas"
for index in range(100):
	x = (lambda j,m:(lambda f,t:t if len(t) <= 1 else j([f(f,x)for x in m(j,m(reversed,(lambda s:zip(*[iter(s)]*(len(s)/2)))(t+"\x01"*(len(t)%2))))]))(lambda f,t:t if len(t) <= 1 else j([f(f,x)for x in m(j,m(reversed,(lambda s: zip(*[iter(s)]*(len(s)/2)))(t+"\x01"*(len(t)%2))))]),x))(''.join,map).replace("\x01","")
	print x
