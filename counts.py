from collections import defaultdict
from PIL import Image
import numpy as np

from color import col2str

repl = {'black': 'background', 'blue': 'leafless'}
skip = ['background']
datasets = ['jun60', 'jul90', 'jul100', 'aug90', 'aug100']
for d in datasets:
     counts = defaultdict(int)
     filename = f'automaton/{d}.png'
     img = Image.open(filename)
     (w, h) = img.size
     total = w * h
     pix = img.load()
     for x in range(w):
          for y in range(h):
               counts[col2str(pix[x, y], False)] += 1
     assert sum(counts.values()) == total
     for s in skip:
          total -= counts[s] 
     for (k, v) in counts.items():
          for (o, r) in repl.items():
               k = k.replace(o, r)
          if k not in skip:
               print(d, k, 100 * v / total)


          


