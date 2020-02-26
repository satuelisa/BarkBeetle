import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import describe

plt.rcParams.update({'font.size': 14})
data = pd.read_csv('trees.dat', sep=' ') # treeID class lon lat diam height NSspan EWspan
print(describe(data['NSspan']))
print(describe(data['EWspan']))
fig, ax = plt.subplots()
data.hist(column='NSspan', bins = 12, grid = False, figsize=(6, 4), color='#00ff00', rwidth = 1, alpha = 0.5, ax  = ax)
data.hist(column='EWspan', bins = 12, grid = False, figsize=(6, 4), color='#0000ff', rwidth = 1, alpha = 0.5, ax = ax)
plt.ylabel('Frequency (absolute)')
plt.xlabel('Tree span (meters)')
plt.yticks([x for x in range(9)])
plt.title('')
m = np.mean((data['NSspan'] + data['EWspan']) / 2)
plt.axvline(m, lw = 3, color = '#ff0000')
plt.savefig('diameter.png',  dpi=150)
print('Mean radius: ', m / 2)

from math import fabs
fig, ax = plt.subplots()
data['diff'] = np.fabs(data['NSspan'] - data['EWspan'])
data.hist(column='diff', bins = 12, grid = False, figsize=(6, 4), color='#009999', rwidth = 1, alpha = 0.5, ax  = ax)
plt.ylabel('Frequency (absolute)')
plt.xlabel('Span difference (meters)')
plt.yticks([x for x in range(5)])
plt.title('')
m = np.mean(data['diff'])
plt.savefig('difference.png',  dpi=150)
print('Mean difference: ', m)

from collections import defaultdict
offsets = defaultdict(dict)
maps = dict()
with open('offsets.txt') as od:
    for line in od:
        fields = line.split()
        f = fields[2]
        maps[f] = open(f'annotations/{f}.annot', 'w')
        offsets[f]['x0'] = int(fields[3])
        offsets[f]['y0'] = int(fields[4])
        offsets[f]['x1'] = int(fields[5])
        offsets[f]['y1'] = int(fields[6])
        offsets[f]['wOrig'] = int(fields[7][1:-1]) # skip ( and ,
        offsets[f]['hOrig'] = int(fields[8][:-1]) # skip )
        offsets[f]['N'] = float(fields[9])
        offsets[f]['S'] = float(fields[10])
        offsets[f]['W'] = float(fields[11])
        offsets[f]['E'] = float(fields[12])
        w = offsets[f]['x1'] - offsets[f]['x0']
        offsets[f]['width'] = w
        h = offsets[f]['y1'] - offsets[f]['y0'] 
        offsets[f]['height'] = h
        print(f'# dim {w} {h}', file = maps[f])

from latlon import lon2x, lat2y
        
with open('trees.tex', 'w') as target:
    print('''\\begin{tabular}{r|c|cc|rrrr}
    {\\bf \\#} & {\\bf Class} & {\\bf Latitude } & {\\bf Longitude } & {\\bf Diameter} & {\\bf Height} & {\\bf N-S } & {\\bf E-W }
    \\\\ \\hline''', file = target)
    # treeID class lon lat diam height NSspan EWspan
    for i, row in data.iterrows():
        treeID =  row.treeID
        lon = row.lon
        lat = row.lat
        label = row.kind
        print(f'{treeID} & {label} & {lon:.14f} & {lat:.14f} & {row.diam:.2f} & {row.height:.1f} & {row.NSspan:.2f} & {row.EWspan:.2f} \\\\', file = target)
        for f in offsets:
            o =  offsets[f]
            x = lon2x(lon, o)
            y = lat2y(lat, o)
            print(x, y)
            if x >= 0 and y >= 0 and x <= o['width'] and y <= o['height']:
                print(treeID, label, x, y, file = maps[f])
    print('\end{tabular}', file = target)
for f in maps:
    with open(f'annotations/{f}.raw') as data:
        o = offsets[f]
        dx = o['x0']
        dy = o['y0']
        for line in data:
            fields = line.split()
            treeID = fields[0]
            label = fields[1]
            x = int(fields[2]) - dx
            y = int(fields[3]) - dy
            # only keep the ones that fall in the zone
            if x > 0 and y > 0 and x <= o['width'] and y <= o['height']: 
                print(treeID, label, x, y, file = maps[f]) 
    maps[f].close()
