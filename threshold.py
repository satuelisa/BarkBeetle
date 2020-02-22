from collections import defaultdict
from math import fabs
from PIL import Image
import warnings

# metadata causes this
warnings.simplefilter('ignore', Image.DecompressionBombWarning)

def values(q = None, plain = True):
    suffix = '' if q is None else f'_{q}'
    th = dict()
    with open(f'thresholds{suffix}.txt') as data:
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

def threshold(dataset = None, kind = None, quantile = None, target = None):
    thresholds = values(quantile, plain = False)
    filename = f'scaled/enhanced/{dataset}.png' if dataset is not None else f'composite/enhanced/{kind}.png'
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
                        pix[x, y] = (0, 0, 0, 0) # black (background)
                    else:
                        counts['black'] += 1

    if target is not None:
        img.save(target)
    else:
        total = w * h
        for (k, v) in counts.items():
            print(kind, '0.' + quantile, k, 100 * v / total)
    return

if __name__ == '__main__':
    from sys import argv
    data = argv[1]
    q = None
    try:
        q = argv[2]
    except:
        pass
    t = None if q is not None else f'thresholded/{data}.png'
    if data in ['jun60', 'jul90', 'jul100', 'aug90', 'aug100']:
        assert q is None
        threshold(dataset = data, target = t)
    elif data in ['green', 'yellow', 'red', 'leafless']:
        assert q is not None
        threshold(kind = data, quantile = q)
    else:
        print('Unknown data source', data)


