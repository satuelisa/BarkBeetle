import os
import os.path
from os import path

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
    with open(f'{kind}.txt') as corrections:
        for line in corrections:
            line = line.strip()
            fields = line.split()
            filename = fields.pop(0)
            data = filename.split('_')
            flight = data[0]
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
                        former  = f'../individual/{variant}/{filename}'
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
    with open(f'{flight}.annot', 'w') as target:
        for line in output[flight]:
            print(line, file = target)
