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

from trees import parse
from gsd import radius
debug = True # mask files are saved in debug mode (to see how round they are)
postprocess = 'post' in argv # whether this is pre- or post-processing
dataset = argv[1]
ground = 'ground' in argv
prefix = 'walk/' if ground else ''
trees, ow = parse(dataset, ground)
r = radius(dataset) // 2 # the cut-out will measure 2 * r per side
d = 2 * r
goal = d**2 # pixel count
center = (0, 0, d, d)
mask = Image.new("L", (d, d), 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0, d, d), fill = 255)
if debug:
    mask.save(f'mask_{r}.png', quality=100)
original = Image.open('cropped/{:s}.png'.format(dataset))
enhanced = Image.open('enhanced/{:s}.png'.format(dataset))
if 'test' in argv:
    with open('offsets.txt') as od:
        for line in od:
            fields = line.split()
            f = fields[2]
            if f == dataset:
                x0 = int(fields[3])
                y0 = int(fields[4])
    x = int(input('X: ')) - x0
    y = int(input('Y: ')) - y0
    zone = (x - r, y - r, x + r, y + r)
    print(f'Extracting a {2 * r} square at {x}, {y}')
    square = original.crop(zone)    
    square.save(f'test.png')
    quit()
if postprocess:
    print('Post-processing for manuscript figures', dataset)
    thresholded = Image.open('thresholded/{:s}.png'.format(dataset))
    automaton = Image.open('automaton/{:s}.png'.format(dataset))
    w, h = thresholded.size
    factor = ow / w
    sr = radius(dataset, factor) // 2
    sd = 2 * sr
    sc = (0, 0, sd, sd)
    smask = Image.new("L", (sd, sd), 0)
    sdraw = ImageDraw.Draw(smask)
    sdraw.ellipse((0, 0, sd, sd), fill = 255)
    if debug:
        mask.save(f'mask_{sr}.png', quality=100)
for treeID in trees:
    pos, label = trees[treeID]
    x, y = pos
    zone = (x - r, y - r, x + r, y + r)
    square = original.crop(zone)
    if ground or goal == np.array(square).any(axis=-1).sum(): # ignore partial image-based samples
        square.save(f'{prefix}individual/squares/{label}/{dataset}_{label}_{treeID}.png')
        w, h = square.size
        assert w == d
        cut(square, d, center, mask, f'{prefix}individual/original/{label}/{dataset}_{label}_{treeID}.png')
        cut(enhanced.crop(zone), d, center, mask, f'{prefix}individual/enhanced/{label}/{dataset}_{label}_{treeID}.png')
        if postprocess:
            sx = int(round(x / factor))
            sy = int(round(y / factor))
            sz = (sx - sr, sy - sr, sx + sr, sy + sr)            
            cut(thresholded.crop(sz), sd, sc, smask,
                f'{prefix}individual/thresholded/{label}/{dataset}_{label}_{treeID}.png')                    
            cut(automaton.crop(sz), sd, sc, smask,
                f'{prefix}individual/automaton/{label}/{dataset}_{label}_{treeID}.png')
