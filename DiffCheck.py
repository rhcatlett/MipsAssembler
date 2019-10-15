#!/usr/bin/env python3
import sys
fileA=sys.argv[1]
fileB=sys.argv[2]

with open(fileA) as f:
    linesA = f.readlines()

with open(fileB) as f:
    linesB = f.readlines()

for i in range(len(linesA)):
    if linesA[i]!=linesB[i]:
        print('Error at line: '+str(i-1))
        print('\t'+linesA[i]+'!='+linesB[i])