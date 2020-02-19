import os.path
from sys import argv
from random import randint, choice
from PIL import Image, ImageDraw

margin = 10
size = 500
rows = 4
cols = 2
w = rows * size + (rows + 1) * margin
h = cols * size + (cols + 1) * margin
datasets = ['jun60', 'jul90', 'jul100', 'aug90', 'aug100']
variants = ['squares', 'original', 'enhanced', 'thresholded', 'automaton']

for kind in ['green', 'yellow', 'red', 'leafless']:
    images = { v : Image.new('RGBA', (h, w)) for v in variants } 
    chosen = set()
    x = margin
    y = margin
    col = 0
    while len(chosen) < rows * cols:
        tID = randint(30, 100) 
        d = choice(datasets)
        suffix = f'{d}_{kind}_{tID}.png'
        success = False
        for v in variants:
            filename = f'individual/{v}/{suffix}'
            if not os.path.exists(filename): 
                assert not success
                break # cannot use a non-existant sample
            if suffix not in chosen:
                chosen.add(suffix) # mark as used
                success = True
                print(suffix)                
            else:
                break
            sample = Image.open(filename).resize((size, size)).convert('RGBA')
            images[v].paste(sample, (x, y), sample)
        if success:
            x += size + margin
            col += 1
            if col == cols:
                y += size + margin
                x = margin
                col = 0
    for v in variants:
        images[v].save(f'examples/{v}/{kind}.png')

