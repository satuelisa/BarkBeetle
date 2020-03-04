import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 14})
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

def diffHisto(first, second):
    freq = defaultdict(int)
    n = len(first)
    assert n == len(second) # ensure matching lengths
    for i in range(n):
        f = int(first[i]) # integers instead of unsigned bytes
        s = int(second[i])
        freq[f - s] += 1 # frequencies
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
    A = RGBA[:,:,3].flatten() / 255
    A[A < 1] = 0 # either opaque or transparent
    count = int(np.sum(A))
    assert np.count_nonzero(A) ==  count
    keep = A.nonzero()
    # ignore all transparent pixels
    R = np.take(RGBA[:,:,0].flatten().astype(int), keep)[0]
    G = np.take(RGBA[:,:,1].flatten().astype(int), keep)[0]
    B = np.take(RGBA[:,:,2].flatten().astype(int), keep)[0]
    vs = [diffHisto(R, G), diffHisto(R, B), diffHisto(G, B)]
    line = [[(th['ty'], 'b'), (th['tg'], 'b')], [(th['tm'], 'b')], [(th['tm'], 'b')]] 
    assert len(line) == len(vs) and len(ax) == len(line)
    for j in range(len(vs)):
        n = sum(vs[j].values()) # total frequency
        if n == 0: # nothing to plot
            ax[j].axis('off')
        else:
            norm = 100 / n # as percentages of the total
            ax[j].text(-240, 0.9 * h, '{0:.2}%'.format(norm * vs[j][0]))
            ax[j].set_ylim(0, h)
            for i in range(-255, 255):
                if i == 0:
                    continue # skip these peaks
                v = vs[j][i];
                if v > 0:
                    ax[j].bar(i, norm * v, width = bw, color = colors[j], edgecolor = colors[j])
            for (l, c) in line[j]:
                ax[j].axvline(l, lw = tw, color = c) # illustrate thresholds

classes = ['enhanced', 'green', 'yellow', 'red', 'leafless']
differences = ['R - G', 'B - R', 'B - G'] 
dataset = argv[1]
fig, ax = plt.subplots(nrows = len(classes), ncols = len(differences),
                       figsize=(len(differences) * 4, (len(classes) + 1) * 2))

row = 0 
for kind in classes:
    filename = f'composite/enhanced/{dataset}.png'
    if kind != 'enhanced': # not the whole image
        filename = filename.replace('.png', f'_{kind}.png')
    if exists(filename): # skip empty classes, if any
        diff(filename, ax[row, :], 3 if '_' in filename else 5)
    row += 1

for a, c in zip(ax[0], differences): 
    a.set_title(c)
for a, c in zip(ax[:, 0], classes): 
    a.set_ylabel(c, rotation = 90, size = 'large')
for r in range(len(classes)):
    for c in range(len(differences)):
        a = ax[r, c]
        a.set_xlim(-255, 255)
        a.set_xticks(tics)
plt.tight_layout()
plt.savefig(f'histograms/{dataset}_diff.png') 
