from os import popen # for the GIF
from PIL import Image
from collections import defaultdict

red = (255, 0, 0, 255)
green = (0, 255, 0, 255)
blue = (0, 0, 255, 255)
yellow = (255, 255, 0, 255)

options = [blue, yellow, red, green]
debug = False
gif = True

def pick(colors, k):
    high = max(colors.values()) # max freq
    for o in options:
        if o in colors.keys() and colors[o] == high:
            return o
    return None # keep the old one

def colfreq(filename, rad = 2, k = 4):
    dataset = filename.split('_')[0]
    img = Image.open(filename)
    (w, h) = img.size
    threshold = int((w * h) / 10000)
    tmp = img.copy() # copy so that the same pixels are blank
    pix = img.load()
    update = tmp.load()
    n = [(dx, dy) for dx in range(-rad, rad + 1) for dy in range(-rad, rad + 1)] # Moore neighborhood
    stable = set()
    iteration = 0
    print('# iterating until less than', threshold, 'pixels change')
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
                    repl = pick(c, k)
                    if repl is not None and p != repl:
                        update[x, y] = repl
                        stable -= nn
                        changes += 1
                    else:
                        stable.add((x, y)) # no change
                        update[x, y] = p
        if changes < threshold:
            img.save(filename.replace('thresholded', 'automaton'))
            if gif:
                popen(f'convert -delay 50 {dataset}_frame_*.png -loop 0 {dataset}.gif') # requiere ImageMagick
            return
        pix, update = update, pix # swap
        img, tmp = tmp, img
        print(changes, 'changes')        
        if debug:
            img.show()
            input('Press enter to continue')
        if gif:
            iteration += 1
            frame = f'{dataset}_frame_{iteration:04}.png'
            print(frame)
            img.resize((300, 300)).save(frame)

from sys import argv
colfreq(argv[1])
