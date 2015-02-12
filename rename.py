import os

# rename the files
# for file in os.listdir():
    # if file[-9:] == "kicad_mod":
        # print('Renaming ',file)
        # os.rename(file, file[:1]+'_'+file[3:])
        

# change the module name to match
for file in os.listdir():
    if file[-9:] == "kicad_mod":
        data = []
        with open(file, 'r') as f:
            data = f.readlines()
        for i,line in enumerate(data):
            if line[:20] == '  (fp_text reference':
                data[i] = line[:22]+'_'+line[24:]
        with open(file, 'w') as f:
            f.writelines(data)        

# change the reference text to match
for file in os.listdir():
    if file[-9:] == "kicad_mod":
        data = []
        with open(file, 'r') as f:
            data = f.readlines()
        for i,line in enumerate(data):
            if line[:7] == '(module':
                data[i] = line[:9]+'_'+line[11:]
        with open(file, 'w') as f:
            f.writelines(data)

# change the reference text to match
for file in os.listdir():
    if file[-9:] == "kicad_mod":
        data = []
        with open(file, 'r') as f:
            data = f.readlines()
        for i,line in enumerate(data):
            if line[:8] == '  (model':
                data[i] = (line[:33]+'_'+line[41:])
        with open(file, 'w') as f:
            f.writelines(data)