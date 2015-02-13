import os
import re

files = []
for file in os.listdir():
    if file[-9:] == "kicad_mod" and file[:1] == "C": 
        files.append(file)
        
# regex to find the length        
findLen = re.compile(r"(?<=x)(?:\d*\.)?\d+")
# regex to find the diameter
findDia = re.compile(r"(?<=r)(?:\d*\.)?\d+")
# regex to find the pitch
findPitch = re.compile(r"(?<=RM)(?:\d*\.)?\d+")
# regex to check for Disc shape
findDisc = re.compile(r'(Disc)')

for file in files:
        
    newName = file.replace('-', '.')
    for m in findDia.finditer(newName):
        D = float(m.group())
    for m in findLen.finditer(newName):
        L = float(m.group())
    for m in findPitch.finditer(newName):
        P = float(m.group())
        PEnd = m.end()

    if findDisc.findall(newName):
        newName = 'C_Disc_D{0:g}'.format(D)+'_P{0:g}'.format(P)+file[PEnd:-10]    
    elif P>D and P>L:
        newName =  'C_Axial_D{0:g}'.format(D)+'_L{0:g}'.format(L)+'_P{0:g}'.format(P)+file[PEnd:-10]
    elif D>L:
        newName =  'C_Rect_L{0:g}'.format(D)+'_W{0:g}'.format(L)+'_P{0:g}'.format(P)+file[PEnd:-10]
    else:
        newName =  'C_Radial_D{0:g}'.format(D)+'_L{0:g}'.format(L)+'_P{0:g}'.format(P)+file[PEnd:-10]

    print(file, newName, sep=' => ')

    with open(file, 'r') as f:
        data = f.readlines()
    
    for i,line in enumerate(data):
        if line[:20] == '  (fp_text reference':
            test = re.compile(r"( \(at)+")
            for match in test.finditer(line):
                start = match.start()
            data[i] = '  (fp_text reference ' + newName + data[i][start:]

        if line[:7] == '(module':
            data[i] = '(module ' + newName + ' (layer F.Cu)\n'
        
        if line[:8] == '  (model':
            data[i] = '  (model Capacitors_ThroughHole/'+newName+'.wrl\n'
                
    with open(file, 'w') as f:
        f.writelines(data)    

    os.rename(file, newName+'.kicad_mod')