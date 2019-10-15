#!/usr/bin/env python3

import sys
import MipsAssemblerLib as MAL
#Personal library of useful functions
#split for readability of code

#load the dictionaries up with the defualt mips instructions
MAL.initiliazeDictionaries()

#the first passed argument is argv[1] and should be the infile
inName=sys.argv[1]
#outfile name should be the same, just .obj
outName=inName.replace('.s','.obj')# turn *.s into *.obj

#read all the lines into list raw with an entry for each line 
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
compiledLineIndex=0#only increment compiledLineIndex when we move up a line in the compiled code
                    # a solo lable does not compile to any code, so it should not increment compiledLineIndex
for x in splitFeilds:
    if x[0].endswith(':'):
        mark=x[0].replace(':','')#the labels dont have colons when attached to a command, so the colons
                                #usefulness ends here, so drop it
        MAL.labels[mark]=compiledLineIndex
        if len(x)!=1:
            del x[0]
            compiledLineIndex+=1
    else:
        compiledLineIndex+=1

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
        #typical data types-atypical I Type-format: command $rt, immediat($rs)
    elif currentLine[0] in MAL.jumpAddrTypes:
        output+=MAL.jumpAddrType(currentLine)
    #special types without friends
    elif currentLine[0] in MAL.specialTypes:
        if currentLine[0]== 'lui':
                op=MAL.opcodes[currentLine[0]]
                rt=MAL.register[currentLine[1]]
                rs='00000'
                immediate=MAL.decToTwosComplment(currentLine[2],16)
                binary=op+rs+rt+immediate
                output+= MAL.binToHex(binary,8)
        elif currentLine[0]== 'syscall':
                op=MAL.opcodes[currentLine[0]]
                rd='00000'
                rt='00000'
                rs='00000'
                shamt='00000'
                funct=MAL.function[currentLine[0]]
                binary=op+rs+rt+rd+shamt+funct
                output+= MAL.binToHex(binary,8)
        #branch should be unreachable, it should only be in specialTypes if it is implmented
        else:
            good=False
            errorMessage='Cannot assemble line #'+str(sourceLineIndex)+':'+str(raw[sourceLineIndex-1])
            output+=errorMessage
            print (errorMessage)   
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
        errorMessage='Cannot assemble '+str(sourceLineIndex)+' at '+str(raw[sourceLineIndex-1])
        output+=errorMessage
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