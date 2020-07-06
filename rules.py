from PIL import Image
from math import ceil
from sys import argv
import numpy as np


datasets = ['jun60', 'jul90', 'jul100', 'aug90', 'aug100']
classes = ['green', 'yellow', 'red', 'leafless', 'ground']
q = float(argv[1])
assert q > 0 and q < 1

tb = [] # others/leafless threshold
tg = [] # green/yellow threshold
tr = [] # red/yellow threshold
tm = [] # monotone threshold for background
for c in classes:
     filename = f'composite/enhanced/{c}.png'
     image = Image.open(filename)
     RGBA = np.array(image)
     dim = RGBA.shape
     if len(dim) < 3 or dim[2] < 4:
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
     low = np.minimum(np.minimum(R, G), B)
     high = np.maximum(np.minimum(R, G), B)
     n = len(R)
     assert n == len(G) and n == len(B)
     dRG = R - G
     dBR = B - G
     dBR = B - R
     dMM = high - low
     if c != 'ground': 
          tm.append(np.quantile(dMM, 1 - q)) # those below are ground
     if c != 'leafless': 
          tb.append(np.quantile(B, q)) # those below are NOT leafless
     if c == 'green':
          tg.append(np.quantile(dRG, q)) # those below are green
     elif c == 'yellow':
          tr.append(np.quantile(dRG, q)) # those below are yellow
print('tb', int(ceil(sum(tb) / len(tb))), '0 #  B < tb are not leafless') # special case: noisy histograms
print('tg', int(ceil(sum(tg) / len(tg))), '0 #  R - G < tg green')
print('ty', int(ceil(sum(tr) / len(tr))), '0 #  R - G < ty yellow')
print('tm', int(ceil(sum(tm) / len(tm))), '0 #  max - min < tm non-transparent')

