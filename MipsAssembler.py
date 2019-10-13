rTypes=('add','addu', 'and')
opcodes= {'add':'000000','addu':'000000'}
function= {'add':'100000','addu':'100001'}
register= {'t0':'01000','t1':'01001','t2':'01010','t3':'01011'}

def rType(command):
    binary=opcodes[command[0]]+register[command[2]]+register[command[3]]+register[command[1]]+'00000'+function[command[0]]
    hexcode= hex(int(binary,2)).replace('0x','')
    return hexcode



sample = ['one', 'two', 'three', 'four']

if 'four' in sample:
   print True



with open('test.txt') as f:
    raw = f.readlines()

raw = [x.strip() for x in raw] 
raw = [x.replace(',',' ') for x in raw]
raw = [x.replace('(',' ') for x in raw]
raw = [x.replace(')',' ') for x in raw]
raw = [x.replace('$','') for x in raw]
raw = [x.lower() for x in raw]

splitFeilds =[x.split() for x in raw]
outFile= open("out.txt",'w')

for x in splitFeilds:
    if x[0] in rTypes:
        outFile.write (rType(x)+'\n')
    else:
        print(x)
        print('is not implemented\n')
outFile.close()     


