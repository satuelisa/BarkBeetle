from math import fabs
from PIL import Image

def values():
    th = dict()
    with open('thresholds.txt') as data:
        for line in data:
            fields = line.split()
            th[fields[0]] = int(fields[1])
    return th

def threshold(filename, thresholds):
    img = Image.open(filename)
    (w, h) = img.size
    pix = img.load()
    for x in range(w):
        for y in range(h):
            p = pix[x, y]
            r = p[0] # red
            g = p[1] # green
            b = p[2] # blue
            a = p[3] # alpha (transparency)
            d = [fabs(r - g), fabs(r - b), fabs(g - b)] # differences
            light = min(r, g, b) # light if this is a high value
            dark = max(r, g, b) # dark if this is a low value
            gray = max(d) # gray-scale if this is a low value
            if a < 255 or dark < thresholds['td']:
                pix[x, y] = (0, 0, 0, 0) # transparent or dark -> transparent
            elif b - (r + g) / 2 > thresholds['tb'] or light > thresholds['tl']: # cf. diff. & grayscale histogram
                pix[x, y] = (0, 0, 255, 255) # blue (leafless); incl. very light pixels
            elif gray < thresholds['tn']: # cf. maximum histogram
                pix[x, y] = (0, 0, 0, 0) # gray pixels -> transparent (neutral)
            elif r - g > thresholds['tr']: # cf. diff. histograms
                pix[x, y] = (255, 0, 0, 255) # red                
            elif r - g > thresholds['ty']: # cf. diff. histograms
                pix[x, y] = (255, 255, 0, 255) # yellow
            elif g > thresholds['tg']: # cf. green-channel histograms
                pix[x, y] = (0, 255, 0, 255) # green
            else:
                pix[x, y] = (0, 0, 0, 0) # black transparent
    img.save(filename.replace('smaller', 'thresholded'))
    return

if __name__ == '__main__':
    from sys import argv
    dataset = argv[1]
    threshold(f'{dataset}_smaller.png', values())


        


