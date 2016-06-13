#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Copyright 2016 LukeSkywalk3r

import json

n = open('add.txt', 'r')
fil = n.readline().strip()
print 'File: ' + fil

f = open(fil, 'r')

j = {}
j = json.load(f)
f.close()
words = []

for k in j['words']:
    words.append(k.lower())

for i in n:
    if not i.strip().lower() in words:
        j['words'].append(i.strip().lower())
        print '+' + i.strip().lower()

f = open(fil, 'w')
json.dump(j, f, indent=4)

f.close()
n.close()
