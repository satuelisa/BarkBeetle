from math import ceil, floor, sqrt
from PIL import Image
import numpy as np
import colorsys

# sorting from https://www.alanzucconi.com/2015/09/30/colour-sorting/
def step (pixel, rep = 8):
    r, g, b, a = pixel
    lum = sqrt( .241 * r + .691 * g + .068 * b )
    h, s, v = colorsys.rgb_to_hsv(r,g,b)
    h2 = int(h * rep)
    lum2 = int(lum * rep)
    v2 = int(v * rep)
    if h2 % 2 == 1:
        v2 = rep - v2
    lum = rep - lum
    return (h2, lum, v2)

def save(a, filename, size = 800):
    a = np.array(sorted(a, key = lambda pixel: step(pixel)))
    n = a.shape[0]
    k = int(ceil(sqrt(n)))
    g = 1.168
    h = int(ceil(sqrt(n / g)))
    w = int(ceil(n / h))
    d = w * h - n
    assert not d < 0
    if d > 0: # pad
        a = np.concatenate((a, np.repeat(0, 4 * d).reshape(d, 4)), axis = 0)
    img = Image.fromarray(np.uint8(a).reshape(w, h, 4), 'RGBA')
    print(f'{w}x{h} {filename}')
    img.save(filename)
    return

classes = ['green', 'yellow', 'red', 'leafless', 'ground']
datasets = ['jun60', 'jul90', 'jul100', 'aug90', 'aug100'] 

for case in ['original', 'enhanced', 'thresholded']:
    pixels = dict()
    for kind in classes:
        for dataset in datasets:
            filename = f'composite/{case}/{dataset}_{kind}.png'
            image = Image.open(filename)
            a = np.array(image)
            if len(a.shape) < 3 or a.shape[2]  != 4:
                print('Forcing RGBA on', dataset, case, kind)
                image = image.convert('RGBA')
                image.save(filename)
                a = np.array(image)    
            a = a[a[:,:,3] > 0] # non-transparent pixels only        
            pixels[kind] = np.concatenate((pixels[kind], a), axis = 0) if kind in pixels else a
        save(pixels[kind], f'collages/{case}/{kind}.png')
    
            
