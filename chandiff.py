import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 10})
from collections import defaultdict
from os.path import exists
from PIL import Image
from sys import argv
from math import fabs
import numpy as np
from threshold import values
th = values()

colors = ['#999900', '#990099', '#009999']
tics = [x for x in range(-200, 201, 100)]

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

def diff(image, ax, h, tw = 2, bw = 5): 
    RGBA = np.array(image)
    R = RGBA[:,:,0].flatten()
    G = RGBA[:,:,1].flatten()
    B = RGBA[:,:,2].flatten()
    A = RGBA[:,:,3].flatten()
    norm = 100 / len(R)
    vs = [diffHisto(R, G, A), diffHisto(R, B, A), diffHisto(G, B, A), diffHisto(B, ((R + G) / 2), A), threeWayHisto(R, G, B, A)]
    line = [[th['tr'], th['ty']], [], [], [th['tb']]]
    for j in range(3):
        if sum(vs[j].values()) == 0: # nothing to plot
            ax[j].axis('off')
        else:
            ax[j].text(-240, 0.9 * h, '{:.3f}% exact matches'.format(norm * vs[j][0]))
            ax[j].set_ylim(0, h)            
            for i in range(-255, 255):
                if i == 0:
                    continue
                v = vs[j][i];
                if v > 0:
                    ax[j].bar(i, norm * v, width = bw, color = colors[j], edgecolor = colors[j])
            for l in line[j]:
                ax[j].axvline(l, lw = tw) # indicate thresholds

# based on histogram.py
classes = ['green', 'yellow', 'red', 'leafless']
differences = ['R - G', 'R - B', 'G - B', 'B - (R + G) / 2', 'max. diff.']
dataset = argv[1]
high = {'aug100': 0.008, 'aug90': 0.03, 'jul100': 0.011, 'jul90':  0.017, 'jun60': 0.035}
fig, ax = plt.subplots(nrows = len(classes), ncols = len(differences),
                       figsize=(len(differences) * 3, len(classes) * 3))
row = 0
for kind in classes:
    filename = f'{dataset}_{kind}_circ.png'
    if exists(filename):
        print(dataset, kind)        
        diff(Image.open(filename), ax[row, :], high[dataset])
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
