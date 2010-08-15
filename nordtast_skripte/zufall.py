#-*- coding: utf-8 -*-
import codecs

import random
random.seed()

alfa = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
        'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
        'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
        'y', 'z', 'ä', 'ö', 'ü', 'ß', ',', '.']

aus = codecs.open('tastaturen.txt', encoding = 'utf-8', mode = 'w')

i = 0
while i <= 200:
	random.shuffle(alfa)
	#tmp = alfa[0:13] + ['e'] + alfa[13:17] + ['n'] + alfa[17:]
	#ta = ''.join(tmp)
        #aus.write(ta.decode('utf-8') + '\n')
        aus.write(''.join(alfa).decode('utf-8') + '\n')
	i += 1
