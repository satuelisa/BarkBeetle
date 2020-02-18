import numpy as np
from sys import argv
from PIL import Image, ImageDraw
import warnings

# metadata causes this
warnings.simplefilter('ignore', Image.DecompressionBombWarning)

def cut(square, d, center, mask, target):
    circle = Image.new('RGBA', (d, d))
    circle.paste(square.crop((center)), (0, 0), mask)
    circle.save(target)

from gsd import radius
debug = False # mask files are saved in debug mode (to see how round they are)
postprocess = 'post' in argv # whether this is pre- or post-processing

dataset = argv[1]
sqr = radius(dataset)
goal = 4*sqr**2
r = sqr // 2
d = 2 * r # must be even
m = sqr - 2 * d
center = (r, r, r + d, r + d)
mask = Image.new("L", (d, d), 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0, d, d), fill = 255)
r = d // 2
original = Image.open('orthomosaics/{:s}.png'.format(dataset))
enhanced = Image.open('enhanced/{:s}.png'.format(dataset))
if postprocess:
    print('Post-processing', dataset)
    thresholded = Image.open('thresholded/{:s}.png'.format(dataset))
    automaton = Image.open('automaton/{:s}.png'.format(dataset))
if debug:
    mask.save(f'mask_{r}.png', quality=100)
with open('annotations/{:s}.map'.format(dataset)) as data:
    for line in data:
        if '#' not in line:
            fields = line.split()
            treeID = int(fields.pop(0))
            if treeID > 30:
                label = fields.pop(0)
                x = int(fields.pop(0))
                y = int(fields.pop(0))
                zone = (x - sqr, y - sqr, x + sqr, y + sqr)
                square = original.crop(zone)
                if goal == np.array(square).any(axis=-1).sum(): # ignore partial samples
                    square.save(f'individual/squares/{dataset}_{label}_{treeID}.png')
                    w, h = square.size
                    assert w == 2 * sqr
                    cut(square, d, center, mask, f'individual/original/{dataset}_{label}_{treeID}.png')
                    cut(enhanced.crop(zone), d, center, mask, f'individual/circles/{dataset}_{label}_{treeID}.png')
                    if postprocess:
                        cut(thresholded.crop(zone), d, center, mask,
                            f'individual/thresholded/{dataset}_{label}_{treeID}.png')                    
                        cut(automaton.crop(zone), d, center, mask,
                            f'individual/automaton/{dataset}_{label}_{treeID}.png')
                        

