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
debug = False # mask files are saved in debug mode (to see how round they are)
postprocess = 'post' in argv # whether this is pre- or post-processing

dataset = argv[1]
trees, ow = parse(dataset)
sqr = radius(dataset)
goal = 4*sqr**2
r = sqr // 2
d = 2 * r # must be even
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
    w, h = thresholded.size
    factor = ow / w
    ssqr = radius(dataset, factor)
    sr = ssqr // 2
    sd = 2 * sr # must be even
    sc = (sr, sr, sr + sd, sr + sd)
    smask = Image.new("L", (sd, sd), 0)
    sdraw = ImageDraw.Draw(smask)
    sdraw.ellipse((0, 0, sd, sd), fill = 255)
    sr = sd // 2
    if debug:
        mask.save(f'mask_{sr}.png', quality=100)
for treeID in trees:
    pos, label = trees[treeID]
    x, y = pos
    zone = (x - sqr, y - sqr, x + sqr, y + sqr)
    square = original.crop(zone)
    if goal == np.array(square).any(axis=-1).sum(): # ignore partial samples
        square.save(f'individual/squares/{dataset}_{label}_{treeID}.png')
        w, h = square.size
        assert w == 2 * sqr
        cut(square, d, center, mask, f'individual/original/{dataset}_{label}_{treeID}.png')
        cut(enhanced.crop(zone), d, center, mask, f'individual/enhanced/{dataset}_{label}_{treeID}.png')
        if postprocess:
            sx = int(round(x / factor))
            sy = int(round(y / factor))
            sz = (sx - ssqr, sy - ssqr, sx + ssqr, sy + ssqr)            
            cut(thresholded.crop(sz), sd, sc, smask,
                f'individual/thresholded/{dataset}_{label}_{treeID}.png')                    
            cut(automaton.crop(sz), sd, sc, smask,
                f'individual/automaton/{dataset}_{label}_{treeID}.png')
                        

