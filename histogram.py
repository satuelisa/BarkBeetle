import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 24})
from PIL import Image
from sys import argv
import numpy as np

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

def getPurple(v):
    return '#%02x%02x%02x' % (v // 4, v // 3, v // 2)

def getBrown(v):
    return '#%02x%02x%02x' % (v // 4, v // 2, v // 3)

def histo(filename, ax, ylim, bw = 5, tw = 2, dark = 1, bright = 254, seglen = 256): 
    histogram = Image.open(filename).histogram()
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
    l = histogram[(2 * seglen):] # blue channel
    for i in range(dark, bright):
        if l[i] > 0:
            g[i] += l[i]        
            ax[2].bar(i, l[i], width = bw, color = getBlue(i), edgecolor = getBlue(i))
    ax[2].axvline(thresholds['tb'], lw = tw, color = 'r') # the blue threshold used in threshold.py
    for i in range(dark, bright):
        if g[i] > 0: # average over the three channels
            ax[3].bar(i, g[i] / 3, width = bw, color = getGray(i), edgecolor = getGray(i))
    for i in range(dark, bright):
        v = min(histogram[i], histogram[i + seglen], histogram[i + 2 * seglen])
        if v > 0: # minimum over the three channels
            ax[4].bar(i, v, width = bw, color = getBrown(i), edgecolor = getBrown(i))
    for i in range(dark, bright):
        v = max(histogram[i], histogram[i + seglen], histogram[i + 2 * seglen])
        if v > 0: # maximum over the three channels
            ax[5].bar(i, v, width = bw, color = getPurple(i), edgecolor = getPurple(i))
        ax[5].axvline(thresholds['td'], lw = tw, color = 'b') # the darkness threshold used in threshold.py
        ax[5].axvline(thresholds['tl'], lw = tw, color = 'b') # the lightness threshold used in threshold.py            
    return True

dataset = argv[1]
classes = ['green', 'yellow', 'red', 'leafless']
channels = ['red channel', 'green channel', 'blue channel', 'grayscale', 'minimum', 'maximum']

fig, ax = plt.subplots(nrows = len(classes) + 1, ncols = len(channels),
                       figsize=(len(channels) * 6, (len(classes) + 2) * 3))

# https://stackoverflow.com/questions/25812255/row-and-column-headers-in-matplotlibs-subplots
for a, c in zip(ax[0], channels): # column titles
    a.set_title(c)
for a, c in zip(ax[:, 0], ['enhanced'] + classes): # row titles
    a.set_ylabel(c, rotation = 90, size = 'large')

high = dict() # no exceptions

histo(f'composite/enhanced/{dataset}.png', ax[0, :], high.get(dataset, 2.0))
row = 1
for kind in classes:
    if histo(f'composite/enhanced/{dataset}_{kind}.png', ax[row, :], high.get(dataset, 1.5)):
        print(kind, 'present in', dataset)
    row += 1
fig.tight_layout()
plt.savefig(f'histograms/{dataset}.png') 
