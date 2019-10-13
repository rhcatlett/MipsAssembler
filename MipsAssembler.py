with open('test.txt') as f:
    raw = f.readlines()

raw = [x.strip() for x in raw] 
raw = [x.replace(',',' ') for x in raw]
raw = [x.replace('(',' ') for x in raw]
raw = [x.replace(')',' ') for x in raw]

file = open('rawout.txt','w') 
for item in raw:
    file.write(item+'\n')
file.close()



