from PIL import Image
from math import ceil
from sys import argv
import numpy as np

def error(value, current, match, below):
     if match:
          if below:
               if value <= current:
                    return 0
               else:
                    return value - current
          else:
               if value >= current:
                    return current
               else:
                    return current - value
     return 0

# initial guesses from visual inspection of histograms
leafless = 180
green = 0
red = 110
ground = 20
el = 0
eg = 0
es = 0
er = 0
count = 0
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
     for value in B: # blue channel
          el += error(value, leafless, c == 'leafless', False) # train the leafless neuron 
     for value in R - G: # channel difference red vs green
          eg += error(value, green, c == 'green', True) # train the green neuron 
          er += error(value, red, c == 'red', True) # train the red neuron 
     for value in high - low: # max channel versus min channel
          es += error(value, ground, c == 'ground', False) # train the ground neuron
     count += n

print(f'tb {leafless - int(round(el / count))} 1 # B > tb -> leafless') 
print(f'tg {green + int(round(eg / count))} 0 #  R - G < tg -> green') 
print(f'tr {red + int(round(er / count))} 1 # R - G > tr -> red') 
print(f'ts {ground - int(round(es / count))} 0 # dMM < ts -> ground (soil)')



