import matplotlib.pyplot as plt
import matplotlib.ticker
from PIL import Image, ImageDraw
from math import ceil, log
from sys import argv
import numpy as np

# histogram extraction based on the code at https://pythontic.com/image-processing/pillow/histogram

def getRed(v):
    return '#%02x%02x%02x' % (v, 0, 0)

def getGreen(v):
    return '#%02x%02x%02x' % (0, v, 0)

def getBlue(v):
    return '#%02x%02x%02x' % (0, 0, v)

def getGray(v):
    return '#%02x%02x%02x' % (v, v, v)

def histo(image, ax, ylim, bw = 5, dark = 40, bright = 250, seglen = 256): 
    histogram = image.histogram()
    for start in range(0, len(histogram), seglen):
        for pos in range(dark): # zero out the dark ones until the desired threshold
            histogram[start + pos] = 0
        for pos in range(bright, seglen): # zero out the bright ones until the desired threshold
            histogram[start + pos] = 0
    count = np.count_nonzero(histogram)
    if count == 0: # nothing to plot
        for a in ax:
            a.axis('off')
        return None
    normalizer = 100 / sum(histogram)
    histogram = [h * normalizer for h in histogram] # percentages
    for a in ax:
        a.set_ylim(0, ylim)
        a.set_xlim(dark, bright)
        a.set_xticks([50, 100, 150, 200])
    l = histogram[0:seglen] # red channel
    g = [0] * seglen
    for i in range(dark, bright):
        if l[i] > 0:
            g[i] += l[i]
            ax[0].bar(i, l[i], width = bw, color = getRed(i), edgecolor = getRed(i), alpha = 0.9)
    l = histogram[seglen:(2 * seglen)] # green channel
    for i in range(dark, bright):
        if l[i] > 0:
            g[i] += l[i]        
            ax[1].bar(i, l[i], width = bw, color = getGreen(i), edgecolor = getGreen(i), alpha = 0.9)
    l = histogram[(2 * seglen):] # blue channel
    for i in range(dark, bright):
        if l[i] > 0:
            g[i] += l[i]        
            ax[2].bar(i, l[i], width = bw, color = getBlue(i), edgecolor = getBlue(i), alpha = 0.9)
    for i in range(dark, bright):
        if g[i] > 0: # average over the three channels
            ax[3].bar(i, g[i] / 3, width = bw, color = getGray(i), edgecolor = getGray(i), alpha = 0.9)
    return 

filename = argv[1]
circles = not 'rect' in argv # circles are default, include rect on the command line to obtain rectangles
image = Image.open(filename)
w, h = image.size
classes = ['leafless', 'red', 'yellow', 'green']
channels = ['red channel', 'green channel', 'blue channel', 'grayscale']
GSD = {60: 1.76, 90: 1.96, 100: 2.17} # cm

fig, ax = plt.subplots(nrows = len(classes) + 1, ncols = len(channels),
                       figsize=(len(channels) * 3, (len(classes) + 1) * 2))

# https://stackoverflow.com/questions/25812255/row-and-column-headers-in-matplotlibs-subplots
for a, c in zip(ax[0], channels): # column titles
    a.set_title(c)
for a, c in zip(ax[:, 0], ['enhanced'] + classes): # row titles
    a.set_ylabel(c, rotation = 90, size = 'large')
    
templates = dict()
counts = dict()
for kind in classes:
    templates[kind] = Image.new('RGB', (w, h))
    counts[kind] = 0

dataset = (filename.split('.')[0]).split('_')[0]
print('Characterizing', dataset)
alt = int(dataset[3:]) # omit the first three letters corresponding to jun / jul / aug to get the flight altitude
sample = 5 # m (adjustable parameter referring to a typical tree dimension)
factor = None
d = None
with open('{:s}.map'.format(dataset)) as data:
    for line in data:
        fields = line.split()        
        if '#' in line and factor is None:
            ow = int(fields[4])
            factor = ow // w
            scale = GSD[alt]
            d = int(ceil(((sample * 100) / scale) / 2)) // factor # in pixels
            if circles:
                mask = Image.new("L", (2 * d, 2 * d), 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, 2 * d, 2 * d), fill=255)
                mask.save(f'mask_{d}.png', quality=100)
        elif '#' not in line: # skip other comments
            assert factor is not None
            treeID = int(fields.pop(0))
            if treeID >= 30: # from-image annotations only as the ground-based ones are flight-specific
                kind = fields.pop(0)
                x = int(fields.pop(0)) // factor # center x after resizing
                y = int(fields.pop(0)) // factor # center y after resizing
                counts[kind] += 1
                if circles:
                    templates[kind].paste(image.crop((x - d, y - d, x + d, y + d)), (x - d, y - d), mask)
                else: # rectangle
                    templates[kind].paste(image.crop((x - d, y - d, x + d, y + d)), (x - d, y - d))

high = {'aug100': 3, 'aug90': 2, 'jul100': 6, 'jul90':  6, 'jun60': 5}
histo(image, ax[0, :], high[dataset])
row = 1
which = 'circ' if circles else 'rect'
for kind in classes:
    if counts[kind] > 0:
        im = templates[kind]
        if histo(im, ax[row, :], high[dataset]) is not None:
            im.save(f'{dataset}_{kind}_{which}.png')
    row += 1

#fig.tight_layout()
plt.savefig(f'{dataset}_{which}_histo.png') 
