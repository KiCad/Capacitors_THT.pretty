import os
import re

# Find only the Elko files
files = []
for file in os.listdir():
    if file[-9:] == "kicad_mod" and file[:4] == "Elko":
        files.append(file)

# regex to find the length        
findLen = re.compile(r"(?<=_)(?:\d*\.)?\d+")
# regex to find the diameter
findDia = re.compile(r"(?<=x)(?:\d*\.)?\d+")
# regex to find the pitch
findPitch = re.compile(r"(?<=RM)(?:\d*\.)?\d+")

for file in files:
    for m in findDia.finditer(file):
        D = m
    for m in findLen.finditer(file):
        L = m
    for m in findPitch.finditer(file):
        P = m
        
    newName = 'C_Radial_D'+str(D.group())+'_L'+str(L.group())+'_P'+str(P.group())+file[P.end():-10]
    
    with open(file, 'r') as f:
        data = f.readlines()
    
    # change the module name to match
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