#!/usr/bin/env python3

import sys
import MipsAssemblerLib as MAL




#Fill the dictionaries up
#could be done statically, but it was a lot more typing and runtime speed isnt very important
#typical rtypes -format: command $rd,$rs,$rt
MAL.addRType('add','0','20')
MAL.addRType('sub','0','22')
MAL.addRType('addu','0','21')
MAL.addRType('subu','0','23')
MAL.addRType('and','0','24')
MAL.addRType('or','0','25')
MAL.addRType('nor','0','27')
MAL.addRType('xor','0','26')
MAL.addRType('slt','0','2a')
MAL.addRType('sltu','0','2b')


#shamt shift types/atyipcal r types-format: command $rd,$rs, shamt
MAL.addShiftType('sll','0','00')
MAL.addShiftType('srl','0','02')
MAL.addShiftType('sra','0','3')

#variable shift types-format: command $rd,$rt,$rs
MAL.addShiftVariableType('sllv','0','4')
MAL.addShiftVariableType('srlv','0','6')
MAL.addShiftVariableType('srav','0','7')
#addShiftVariableType('','0','')


#mult types/ atypical r types-format: command $rs, $rt
MAL.addMultType('mult','0','18')
MAL.addMultType('div','0','1a')
MAL.addMultType('multu','0','19')
MAL.addMultType('divu','0','1b')
#addMultType('','0','')

#mf types/ atyipcal r types-format: command $rd
MAL.addMFType('mfhi','0','10')
MAL.addMFType('mflo','0','12')

#addMFType('','0','')

#typical I types-format: command $rt, $rs, immediate
MAL.addIType('addi','8')
MAL.addIType('addiu','9')
MAL.addIType('andi','c')
MAL.addIType('ori','d')
MAL.addIType('xori','e')
MAL.addIType('slti','a')
MAL.addIType('sltiu','b')
#addIType('','')

#typical data types-atypical I Type-format: command $rt, immediat($rs)
MAL.addDataType('lb','20')
MAL.addDataType('lbu','24')
MAL.addDataType('lh','21')
MAL.addDataType('lhu','25')
MAL.addDataType('lw','23')
MAL.addDataType('sb','28')
MAL.addDataType('sw','2b')
MAL.addDataType('ll','20')
MAL.addDataType('sc','38')

#typical reatlive branches-atypical I type -format: command $rt, $rs, LABEL
MAL.addRelativeBranch('beq','4')
MAL.addRelativeBranch('bne','5')


#make sure the dictionary codes are the correct length
#not strictly necessary, but helps prevent preventable errors
MAL.checkLength(MAL.opcodes,6,"Bad OPcode:")
MAL.checkLength(MAL.function,6,"Bad Function:")
MAL.checkLength(MAL.register,5,"Bad Register:")
    
#the first passed argument is argv[1]
inName=sys.argv[1]
outName=inName.replace('.s','.obj')# turn *.s into *.obj

#read all the lines into raw
with open(inName) as f:
    raw = f.readlines()

#strip unneccsary whitespacing and syntax, force to lowercase
splitFeilds = [x.strip() for x in raw] 
splitFeilds = [x.replace(',',' ') for x in splitFeilds]
splitFeilds = [x.replace('(',' ') for x in splitFeilds]
splitFeilds = [x.replace(')',' ') for x in splitFeilds]
splitFeilds = [x.replace('$','') for x in splitFeilds]
splitFeilds = [x.lower() for x in splitFeilds]

#split each line into seperate feilds so that we have a two dimensional list
#of the lines and the feilds within the lines
splitFeilds =[x.split() for x in splitFeilds]


#go through the lines and handles the labels
#works with both freestanding labels and labels attached to other lines of code
#if the label is freestanding, it is left as is to maintain raw count later
#if the label is attached, it is removed from the line in splitfeilds
lineIndex=0
while lineIndex < len(splitFeilds):
    x=splitFeilds[lineIndex]

    if x[0].endswith(':'):
        mark=x[0].replace(':','')
        MAL.labels[mark]=lineIndex
        if len(x)!=1:
            del x[0]
   
    lineIndex+=1

#goes thrrough each line of commands after the labels have been handled
#shunts the commands off to the appropriate functions
compiledLineIndex=0 #the line number where it is compiled to, used for controlling branches
sourceLineIndex=1#the line where it lives in the source, used to retrieve the source for error logging
good=True#did we properly handle all commands
output=''#what should be written to files if we handled all commands
for currentLine in splitFeilds:
    didCommand=True
    #typical rtypes -format: command $rd,$rs,$rt
    if currentLine[0] in MAL.rTypes:
        output+=MAL.rType(currentLine)
    #shamt shift types/atyipcal r types-format: command $rd,$rs, shamt
    elif currentLine[0] in MAL.shiftTypes:
        output+=MAL.shiftType(currentLine)
    #variable shift types-format: command $rd,$rt,$rs
    elif currentLine[0] in MAL.shiftVariableTypes:
        output+=MAL.shiftVariableType(currentLine)
    #mult types/ atypical r types-format: command $rs, $rt
    elif currentLine[0] in MAL.multTypes:
        output+=MAL.multType(currentLine)
    #mf types/ atyipcal r types-format: command $rd
    elif currentLine[0] in MAL.mfTypes:
        output+=MAL.mfType(currentLine)
    #typical I types-format: command $rt, $rs, immediate
    elif currentLine[0] in MAL.iTypes:
        output+= MAL.iType(currentLine)
    #typical data types-atypical I Type-format: command $rt, immediat($rs)
    elif currentLine[0] in MAL.dataTypes:
        output+=MAL.dataType(currentLine)
    #typical reatlive branches-atypical I type -format: command $rt, $rs, LABEL
    elif currentLine[0] in MAL.relativeBranchTypes:
        output+=MAL.relativeBranchType(currentLine,compiledLineIndex)
        #if the current line is just a label, it should not be turned into hex codes
        #still useful to trrack to help backtrack to errorfull lines in the source
    elif MAL.isLabel(currentLine):
        didCommand=False#we always want to increment source and add a newline
                        #to the compiled code if we operated on a command
                        #thhe only time we dont want to is when we didn't operate on a command
                        #which only happens with labels

    else:#if the command is unimplmented, dont print to file
         #but keep going to collect error messages
        good=False
        errorMessage='Cannot assemble line #'+str(sourceLineIndex)+':'+str(raw[sourceLineIndex-1])
        out+=errorMessage
        print (errorMessage)
    
    sourceLineIndex+=1#we always are
    if(didCommand):
        output+='\n'
        compiledLineIndex+=1
        didCommand=True
#if no errors write to file
if good==True:
    outFile= open(outName,'w')
    outFile.write(output)
    outFile.close()   