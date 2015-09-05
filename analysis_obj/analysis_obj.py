# -*- coding: utf-8 -*-

import sys

argvs = sys.argv
argc = len(argvs)

f = open(argvs[1], 'r')
line = f.readline()
while line:
    if line != '':
        print line
    line = f.readline()

f.close()



