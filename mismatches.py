import os.path
from sys import argv
from random import randint, choice
from PIL import Image, ImageDraw, ImageFont

margin = 15
size = 200
incl = set()
with open('mismatched.txt') as data:
    for line in data:
        incl.add(int(line.strip()))
n = len(incl)
w = n * size + (n + 1) * margin
h = size
files = dict()
labels = dict()
for treeID in incl:
    for kind in ['green', 'yellow', 'red', 'leafless']:
        filename = f'ground/individual/squares/aug100_{kind}_{treeID}.png'
        if os.path.exists(filename): 
            files[treeID] = filename
            labels[treeID] = kind
            break
image = Image.new('RGBA', (w, h))
x = margin
from color import pltcol
canvas = ImageDraw.Draw(image)
orig = dict()
offset = 15
lw = 8
font = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", 60, encoding="unic")
# font = ImageFont.load_default()
with open('trees.txt') as data:
    data.readline() # skip header row
    for line in data:
        fields = line.split()
        treeID = int(fields[0])
        orig[treeID] = fields[1]
for treeID in incl:
    sample = Image.open(files[treeID]).resize((size, size)).convert('RGBA')
    image.paste(sample, (x, 0), sample)
    if labels[treeID] != orig[treeID]:
        canvas.rectangle((x, 0, x + size, size), outline = pltcol[labels[treeID]], width = 2 * lw)
        canvas.rectangle((x, 0, x + size, size), outline = pltcol[orig[treeID]], width = lw)
    else:
        canvas.rectangle((x, 0, x + size, size), outline = pltcol[orig[treeID]], width = lw)
    canvas.text((x + 2 * offset, offset), str(treeID), 'black', font = font)
    x += size + margin
image.save('mismatches.png')
