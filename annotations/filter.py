import os
import os.path
from os import path

offsets = dict()
with open('../offsets.txt') as od:
    for line in od:
        fields = line.split()
        f = fields[2]
        offsets[f] = dict()
        offsets[f]['x'] = int(fields[3])
        offsets[f]['y'] = int(fields[4])

flights = ['jun60', 'jul90', 'jul100', 'aug90', 'aug100']
classes = ['green', 'yellow', 'red', 'leafless', 'ground']
variants = ['automaton', 'enhanced', 'original', 'squares', 'thresholded']
original = dict()
filtered = dict()
output = dict()

for flight in flights:
    original[flight] = dict()
    filtered[flight] = dict()
    output[flight] = []
    with open(f'{flight}.annot') as annotations:
        for line in annotations:
            line = line.strip()
            if '#' in line:
                output[flight].append(line)
            else:
                fields = line.split()
                treeID = int(fields.pop(0))
                if treeID <= 30: # ground annotation
                    output[flight].append(line)
                else:
                    label = fields.pop(0)
                    if label not in original[flight]:
                        original[flight][label] = dict()
                        filtered[flight][label] = dict()                        
                    x = int(fields.pop(0)) # pixel column
                    y = int(fields.pop(0)) # pixel row
                    original[flight][label][treeID] = (x, y)
                
for kind in classes:
    if not path.exists(f'{kind}.txt'):
        continue
    with open(f'{kind}.txt') as corrections:
        for line in corrections:
            line = line.strip()
            fields = line.split()
            filename = fields.pop(0)
            data = filename.split('_')
            flight = data[0].split('/')[-1]
            label = data[1]
            treeID = int(data[2][:-4]) # remove .png
            if treeID not in original[flight][label]:
                print(f'WARNING: correction ignored for a {label} {treeID} in {flight} as there is no such tree')
                continue
            (x, y) = original[flight][label][treeID]
            del original[flight][label][treeID]
            if len(fields) == 0: # no correction, pass it over as such
                filtered[flight][label][treeID] = (x, y)
            else: # there is a correction, make the required change
                correction = fields.pop(0)
                if correction in ['discard', 'overexposed']:
                    for variant in variants: # in case extracted files exist
                        former  = f'../individual/{variant}/{kind}/{filename}'
                        if path.exists(former):
                            os.system(f'rm {former}') # delete it
                        else:
                            print(f'WARNING: file {former} has already been erased')
                elif correction in classes:
                    filtered[flight][correction][treeID] = (x, y)
                    for variant in variants: # in case extracted files exist
                        former  = f'../individual/{variant}/{filename}'
                        altered = filename.replace(label, correction)
                        corrected  = f'../individual/{variant}/{altered}'
                        if path.exists(former):
                            os.system(f'mv {former} {corrected}') # rename it
                        else:
                            print(f'WARNING: file {former} has already been moved')                            
                else:
                    print(f'ERROR: unknown correction {line}')
                    
for flight in filtered: # all the corrections that were made
    for kind in filtered[flight]:
        for treeID in filtered[flight][kind]:
            (x, y) = filtered[flight][kind][treeID]
            output[flight].append(f'{treeID} {kind} {x} {y}')
                    
for flight in original: # anything that was not mentioned in the corrections
    for kind in original[flight]:
        for treeID in original[flight][kind]:
            (x, y) = original[flight][kind][treeID]
            output[flight].append(f'{treeID} {kind} {x} {y}')

        
for flight in output: # overwrite the annotation files
    assert flight in offsets
    with open(f'{flight}.annot', 'w') as target:
        for line in output[flight]:
            print(line, file = target)
    with open(f'{flight}.raw', 'w') as target:
        for line in output[flight]:
            if '#' in line:
                continue
            line = line.strip()
            fields = line.split()
            if len(fields) == 4: # an image-based annotation
                fields.pop(0) # the raw file does not include the tree IDs
                label = fields.pop(0)
                x = int(fields.pop(0)) + offsets[flight]['x'] 
                y = int(fields.pop(0)) + offsets[flight]['y'] 
                print(f'{flight} {label} {x} {y}', file = target)

