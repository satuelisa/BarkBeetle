from PIL import Image
from random import choice
from collections import defaultdict

def colround(filename, tb = 10, tr = 100, tg = 100, ty = 0):
    img = Image.open(filename)
    (w, h) = img.size
    pix = img.load()
    c = 0
    for x in range(w):
        for y in range(h):
            p = pix[x, y]
            r = p[0]
            g = p[1]
            b = p[2]
            a = p[3]
            if a < 255:
                pix[x, y] = (0, 0, 0, 0) # black transparent
            elif b < (r + g) / 2 + tb:
                pix[x, y] = (0, 0, 255, 255) # blue (leafless)
            elif r > tr and g < tg:
                pix[x, y] = (255, 0, 0, 255) # red
            elif r - b > ty:
                pix[x, y] = (255, 255, 0, 255) # yellow
            elif g < tg:
                pix[x, y] = (0, 255, 0, 255) # green
            else:
                pix[x, y] = (0, 0, 0, 0) # black transparent
            c += 1
    img.save(filename.replace('smaller', 'thresholded'))
    return

from sys import argv
import os

for f in os.listdir('.'):
    fn = os.fsdecode(f)
    if fn.endswith('smaller_.png'):
        colround(fn)


        


