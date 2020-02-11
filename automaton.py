from PIL import Image
from random import choice
from collections import defaultdict

def colfreq(filename, rad = 2):
    img = Image.open(filename)
    (w, h) = img.size
    pix = img.load()
    n = [(dx, dy) for dx in range(-rad, rad + 1) for dy in range(-rad, rad + 1)] # Moore neighborhood
    stable = set()
    while True:
        changes = 0
        for x in range(w):
            for y in range(h):
                if (x, y) not in stable:
                    p = pix[x, y]
                    c = defaultdict(int)
                    for dx, dy in n:
                        nx, ny = x + dx, y + dy
                        if nx >= 0 and nx < w and ny >= 0 and ny < h:
                            c[pix[nx, ny]] += 1
                    freq = max(c.values())
                    cands = []
                    for color in c:
                        if c[color] == freq:
                            cands.append(color)
                    if p not in cands: # substitute with most frequent in neighborhood
                        pix[x, y] = choice(cands) # random pick on a draw
                        for dx, dy in n: # re-evaluate the neighbors
                            stable.discard((x + dx, y + dy))
                        changes += 1
                    else:
                        stable.add((x, y))
        if changes == 0:
            img.save(filename.replace('thresholded', 'majority'))
            return 
        print(changes, 'changes')

from sys import argv
colfreq(argv[1])
