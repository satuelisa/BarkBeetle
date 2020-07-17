from PIL import Image
from math import ceil
from sys import argv
import numpy as np

def accuracy(values, labels, threshold, invert, skiplist = None, wp = 1, wn = 1):
     n = len(values)
     fp = 0
     tp = 0
     fn = 0
     tn = 0
     for i in range(n):
          v = values[i]
          l = labels[i]
          if skiplist is not None and skiplist[i]:
               continue
          if (invert and v > threshold) or (not invert and v < threshold):
               tp += l
               fp += not l
          else:
               fn += l
               tn += not l
     totP = tp + fn
     totN = tn + fp
     ta = tp / totP
     fa = tn / totN
     return (wp * ta + wn * fa) / (wp + wn) # weighted balanced accuracy

def test(values, labels, low = 1, high = 256, step = 1, invert = False, skiplist = None):
     chosen = None
     performance = 0
     for threshold in range(low, high, step):
          current = accuracy(values, labels, threshold, invert, skiplist)
          if current > performance:
               chosen = threshold
               performance = current
     return chosen

def best(values, labels, invert = False, neg = False, skiplist = None, step = 15):
     thr = test(values, labels, low = 1 if not neg else -254, step = step, invert = invert, skiplist = skiplist)
     return test(values, labels,
                 low = max(1 if not neg else -254, thr - step),
                 high = min(thr + step, 255),
                 invert = invert, skiplist = skiplist)
     
vBlue = []
vRG = []
vMM = []
lBlue = []
lGreen = []
lRed = []
lYellow = []
for c in ['green', 'yellow', 'red', 'leafless', 'ground']:
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
     assert np.count_nonzero(A) == count
     keep = A.nonzero()
     # ignore all transparent pixels
     R = np.take(RGBA[:,:,0].flatten().astype(int), keep)[0]
     G = np.take(RGBA[:,:,1].flatten().astype(int), keep)[0]
     B = np.take(RGBA[:,:,2].flatten().astype(int), keep)[0]
     low = np.minimum(np.minimum(R, G), B)
     high = np.maximum(np.minimum(R, G), B)
     n = len(R)
     assert n == len(G) and n == len(B)
     vBlue += B.tolist()
     lBlue += [c == 'leafless'] * n
     if c != 'leafless': # leafless is filtered out first
          vRG += (R - G).tolist()
          lGreen += [c == 'green'] * n
          lRed += [c == 'red'] * n
          if c != 'green' and c != 'red': # green and red are filtered out second and third
               vMM += (high - low).tolist()
               lYellow += [c == 'yellow'] * n

inv = False # <
print(f'tg {best(vRG, lGreen, neg = True)} {1 * inv}')
inv = True # >
print(f'tb {best(vBlue, lBlue, invert = inv)} {1 * inv}') 
print(f'tr {best(vRG, lRed, invert = inv, neg = True, skiplist = lGreen)} {1 * inv}') 
print(f'ty {best(vMM, lYellow, invert = inv)} {1 * inv}')



