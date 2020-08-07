import numpy as np
from sys import argv
from PIL import Image, ImageDraw
from cut import circle, cut
import warnings

# metadata causes this
warnings.simplefilter('ignore', Image.DecompressionBombWarning)

from trees import parse
from gsd import radius
debug = True # mask files are saved in debug mode (to see how round they are)
postprocess = 'post' in argv # whether this is pre- or post-processing
dataset = argv[1]
ground = 'ground' in argv
prefix = 'walk/' if ground else ''
trees, ow = parse(dataset, ground)
r = radius(dataset) // 2 # the cut-out size
d = 2 * r
goal = d**2 # pixel count
margin = d // 10 # margin
mask = circle(d, margin)
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
    cut(square, d, circle(d, margin, opacity = 200), 'test.png')    
    quit()
if postprocess:
    print('Post-processing for manuscript figures', dataset)
    thresholded = Image.open('thresholded/{:s}.png'.format(dataset))
    automaton = Image.open('automaton/{:s}.png'.format(dataset))
    w, h = thresholded.size
    factor = ow / w
    sr = radius(dataset, factor) // 2
    sd = 2 * sr
    smask = circle(sd)
for treeID in trees:
    pos, label = trees[treeID]
    x, y = pos
    zone = (x - r, y - r, x + r, y + r)
    square = original.crop(zone)
    if ground or goal == np.array(square).any(axis=-1).sum(): # ignore partial image-based samples
        square.save(f'{prefix}individual/squares/{label}/{dataset}_{label}_{treeID}.png')
        w, h = square.size
        assert w == d
        cut(square, d, circle(d, margin, opacity = 200), f'{prefix}individual/highlight/{label}/{dataset}_{label}_{treeID}.png')
        cut(square, d, mask, f'{prefix}individual/original/{label}/{dataset}_{label}_{treeID}.png',
            start = margin, end = d - margin)
        cut(enhanced.crop(zone), d, mask, f'{prefix}individual/enhanced/{label}/{dataset}_{label}_{treeID}.png',
            start = margin, end = d - margin)
        if postprocess:
            sx = int(round(x / factor))
            sy = int(round(y / factor))
            sz = (sx - sr, sy - sr, sx + sr, sy + sr)            
            cut(thresholded.crop(sz), sd, smask,
                f'{prefix}individual/thresholded/{label}/{dataset}_{label}_{treeID}.png')                    
            cut(automaton.crop(sz), sd, smask,
                f'{prefix}individual/automaton/{label}/{dataset}_{label}_{treeID}.png')
