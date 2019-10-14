#typical style commands
rTypes=[]
iTypes=[]
#atypical ones
shiftTypes=[]
jumpTypes=[]
dataTypes=[]

#dictionary for opcodes/functin codes and registers
opcodes={}
function= {}


register= {'zero':'00000','at':'00001','v0':'00010','v1':'00011','a0':'00100','a1':'00101','a2':'00110','a3':'00111',
            't0':'01000','t1':'01001','t2':'01010','t3':'01011','t4':'01100','t5':'01101','t6':'01110','t7':'01111',
            's0':'10000','s1':'10001','s2':'10010','s3':'10011','s4':'10100','s5':'10101','s6':'10110','s7':'10111',
            't8':'11000','t9':'11001','k0':'11010','k1':'11011','gp':'11100','sp':'11101','fp':'11110','ra':'11111'}


def hexToBin(input,bits):
    ret=bin(int(input, 16))[2:].zfill(bits)
    return ret

def decToBin(input,bits):
    ret=bin(int(input,10))[2:].zfill(bits)
    return ret


def binToHex(input, places):
    ret=hex(int(input, 2))[2:].zfill(places).replace('0x','')
    return ret


def checkLength(dictionary, length, error):
    for x in dictionary:
        if len(dictionary[x])!=length:
            print(error+x+":"+dictionary[x])


def addRType(label, op,func):
    rTypes.append(label)
    opcodes[label]=hexToBin(op,6)
    function[label]=hexToBin(func,6)

    return
    
def addShiftType(label, op,func):
    shiftTypes.append(label)
    opcodes[label]=hexToBin(op,6)
    function[label]=hexToBin(func,6)

    return
    
def addIType(label, op):
    iTypes.append(label)
    opcodes[label]=hexToBin(op,6)
    return

def addDataType(label, op):
    dataTypes.append(label)
    opcodes[label]=hexToBin(op,6)
    return



def rType(command):
    op=opcodes[command[0]]
    rd=register[command[1]]
    rs=register[command[2]]
    rt=register[command[3]]
    shamt='00000'
    funct=function[command[0]]
    binary=op+rs+rt+rd+shamt+funct
    hexcode= binToHex(binary,8)
    return hexcode

def shiftType(command):
    op=opcodes[command[0]]
    rd=register[command[1]]
    rt=register[command[2]]
    rs='00000'
    shamt=decToBin(command[3],5)
    funct=function[command[0]]
    binary=op+rs+rt+rd+shamt+funct
    hexcode= binToHex(binary,8)
    return hexcode


def iType(command):
    
    op=opcodes[command[0]]
    rt=register[command[1]]
    rs=register[command[2]]
    immediate=decToBin(command[3],16)
    binary=op+rs+rt+immediate
    hexcode= binToHex(binary,8)
    return hexcode


def dataType(command):
    op=opcodes[command[0]]
    rt=register[command[1]]
    immediate=decToBin(command[2],16)
    rs=register[command[3]]
    binary=op+rs+rt+immediate
    hexcode= binToHex(binary,8)
    return hexcode



            
#typical rtypes    
addRType('add','0','20')
addRType('addu','0','21')
addRType('sub','0','22')
addRType('subu','0','23')
addRType('and','0','24')
addRType('or','0','25')
addRType('nor','0','27')
addRType('slt','0','2a')
addRType('sltu','0','2b')
#shift types/atyipcal r types
addShiftType('sll','0','00')
addShiftType('srl','0','02')

#typical I types
addIType('addi','8')
addIType('addiu','9')
addIType('andi','c')
addIType('ori','d')
addIType('slti','a')
addIType('sltiu','b')
#typical data types-atypical I Type
addDataType('lw','23')
addDataType('sw','2b')


checkLength(opcodes,6,"Bad OPcode:")
checkLength(function,6,"Bad Function:")
checkLength(register,5,"Bad Register:")
    



inName='test_case2'
outName=inName+'mine'
with open(inName+'.s') as f:
    raw = f.readlines()

raw = [x.strip() for x in raw] 
raw = [x.replace(',',' ') for x in raw]
raw = [x.replace('(',' ') for x in raw]
raw = [x.replace(')',' ') for x in raw]
raw = [x.replace('$','') for x in raw]
raw = [x.lower() for x in raw]

splitFeilds =[x.split() for x in raw]
outFile= open(outName+'.obj','w')

for x in splitFeilds:
    if x[0] in rTypes:
        outFile.write (rType(x)+'\n')
    elif x[0] in iTypes:
        outFile.write( iType(x)+'\n')
    elif x[0] in dataTypes:
        outFile.write(dataType(x)+'\n')
    elif x[0] in shiftTypes:
        outFile.write(shiftType(x)+'\n')
    else:
        outFile.write(''.join(x))
        outFile.write('yarrr\n')
outFile.close()     


with open(inName+'.obj') as f:
    correct = f.readlines()
with open(outName+'.obj') as f:
    mine = f.readlines()
correct = [x.strip() for x in correct] 
mine = [x.strip() for x in mine] 

for x in range (len(correct)):
    if correct[x]!=mine[x]:
        print('Error atline '+str(x))
        print('correct: '+correct[x]+'\nmine:\t'+mine[x])