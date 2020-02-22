from collections import defaultdict
from math import fabs
from PIL import Image
import warnings

# metadata causes this
warnings.simplefilter('ignore', Image.DecompressionBombWarning)

def values(q = None):
    suffix = '' if q is None else f'_{q}'
    th = dict()
    with open(f'thresholds{suffix}.txt') as data:
        for line in data:
            fields = line.split()
            th[fields[0]] = int(fields[1])
    return th

def threshold(dataset = None, kind = None, quantile = None, target = None):
    thresholds = values(quantile)
    filename = f'scaled/enhanced/{dataset}.png' if dataset is not None else f'composite/enhanced/{kind}.png'
    img = Image.open(filename)
    (w, h) = img.size
    pix = img.load()
    if target is None:
        counts = defaultdict(int)
    for x in range(w):
        for y in range(h):
            p = pix[x, y]
            r = p[0] # red
            g = p[1] # green
            b = p[2] # blue
            a = p[3] # alpha 
            rg = r - g 
            rb = r - b 
            gb = g - b
            tone = (r + g + b) / 3
            diff = max(fabs(rg), fabs(rb), fabs(gb))
            if a == 255: # completely opaque pixels only
                if tone < thresholds['td']: # dark
                    if target is not None:
                        pix[x, y] = (0, 0, 0, 0) # shadows
                    else:
                        counts['background'] += 1
                elif b > thresholds['tb']:
                    if target is not None:
                        pix[x, y] = (0, 0, 255, 255) # blue (leafless)
                    else:
                        counts['leafless'] += 1
                elif tone > thresholds['tl']: # light
                    if target is not None:
                        pix[x, y] = (0, 0, 0, 0) # rocks
                    else:
                        counts['background'] += 1
                elif rg < thresholds['tg']:
                    if target is not None:
                        pix[x, y] = (0, 255, 0, 255) # green
                    else:
                        counts['green'] += 1
                elif rg > thresholds['tr']:
                    if target is not None:
                        pix[x, y] = (255, 0, 0, 255) # red
                    else:
                        counts['red'] += 1
                elif diff < thresholds['tm']: # gray
                    if target is not None:
                        pix[x, y] = (0, 0, 0, 0) # ground
                    else:
                        counts['background'] += 1
                else:
                    if target is not None:
                        pix[x, y] = (255, 255, 0, 255) # yellow
                    else:
                        counts['yellow'] += 1
            else:
                pix[x, y] = (0, 0, 0, 0) # transparent (black)
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


