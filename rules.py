from PIL import Image
from math import ceil
import numpy as np

datasets = ['jun60', 'jul90', 'jul100', 'aug90', 'aug100']
classes = ['green', 'yellow', 'red', 'leafless']
cutoff = 0.975

tb = [] # others/leafless threshold
tg = [] # green/yellow threshold
tr = [] # red/yellow threshold
tl = [] # lightness threshold for background
td = [] # darkness threshold for background
tm = [] # monotone threshold for background
for c in classes:
    for d in datasets:
        filename = f'composite/enhanced/{d}_{c}.png'
        image = Image.open(filename)
        RGBA = np.array(image)
        dim = RGBA.shape
        if len(dim) < 3 or dim[2] < 4:
            print('Forcing RGBA on', filename)
            image = image.convert('RGBA')
            image.save(filename)
            RGBA = np.array(image)
        A = RGBA[:,:,3].flatten() / 255
        A[A < 1] = 0 # either opaque or transparent
        count = int(np.sum(A))
        assert np.count_nonzero(A) ==  count
        keep = A.nonzero()
        # ignore all transparent pixels
        R = np.take(RGBA[:,:,0].flatten().astype(int), keep)[0]
        G = np.take(RGBA[:,:,1].flatten().astype(int), keep)[0]
        B = np.take(RGBA[:,:,2].flatten().astype(int), keep)[0]
        n = len(R)
        assert n == len(G) and n == len(B)
        dRG = R - G
        dBR = B - G
        dBR = B - R
        grayscale = (R + B + G) / 3
        comb = np.concatenate([np.abs(dRG), np.abs(dBR), np.abs(dRG)])
        monotone = 255 - np.max(comb.reshape(3, n), axis = 0)
        assert len(monotone) == n
        tl.append(np.quantile(grayscale, cutoff))
        td.append(np.quantile(255 - grayscale, cutoff))
        tm.append(np.quantile(monotone, cutoff))
        if c != 'leafless':
            tb.append(np.quantile(B, cutoff))
        if c == 'green':
            tg.append(np.quantile(dRG, cutoff)            )
        elif c == 'yellow':
            tr.append(np.quantile(dRG, cutoff)            ) 
print('tb', int(ceil(sum(tb) / len(tb))), '# pixels with B > tb are made blue')
print('tg', int(ceil(sum(tg) / len(tg))), '# pixels with R - G < tg are made green')
print('tr', int(ceil(sum(tr) / len(tr))), '# pixels with R - G > tr are made red')
print('tm', 255 - int(ceil(sum(tm) / len(tm))), '# pixels with max diff in RGB < tm are made transparent')
print('td', 255 - int(ceil(sum(td) / len(td))), '# pixels with tone < td are made transparent')
print('tl', int(ceil(sum(tl) / len(tl))), '# pixels with tone > tl are made transparent')

