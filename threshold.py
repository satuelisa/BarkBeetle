from math import fabs
from PIL import Image

def values():
    th = dict()
    with open('thresholds.txt') as data:
        for line in data:
            fields = line.split()
            th[fields[0]] = int(fields[1])
    return th

def threshold(filename, thresholds, outputfile):
    img = Image.open(filename)
    (w, h) = img.size
    pix = img.load()
    for x in range(w):
        for y in range(h):
            p = pix[x, y]
            r = p[0] # red
            g = p[1] # green
            b = p[2] # blue
            a = p[3] # alpha 
            rg = r - g # red minus green
            if a == 255: # completely opaque pixels only
                if b > thresholds['tb']:
                    pix[x, y] = (0, 0, 255, 255) # blue (leafless)
                elif rg >= thresholds['tr']: 
                    pix[x, y] = (255, 0, 0, 255) # red
                elif rg <= thresholds['tg']: 
                    pix[x, y] = (0, 255, 0, 255) # green
                else:
                    pix[x, y] = (255, 255, 0, 255) # yellow
            else:
                pix[x, y] = (0, 0, 0, 0) # transparent (black)
    img.save(outputfile)
    return

if __name__ == '__main__':
    from sys import argv
    dataset = argv[1]
    th = values()
    threshold(f'{dataset}_enhanced.png', th, f'{dataset}_thresholded.png')
    for kind in ['green', 'yellow', 'red', 'leafless']:
        threshold(f'{dataset}_{kind}.png', th, f'{dataset}_thr_{kind}.png')


        


