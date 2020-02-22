import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import pandas as pd

from color import pltcol

def text(p):
    return ('%.0f%%' % p) if p >= 15 else ''

datasets = ['jun60', 'jul90', 'jul100', 'aug90', 'aug100']
n = len(datasets)
measurements = pd.read_csv('coverage.txt', sep = ' ', header = None)
measurements.columns = ['dataset',  'pixels', 'percentage']
full = {'jun60': 'June 60 m',
        'jul90': 'July 90 m',
        'jul100': 'July 100 m',
        'aug90': 'August 90 m',
        'aug100': 'August 100 m'}

plt.rcParams.update({'font.size': 9})
plt.figure(figsize = (2 * n, 2))
gs = gridspec.GridSpec(1, n)
gs.update(wspace = 0.02, hspace = 0.2)

for label, data in measurements.groupby(['dataset']):
    target = plt.subplot(gs[datasets.index(label)])
    d = data.reset_index()    
    values = d.percentage
    names = d.pixels
    target.set_title(full[label])
    slices, texts, at = target.pie(values, labels = names, autopct = text, shadow = False)
    for s in slices:
        s.set_edgecolor('white')
        s.set_facecolor(pltcol[s.get_label()])
    for t in texts:
        current = t.get_text()
        match = d.loc[d.pixels == current]
        if not match.empty: # present
            m = match.reset_index()
            if m.percentage[0] < 5:
                t.set_text('') # erase
plt.subplots_adjust(left = 0, right = 0.95, top = 0.85, bottom = 0.05)
plt.savefig('coverage.png', dpi = 150)
