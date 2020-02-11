import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 15})
from collections import defaultdict
from os.path import exists
from PIL import Image
from sys import argv
from math import fabs
import numpy as np
from threshold import values
th = values()

colors = ['#999900', '#990099', '#009999', '#0000ff', '#666666']
tics = [x for x in range(-200, 201, 100)]
matchText = True # peaks on matching values

def diffHisto(first, second, alpha):
    freq = defaultdict(int)
    n = len(first)
    assert n == len(second) # ensure matching lengths
    for i in range(n):
        f = int(first[i]) # integers instead of unsigned bytes
        s = int(second[i])
        if alpha[i] == 255: # not transparent
            freq[f - s] += 1 # frequencies
    return freq

def threeWayHisto(first, second, third, alpha, func = max):
    freq = defaultdict(int)
    n = len(first)
    assert n == len(second) and n == len(third)
    for i in range(n):
        f = int(first[i]) # integers instead of unsigned bytes
        s = int(second[i])
        t = int(third[i])
        if alpha[i] == 255: # not transparent
            v = max(fabs(f - s), fabs(f - t), fabs(s - t))
            freq[v] += 1 # frequencies
    return freq

def diff(filename, ax, h, tw = 2, bw = 5):
    image = Image.open(filename)
    RGBA = np.array(image)
    dim = RGBA.shape
    if len(dim) < 3 or dim[2] < 4:
        print('Forcing RGBA on', filename)
        image = image.convert('RGBA')
        image.save(filename)
        RGBA = np.array(image)    
    R = RGBA[:,:,0].flatten()
    G = RGBA[:,:,1].flatten()
    B = RGBA[:,:,2].flatten()
    A = RGBA[:,:,3].flatten()
    vs = [diffHisto(R, G, A), diffHisto(R, B, A), diffHisto(G, B, A)] # , diffHisto(B, ((R + G) / 2), A), threeWayHisto(R, G, B, A)]
    line = [[th['tr'], th['tg']], [], []] #  [], []]
    assert len(line) == len(vs) and len(ax) == len(line)
    for j in range(len(vs)):
        n = sum(vs[j].values()) # total frequency
        if n == 0: # nothing to plot
            ax[j].axis('off')
        else:
            norm = 100 / n # as percentages of the total
            if matchText:
                ax[j].text(-240, 0.9 * h, '{0:.2}% exact'.format(norm * vs[j][0]))
            ax[j].set_ylim(0, h)            
            for i in range(-255, 255):
                if matchText and i == 0: # put the exact matches on a label
                    continue
                v = vs[j][i];
                if v > 0:
                    ax[j].bar(i, norm * v, width = bw, color = colors[j], edgecolor = colors[j])
            for l in line[j]:
                ax[j].axvline(l, lw = tw, color = 'r') # indicate thresholds

classes = ['enhanced', 'green', 'yellow', 'red', 'leafless']
differences = ['R - G', 'R - B', 'G - B'] # , 'B - (R + G) / 2', 'max. diff.']
dataset = argv[1]
fig, ax = plt.subplots(nrows = len(classes), ncols = len(differences),
                       figsize=(len(differences) * 3, (len(classes) + 1) * 2))

row = 0 
for kind in classes:
    filename = f'{dataset}_{kind}.png'
    high = 0.7
    if kind == 'enhanced':
        filename = f'{dataset}_enhanced.png'
        high += 1.8
    if exists(filename): # skip empty classes, if any
        print(dataset, kind)        
        diff(filename, ax[row, :], high)
    row += 1

for a, c in zip(ax[0], differences): 
    a.set_title(c)
for a, c in zip(ax[:, 0], classes): 
    a.set_ylabel(c, rotation = 90, size = 'large')
for r in range(len(classes)):
    for c in range(len(differences)):
        a = ax[r, c]
        a.set_xlim(-270, 270)
        a.set_xticks(tics)
plt.tight_layout()
plt.savefig(f'{dataset}_diff.png') 
