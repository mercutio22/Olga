#!/usr/bin/env python
from oosheet import OOSheet as S
import pdb
import json

S('a1').string = 'Nome'
S('b1').string = 'Clinica'
S('c1').string = 'Endereco'

with open('scraped.json') as f:
	data = f.read()
	data = json.loads(data)

	i = 2
	for line in data:
		#for k, v in line.iteritems():
			#if k == 'clinics' and len(v) > 1:
			#	print line
		try:
			S('a' + str(i)).string = line['name'][0]
			S('b' + str(i)).string = line['clinics'][0]
			S('c' + str(i)).string = line['addresses'][0]
			i += 1
		except IndexError:
			pass
		
			

	pdb.set_trace()
	print data