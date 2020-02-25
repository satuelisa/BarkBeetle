from PIL import Image
from math import ceil
from sys import argv
import numpy as np


datasets = ['jun60', 'jul90', 'jul100', 'aug90', 'aug100']
classes = ['green', 'yellow', 'red', 'leafless']
q = float(argv[1])
assert q > 0 and q < 1

tb = [] # others/leafless threshold
tg = [] # green/yellow threshold
tr = [] # red/yellow threshold
tl = [] # lightness threshold for background
td = [] # darkness threshold for background
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
     n = len(R)
     assert n == len(G) and n == len(B)
     dRG = R - G
     dBR = B - G
     dBR = B - R
     grayscale = (R + B + G) / 3
     comb = np.concatenate([np.abs(dRG), np.abs(dBR), np.abs(dRG)])
     monotone = np.max(comb.reshape(3, n), axis = 0) 
     assert len(monotone) == n
     tl.append(np.quantile(grayscale, q)) # lightness, those below are ok
     td.append(np.quantile(grayscale, 1 - q)) # darkness, those _above_ are ok
     tm.append(np.quantile(monotone, 1 - q)) # grayness, those _above_ are ok
     if c != 'leafless':
          tb.append(np.quantile(B, q)) # those below are NOT leafless
     if c == 'green':
          tg.append(np.quantile(dRG, q)) # those below are green
     elif c == 'yellow':
          tr.append(np.quantile(dRG, q)) # those below are yellow
print('tb', int(ceil(sum(tb) / len(tb))), '0 #  B < tb are not leafless') # special case: noisy histograms
print('tg', int(ceil(sum(tg) / len(tg))), '0 #  R - G < tg green')
print('ty', int(ceil(sum(tr) / len(tr))), '0 #  R - G < ty yellow')
print('tm', int(ceil(sum(tm) / len(tm))), '1 #  diff > tm non-transparent')
print('td', int(ceil(sum(td) / len(td))), '1 #  tone > td non-transparent')
print('tl', int(ceil(sum(tl) / len(tl))), '0 #  tone < tl non-transparent')

