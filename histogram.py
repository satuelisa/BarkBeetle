import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 14})
from PIL import Image, ImageDraw
from math import ceil, log
from sys import argv
import numpy as np

from gsd import radius
from threshold import values
thresholds = values()

# histogram extraction based on the code at https://pythontic.com/image-processing/pillow/histogram

def getRed(v):
    return '#%02x%02x%02x' % (v, 0, 0)

def getGreen(v):
    return '#%02x%02x%02x' % (0, v, 0)

def getBlue(v):
    return '#%02x%02x%02x' % (0, 0, v)

def getGray(v):
    return '#%02x%02x%02x' % (v, v, v)

def histo(image, ax, ylim, bw = 5, tw = 2, dark = 1, bright = 254, seglen = 256): 
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
        return False
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
            ax[0].bar(i, l[i], width = bw, color = getRed(i), edgecolor = getRed(i))
    l = histogram[seglen:(2 * seglen)] # green channel
    for i in range(dark, bright):
        if l[i] > 0:
            g[i] += l[i]        
            ax[1].bar(i, l[i], width = bw, color = getGreen(i), edgecolor = getGreen(i))
    ax[1].axvline(thresholds['tg'], lw = tw) # illustrate the green threshold used in threshold.py            
    l = histogram[(2 * seglen):] # blue channel
    for i in range(dark, bright):
        if l[i] > 0:
            g[i] += l[i]        
            ax[2].bar(i, l[i], width = bw, color = getBlue(i), edgecolor = getBlue(i))            
    for i in range(dark, bright):
        if g[i] > 0: # average over the three channels
            ax[3].bar(i, g[i] / 3, width = bw, color = getGray(i), edgecolor = getGray(i))
    for i in range(dark, bright):
        v = min(histogram[i], histogram[i + seglen], histogram[i + 2 * seglen])
        if v > 0: # minimum over the three channels
            ax[4].bar(i, v, width = bw, color = '#996633', edgecolor = '#996633')
    ax[4].axvline(thresholds['tl'], lw = tw) # illustrate the lightness threshold used in threshold.py
    for i in range(dark, bright):
        v = max(histogram[i], histogram[i + seglen], histogram[i + 2 * seglen])
        if v > 0: # maximum over the three channels
            ax[5].bar(i, v, width = bw, color = '#663399', edgecolor = '#663399')
    return True

dataset = argv[1]
image = Image.open(f'{dataset}_enhanced.png')
classes = ['green', 'yellow', 'red', 'leafless']
channels = ['red channel', 'green channel', 'blue channel', 'grayscale', 'minimum', 'maximum']

fig, ax = plt.subplots(nrows = len(classes) + 1, ncols = len(channels),
                       figsize=(len(channels) * 3, (len(classes) + 1) * 2))

# https://stackoverflow.com/questions/25812255/row-and-column-headers-in-matplotlibs-subplots
for a, c in zip(ax[0], channels): # column titles
    a.set_title(c)
for a, c in zip(ax[:, 0], ['enhanced'] + classes): # row titles
    a.set_ylabel(c, rotation = 90, size = 'large')

templates = dict() # store the cut-out versions of the enhanced images
originals = dict() # for comparison, also cut out the same regions of the original orthomosaics
ofn =  f'{dataset}_smaller.png'
orig = Image.open(ofn)
w, h = orig.size # possibly larger of the two

counts = dict() 
for kind in classes:
    templates[kind] = Image.new('RGB', (w, h))
    originals[kind] = Image.new('RGB', (w, h))
    counts[kind] = 0

offsetX = None
offsetY = None
factor = None
with open('offsets.txt') as data:
    for line in data:
        fields = line.split()
        if fields[0] == dataset: # do NOT break, use the LAST value (the file gets appended)
            offsetX = int(fields[1])
            offsetY = int(fields[2])
            factor = float(fields[3])
assert offsetX is not None

r = radius(dataset, factor)
mask = Image.new("L", (2 * r, 2 * r), 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0, 2 * r, 2 * r), fill = 255)
# mask.save(f'mask_{r}.png', quality=100)

print('Extracting and analyzing', dataset)
with open('{:s}.map'.format(dataset)) as data:
    for line in data:
        fields = line.split()        
        if '#' not in line: # skip other comments
            assert factor is not None
            treeID = int(fields.pop(0))
            if treeID >= 30: # from-image annotations only as the ground-based ones are flight-specific
                kind = fields.pop(0)
                x = round(int(fields.pop(0)) / factor) # center x after resizing
                y = round(int(fields.pop(0)) / factor) # center y after resizing
                xe = x - offsetX # the enhanced version was cropped
                ye = y - offsetY # also vertically
                counts[kind] += 1
                pos = (x, y)
                templates[kind].paste(image.crop((xe - r, ye - r, xe + r, ye + r)), pos, mask)
                originals[kind].paste(orig.crop((x - r, y - r, x + r, y + r)), pos, mask)

high = {'aug100': 3, 'aug90': 2, 'jul100': 5, 'jul90':  4, 'jun60': 4}
histo(image, ax[0, :], high[dataset])
row = 1
for kind in classes:
    if counts[kind] > 0:
        im = templates[kind]
        if histo(im, ax[row, :], high[dataset]):
            print(kind)
            im.save(f'{dataset}_{kind}.png')
            originals[kind].save(f'{dataset}_orig_{kind}.png')
    row += 1
fig.tight_layout()
plt.savefig(f'{dataset}_histo.png') 
