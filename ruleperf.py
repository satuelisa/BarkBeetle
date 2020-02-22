import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from sys import argv
import pandas as pd

from color import pltcol

def text(p):
    return ('%.0f%%' % p) if p >= 25 else ''

start = int(argv[1])
end = int(argv[2]) + 1
step = int(argv[3])
quantiles = [q for q in range(start, end, step)]
print(quantiles)
nq = len(quantiles)
kinds = ['green', 'yellow', 'red', 'leafless']
nk = len(kinds)
measurements = pd.read_csv('ruleperf.txt', sep = ' ', header = None)
measurements.columns = ['kind', 'quantile', 'pixels', 'percentage']

coords = dict()
r, c = 0, 0
for q in quantiles:
    for k in kinds:
        coords[(q / 100, k)] = (c, r)
        c += 1
        if c == nk:
            c = 0
            r += 1
            
plt.rcParams.update({'font.size': 8})
plt.figure(figsize = (nk * 2, nq * 2))
gs = gridspec.GridSpec(nq, nk)
gs.update(wspace = 0.02, hspace = 0.25) 

for label, group in measurements.groupby(['quantile', 'kind']):
    q, k = label
    (c, r) = coords[(q, k)]
    target = plt.subplot(gs[nk * r + c])
    g = group.reset_index()    
    values = g.percentage
    names = g.pixels
    match = g.loc[g.pixels == k]
    highlight = None
    if not match.empty:
        pos = match.index[0]
        highlight = [0] * len(values)
        highlight[pos] += 0.05
    quantile = '{:.2f}'.format(q)
    target.set_title(f'{k} samples ({quantile})')
    slices, texts, at = target.pie(values, labels = names, autopct = text, shadow = False,
                               explode = highlight)
    for s in slices:
        s.set_edgecolor('white')
        s.set_facecolor(pltcol[s.get_label()])
    for t in texts:
        current = t.get_text()
        match = g.loc[g.pixels == current]
        if not match.empty: # present
            m = match.reset_index()
            if m.percentage[0] < 25:
                t.set_text('') # erase
plt.subplots_adjust(left = 0.05, right = 1, top = 0.98, bottom = 0)
plt.savefig('ruleperf.png', dpi = 150)
