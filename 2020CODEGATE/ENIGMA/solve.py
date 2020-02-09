#!/usr/bin/env python3

p1 = "DON'T LET YOUR RIGHT HAND KNOW WHAT YOUR LEFT HAND DID"
c1 = "5+,'( \"2( )+-3 r-/:( :*,5 ',+1 1:*( )+-3 \"26( :*,5 5-d"

p2 = "ONCE A HACKER IS AN ETERNAL HACKER"
c2 = "+,92 * :*9'23 -4 *, 2(23,*\" :*9'23"

p3 = "A HACKER WITHOUT PHILOSOPHY IS JUST AN EVIL COMPUTER GENIUS"
c3 = "* :*9'23 1-(:+-( @:-\"+4+@:) -4 ;_4( *, 2?-\" 9+.@_(23 /2,-_4"

#cflag = "9+52/*(22020{:*9'234 *32 ,+( !+3, +,\") -( -4 .*52}"
cflag = ":*9'234 *32 ,+( !+3, +,\") -( -4 .*52"

p = p1 + p2 + p3
c = c1 + c2 + c3

table = {}
conflict = {}
for i in range(len(c)):
    if c[i] not in table:
        table[c[i]] = p[i]
    elif c[i] in table and table[c[i]] != p[i]:
        conflict[c[i]] = table[c[i]] + ' ' + p[i]
print(conflict)

pflag = ''
for i in cflag:
    if i in table:
        pflag += table[i]
    else:
        pflag += i
print(pflag)

for i in range(26):
    if chr(0x41 + i) not in p:
        print(chr(0x41 + i))
