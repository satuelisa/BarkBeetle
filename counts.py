from collections import defaultdict
from PIL import Image
import numpy as np

from color import col2str

m = 150 # margin on the left and the right side
datasets = ['jun60', 'jul90', 'jul100', 'aug90', 'aug100']
o = dict()
p = dict()
c = defaultdict(dict)
w = None
h = dict()

for d in datasets:
     filename = f'automaton/{d}.png'
     img = Image.open(filename)
     (iw, ih) = img.size
     h[d] = ih # slight variation
     if w is None:
          w = iw
     else:
          assert iw == w
     p[d] = img.load()
     o[d] = np.array(Image.open(f'scaled/original/{d}.png'))
     c[d] = defaultdict(int)

goal = w - 2 * m
for y in range(min(h.values())):
     if all([o[d][y, m : (w - m)].any(axis=-1).sum() == goal for d in datasets]):
          # only process the pixels if the row is opaque in all cropped and scaled originals
          for x in range(m, w - m): # iterate over the row (skipping the margins)
               for d in datasets:
                    c[d][col2str(p[d][x, y], False)] += 1

for d in datasets:
     counts = c[d]
     total = sum(counts.values())
     for (k, v) in counts.items():
          print(d, k.replace('blue', 'leafless'), 100 * v / total)
