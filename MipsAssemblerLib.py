#A bunch of dictionaries and list to turn strings into corresponding ints and quickly figure out a strings type
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAPPINGS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#R  type commands
rTypes=[]#typical rtypes -format: command $rd,$rs,$rt
shiftTypes=[]#shamt shift types/atyipcal r types-format: command $rd,$rs, shamt
shiftVariableTypes=[]#variable shift types-format: command $rd,$rt,$rs
multTypes=[]#mult types/ atypical r types-format: command $rs, $rt
mfTypes=[]#mf types/ atyipcal r types-format: command $rd

#R Type Commds
iTypes=[]#typical I types-format: command $rt, $rs, immediate
relativeBranchTypes=[]#typical reatlive branches-atypical I type -format: command $rt, $rs, LABEL
dataTypes=[]#typical data types-atypical I Type-format: command $rt, immediat($rs)

#jumps not implmented
#jumpTypes=[]#typical jump types-form: command addr
#jumpAddrTypes=[]#typical jump types-form: command $rs
#dictionary for opcodes/functin codes and registers
opcodes={}
function= {}
register= {'zero':'00000','at':'00001','v0':'00010','v1':'00011','a0':'00100','a1':'00101','a2':'00110','a3':'00111',
            't0':'01000','t1':'01001','t2':'01010','t3':'01011','t4':'01100','t5':'01101','t6':'01110','t7':'01111',
            's0':'10000','s1':'10001','s2':'10010','s3':'10011','s4':'10100','s5':'10101','s6':'10110','s7':'10111',
            't8':'11000','t9':'11001','k0':'11010','k1':'11011','gp':'11100','sp':'11101','fp':'11110','ra':'11111'}
#dictionary for labels for jumping
labels={}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAPPINGS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




#is the given formatted line a label board
def isLabel(currentLine):
    return len(currentLine)==1 and currentLine[0].endswith(':') and currentLine[0].replace(':','') in labels


#the defualt python number format conversions are a little unweildy for my purpose
#just some wrappers to make them easier
#~~~~~~~~~~~~~~~~~~~~NUMBER FORMAT CONVERTERS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#convers an input,int or string type, in decimal format to a bits-long string binary representation
def decToBin(input,bits):
    ret=bin(int(str(input),10))[2:].zfill(bits)
    return ret

#same converts an int type input to a signed bits long binary string
def decToTwosComplment(input, bits):
    if input>=0:
       val= decToBin(input, bits)  
    else:
        msb=-2**bits
        rest=msb-input
        val=decToBin(rest,bits-1)
        val=val.replace('b','')
    return val


#converts an unsigned hex string to an unsigned bit string
def hexToBin(input,bits):
    ret=bin(int(input, 16))[2:].zfill(bits)
    return ret


#converts an unsigned binary string to hex string
def binToHex(input, places):
    ret=hex(int(input, 2))[2:].zfill(places).replace('0x','')
    return ret
#~~~~~~~~~~~~~~~~~~~~NUMBER FORMAT CONVERTERS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~DICTIONARY LOADERS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def checkLength(dictionary, length, error):
    for key in dictionary:
        if len(dictionary[key])!=length:
            print(error+key+":"+dictionary[key])

#handles adding typical r types to teh dictionaries
#typical rtypes -format: command $rd,$rs,$rt
def addRType(label, op,func):
    rTypes.append(label)
    opcodes[label]=hexToBin(op,6)
    function[label]=hexToBin(func,6)
    return

#shift types are atypical r types and are easiest to handkle sperately with my architecture
#shamt shift types/atyipcal r types-format: command $rd,$rs, shamt
def addShiftType(label, op,func):
    shiftTypes.append(label)
    opcodes[label]=hexToBin(op,6)
    function[label]=hexToBin(func,6)
    return

#variable shift types-format: command $rd,$rt,$rs    
def addShiftVariableType(label, op,func):
    shiftVariableTypes.append(label)
    opcodes[label]=hexToBin(op,6)
    function[label]=hexToBin(func,6)
    return

#mult types are atypical r types and are easiest to handkle sperately with my architecture
#mult types/ atypical r types-format: command $rs, $rt
def addMultType(label, op,func):
    multTypes.append(label)
    opcodes[label]=hexToBin(op,6)
    function[label]=hexToBin(func,6)
    return

#mf types/ atyipcal r types-format: command $rd
def addMFType(label, op,func):
    mfTypes.append(label)
    opcodes[label]=hexToBin(op,6)
    function[label]=hexToBin(func,6)
    return



#adds typical immidiate types to the dictionary
#typical I types-format: command $rt, $rs, immediate
def addIType(label, op):
    iTypes.append(label)
    opcodes[label]=hexToBin(op,6)
    return

#lw/sw/etc have an atypical format and it is easier to handle them sperately from typical I types
#typical data types-atypical I Type-format: command $rt, immediat($rs)def addDataType(label, op):
def addDataType(label, op):
    dataTypes.append(label)
    opcodes[label]=hexToBin(op,6)
    return

#beq/bne/etc have an atypical format and it is easier to handle them sperately from typical I types
#typical reatlive branches-atypical I type -format: command $rt, $rs, LABEL
def addRelativeBranch(label, op):
    relativeBranchTypes.append(label)
    opcodes[label]=hexToBin(op,6)
    return
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DICTIONARY LOADERS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~COMMAND ASSEMBLERS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# given a list of the four feilds in an r type, returns the hex encoding
#typical rtypes -format: command $rd,$rs,$rt
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

# given a list of the four feilds in an shift type, returns the hex encoding
#shamt shift types/atyipcal r types-format: command $rd,$rs, shamt
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

#variable shift types-format: command $rd,$rt,$rs
def shiftVariableType(command):
    op=opcodes[command[0]]
    rd=register[command[1]]
    rt=register[command[2]]
    rs=register[command[3]]
    shamt='00000'
    funct=function[command[0]]
    binary=op+rs+rt+rd+shamt+funct
    hexcode= binToHex(binary,8)
    return hexcode

#mult types/ atypical r types-format: command $rs, $rt
def multType(command):
    op=opcodes[command[0]]
    rd='00000'
    rs=register[command[1]]
    rt=register[command[2]]
    shamt='00000'
    funct=function[command[0]]
    binary=op+rs+rt+rd+shamt+funct
    hexcode= binToHex(binary,8)
    return hexcode

#mf types/ atyipcal r types-format: command $rd
def mfType(command):
    op=opcodes[command[0]]
    rd=register[command[1]]
    rs='00000'
    rt='00000'
    shamt='00000'
    funct=function[command[0]]
    binary=op+rs+rt+rd+shamt+funct
    hexcode= binToHex(binary,8)
    return hexcode



#I Types
# given a list of the four feilds in an I type, returns the hex encoding
#typical I types-format: command $rt, $rs, immediate
def iType(command):
    
    op=opcodes[command[0]]
    rt=register[command[1]]
    rs=register[command[2]]
    immediate=decToBin(command[3],16)
    binary=op+rs+rt+immediate
    hexcode= binToHex(binary,8)
    return hexcode

# given a list of the four feilds in a data type, the hex encoding
#typical data types-atypical I Type-format: command $rt, immediat($rs)
def dataType(command):
    op=opcodes[command[0]]
    rt=register[command[1]]
    immediate=decToBin(command[2],16)
    rs=register[command[3]]
    binary=op+rs+rt+immediate
    hexcode= binToHex(binary,8)
    return hexcode

# given a list of the three feilds in an relative branch type, returns the hex encoding
#typical reatlive branches-atypical I type -format: command $rt, $rs, LABEL
def relativeBranchType(command, line):
    op=opcodes[command[0]]
    rs=register[command[1]]
    rt=register[command[2]]
    targetLabel=command[3]
    jump=labels[targetLabel]-(line+1)
    immediate=decToTwosComplment(jump,16)
    binary=op+rs+rt+immediate
    hexcode= binToHex(binary,8)
    return hexcode

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~COMMAND ASSEMBLERS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
