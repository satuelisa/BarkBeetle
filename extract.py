import os.path
from sys import argv
from PIL import Image, ImageDraw

from gsd import radius

debug = False # mask files are saved in debug mode (to see how round they are)

dataset = argv[1]
sqr = radius(dataset)
r = sqr // 2
d = 2 * r # must be even
m = sqr - 2 * d
center = (r, r, r + d, r + d)
mask = Image.new("L", (d, d), 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0, d, d), fill = 255)
r = d // 2

if debug:
    mask.save(f'mask_{r}.png', quality=100)

print('Extracting', dataset)
with open('{:s}.map'.format(dataset)) as data:
    for line in data:
        fields = line.split()        
        if '#' not in line: # skip other comments
            treeID = int(fields.pop(0))
            if treeID >= 30: # from-image annotations only as the ground-based ones are flight-specific
                kind = fields.pop(0)
                filename = f'{dataset}_{kind}_t{treeID}.png'
                if os.path.exists(filename):
                    x = int(fields.pop(0))
                    y = int(fields.pop(0))
                    square = Image.open(filename)
                    w, h = square.size
                    assert w == 2 * sqr
                    smaller = Image.new('RGBA', (d, d))
                    smaller.paste(square.crop((center)), (0, 0), mask)
                    smaller.save(f'{dataset}_{kind}_s{treeID}.png')
                
