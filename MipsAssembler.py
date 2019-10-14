#!/usr/bin/env python3

import sys

#typical style commands my cpp instructor would yell at me for all these global variables
rTypes=[]
iTypes=[]
#atypical ones
shiftTypes=[]
jumpTypes=[]
dataTypes=[]
relativeBranchTypes=[]
#dictionary for opcodes/functin codes and registers
opcodes={}
function= {}
register= {'zero':'00000','at':'00001','v0':'00010','v1':'00011','a0':'00100','a1':'00101','a2':'00110','a3':'00111',
            't0':'01000','t1':'01001','t2':'01010','t3':'01011','t4':'01100','t5':'01101','t6':'01110','t7':'01111',
            's0':'10000','s1':'10001','s2':'10010','s3':'10011','s4':'10100','s5':'10101','s6':'10110','s7':'10111',
            't8':'11000','t9':'11001','k0':'11010','k1':'11011','gp':'11100','sp':'11101','fp':'11110','ra':'11111'}
#dictionary for labels for jumping
labels={}




def decToBin(input,bits):
    ret=bin(int(str(input),10))[2:].zfill(bits)
    return ret


def decToTwosComplment(input, bits):
    if input>=0:
       val= decToBin(input, bits)  
    else:
        msb=-2**bits
        rest=msb-input
        val=decToBin(rest,bits-1)
        val=val.replace('b','')
    return val



def hexToBin(input,bits):
    ret=bin(int(input, 16))[2:].zfill(bits)
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

def addRelativeBranch(label, op):
    relativeBranchTypes.append(label)
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


#Fill the dictionaries up
#could be done statically, but it was a lot more typing and runtime speed isnt very important


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

#typical reatlive branches-atypical I type
addRelativeBranch('beq','4')
addRelativeBranch('bne','5')


#make sure the dictionary codes are the correct length
#not strictly necessary, but helps prevent preventable errors
checkLength(opcodes,6,"Bad OPcode:")
checkLength(function,6,"Bad Function:")
checkLength(register,5,"Bad Register:")
    
#the first passed argument is argv[1]
inName=sys.argv[1]
outName=inName.replace('.s','.obj')

#read all the lines into raw
with open(inName) as f:
    raw = f.readlines()

#strip unneccsary whitespacing and syntax, force to lowercase
raw = [x.strip() for x in raw] 
raw = [x.replace(',',' ') for x in raw]
raw = [x.replace('(',' ') for x in raw]
raw = [x.replace(')',' ') for x in raw]
raw = [x.replace('$','') for x in raw]
raw = [x.lower() for x in raw]

#split each line into seperate feilds so that we have a two dimensional list
#of the lines and the feilds within the lines
splitFeilds =[x.split() for x in raw]


#go through the lines and handles the labels
#does so by removing the labels from splitFeilds and filling
#the labels dictionary with the label:line pairs
#currently assumes each label has its own line
lineIndex=0
while lineIndex < len(splitFeilds):
    x=splitFeilds[lineIndex]
    if len(x)==1:
        mark=x[0].replace(':','')
        labels[mark]=lineIndex
        splitFeilds.remove(x)
    else:
        lineIndex+=1

#goes thrrough each line of commands after the labels have been handled
#shunts the commands off to the appropriate functions
lineIndex=0
good=True#did we properly handle all commands
output=''
for currentLine in splitFeilds:
    if currentLine[0] in rTypes:
        output+=rType(currentLine)+'\n'
    elif currentLine[0] in iTypes:
        output+= iType(currentLine)+'\n'
    elif currentLine[0] in dataTypes:
        output+=dataType(currentLine)+'\n'
    elif currentLine[0] in shiftTypes:
        output+=shiftType(currentLine)+'\n'
    elif currentLine[0] in relativeBranchTypes:
        output+=relativeBranchType(currentLine,lineIndex)+'\n'
    else:#if the command is unimplmented, dont print to file
         #but keep going to collect error messages
        good=False
        print(x)
    lineIndex+=1
#if no errors write to file
if good==True:
    outFile= open(outName,'w')
    outFile.write(output)
    outFile.close()   