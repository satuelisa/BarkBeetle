from collections import defaultdict
from math import floor, sqrt
from PIL import Image
from os import popen # for the GIF
from sys import argv
import warnings

# metadata causes this
warnings.simplefilter('ignore', Image.DecompressionBombWarning)

from trees import parse
from gsd import radius

red = (255, 0, 0, 255)
green = (0, 255, 0, 255)
blue = (0, 0, 255, 255)
yellow = (255, 255, 0, 255)

options = [red, blue, yellow, green]
debug = False
gif = 'gif' in argv

def pick(colors, margin = 1):
    high = max(colors.values()) # max freq
    for o in options:
        if o in colors.keys() and colors[o] >= high - margin:
            return o
    return None # keep the old one

def colfreq(dataset):
    filename = 'thresholded/' + dataset + '.png'    
    img = Image.open(filename)
    (w, h) = img.size
    trees, ow = parse(dataset)
    trees = None # we do not need this here
    factor = ow / w
    rad = int(floor(sqrt(radius(dataset, factor))))
    threshold = int((w * h) / 10000)
    tmp = img.copy() # copy so that the same pixels are blank
    pix = img.load()
    update = tmp.load()
    n = [(dx, dy) for dx in range(-rad, rad + 1) for dy in range(-rad, rad + 1)] # Moore neighborhood
    stable = set()
    iteration = 0
    print(f'# iterating with {rad} radius until less than', threshold, 'pixels change')
    while True:
        changes = 0
        for x in range(w):
            for y in range(h):
                if (x, y) not in stable:
                    p = pix[x, y]
                    if p[3] < 255: # trasparent pixels never change
                        continue
                    c = defaultdict(int)
                    nn = set()
                    for dx, dy in n:
                        nx, ny = x + dx, y + dy
                        if nx >= 0 and nx < w and ny >= 0 and ny < h:
                            pn = pix[nx, ny]
                            if pn[3] == 255: # opaque
                                c[pn] += 1
                                nn.add((nx, ny))
                    repl = pick(c)
                    if repl is not None and p != repl:
                        update[x, y] = repl
                        stable -= nn
                        changes += 1
                    else:
                        stable.add((x, y)) # no change
                        update[x, y] = p
        if changes < threshold:
            img.save(f'automaton/{dataset}.png') # final stage
            if gif: # build an animated GIF with ImageMagick
                popen(f'convert -delay 50 automaton/frames/{dataset}_*.png -loop 0 automaton/{dataset}.gif') 
            return
        pix, update = update, pix # swap
        img, tmp = tmp, img
        print(changes, 'changes')        
        if debug:
            img.show()
            input('Press enter to continue')
        if gif:
            iteration += 1
            frame = f'automaton/frames/{dataset}_{iteration:04}.png'
            img.resize((300, 300)).save(frame)

colfreq(argv[1])
