from collections import defaultdict
from math import fabs
from PIL import Image
import warnings

# metadata causes this
warnings.simplefilter('ignore', Image.DecompressionBombWarning)

def values(q = None, plain = True):
    source = 'thresholds' if q is None else f'thresholds/thr_{q}'
    th = dict()
    with open(f'{source}.txt') as data:
        for line in data:
            fields = line.split()
            key = fields[0]
            value = int(fields[1])
            if plain:
                th[key] = value
            else:
                th[key] = (value, '1' in fields[2])
    return th

def accept(value, criterion):
    (limit, invert) = criterion
    if invert:
        return limit < value
    else:
        return value < limit

def threshold(thresholds, source, target = None):
    filename = f'scaled/enhanced/{source}.png' if target is not None else f'composite/enhanced/{source}.png'
    img = Image.open(filename)
    (w, h) = img.size
    pix = img.load()
    if target is None:
        counts = defaultdict(int)
    for x in range(w):
        for y in range(h):
            p = pix[x, y]
            a = p[3] # alpha
            if a == 255: # completely opaque pixels only
                r = p[0] # red
                g = p[1] # green
                b = p[2] # blue
                rg = r - g
                tone = (r + g + b) / 3
                notTooDark = accept(tone, thresholds['td']) # accept higher
                notTooLight = accept(tone, thresholds['tl']) # accept lower
                diff = max(fabs(rg), fabs(r - b), fabs(g - b))
                notTooGray = accept(diff, thresholds['tm']) # accept higher
                if notTooLight and notTooDark and notTooGray:
                    if accept(b, thresholds['tb']): # not leafless (accept lower)               
                        if accept(rg, thresholds['tg']): # accept lower
                            if target is not None:
                                pix[x, y] = (0, 255, 0, 255) # green (do this before yellow)
                            else:
                                counts['green'] += 1
                        elif accept(rg, thresholds['ty']): # accept lower
                            if target is not None:
                                pix[x, y] = (255, 255, 0, 255) # yellow (do this after green)
                            else:
                                counts['yellow'] += 1
                        else:
                            if target is not None:
                                pix[x, y] = (255, 0, 0, 255) # red
                            else:
                                counts['red'] += 1                            
                    else: # leafless
                        if target is not None:
                            pix[x, y] = (0, 0, 255, 255) # blue (leafless)
                        else:
                            counts['leafless'] += 1
                else: # not likely to be a sample pixel
                    if target is not None:
                        pix[x, y] = (0, 0, 0, 0) # background
                    else:
                        counts['bg'] += 1

    if target is not None:
        img.save(target)
        return
    else:
        return counts

kinds = ['green', 'yellow', 'red', 'leafless']
if __name__ == '__main__':
    from sys import argv
    data = argv[1]
    if len(argv) > 2:
        q = argv[2]
        v = values(q, plain = False)
        if data in kinds:
            counts = threshold(v, source = data)
            total = sum(counts.values()) 
            for (k, v) in counts.items():
                print(data, '0.' + q, k, 100 * v / total)
    else:
        threshold(values(q = None, plain = False), source = data, target = f'thresholded/{data}.png')



