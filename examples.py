import os.path
from sys import argv
from math import ceil, sqrt
from random import randint, choice
from PIL import Image, ImageDraw

margin = 12
size = 600
rows = 4
cols = 2
w = rows * size + (rows + 1) * margin
h = cols * size + (cols + 1) * margin
squares = Image.new('RGBA', (h, w))
circles = Image.new('RGBA', (h, w))
enhanced = Image.new('RGBA', (h, w))
datasets = ['jun60', 'jul90', 'jul100', 'aug90', 'aug100']
for kind in ['green', 'yellow', 'red', 'leafless']:
    chosen = set()
    x = margin
    y = margin
    col = 0
    while len(chosen) < rows * cols:
        tID = randint(30, 100)
        d = choice(datasets)
        filename = f'{d}_{kind}_t{tID}.png'
        if os.path.exists(filename):
            chosen.add(filename)
            sample = Image.open(filename).resize((size, size)).convert('RGBA')
            squares.paste(sample, (x, y), sample)
            sample = Image.open(f'{d}_{kind}_s{tID}.png').resize((size, size)).convert('RGBA')            
            circles.paste(sample, (x, y), sample)
            sample = Image.open(f'{d}_{kind}_s{tID}_enhanced.png').resize((size, size)).convert('RGBA')            
            enhanced.paste(sample, (x, y), sample)
            x += size + margin
            col += 1
            if col == cols:
                y += size + margin
                x = margin
                col = 0
    squares.save(f'examples_{kind}_squares.png')
    circles.save(f'examples_{kind}_circles.png')
    enhanced.save(f'examples_{kind}_enhanced.png')
