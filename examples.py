import os.path
from sys import argv
from random import randint, choice
from PIL import Image, ImageDraw

maxattempts = 5000
margin = 15
size = 200
rows = int(argv[1])
cols = int(argv[2])
ground = 'ground' in argv
prefix = '' if not ground else 'ground/' 
w = rows * size + (rows + 1) * margin
h = cols * size + (cols + 1) * margin
datasets = ['jun60', 'jul90', 'jul100', 'aug90', 'aug100']
variants = ['squares', 'original', 'enhanced', 'thresholded', 'automaton']

start = 1 if ground else 31
end = 30 if ground else 5000 
for kind in ['green', 'yellow', 'red', 'leafless', 'ground']:
    images = { v : Image.new('RGBA', (h, w)) for v in variants } 
    chosen = set()
    x = margin
    y = margin
    col = 0
    attempts = 0
    while len(chosen) < rows * cols:
        tID = randint(start, end) 
        d = choice(datasets)
        suffix = f'{d}_{kind}_{tID}.png'
        add = False
        for v in variants:
            filename = f'{prefix}individual/{v}/{suffix}'
            if not os.path.exists(filename): 
                assert not add
                break # cannot use a non-existant sample
            if suffix not in chosen:
                chosen.add(suffix) # mark as used
                add = True
                print(suffix)
            sample = Image.open(filename).resize((size, size)).convert('RGBA')
            images[v].paste(sample, (x, y), sample)
        if add:
            x += size + margin
            col += 1
            if col == cols:
                y += size + margin
                x = margin
                col = 0
            add = False
            attempts = 0
        else:
            attempts += 1
            if attempts > maxattempts:
                break
    for v in variants:
        target = f'examples/{prefix}{v}/{kind}.png'
        images[v].save(target)
        
