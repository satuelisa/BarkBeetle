import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from sys import argv
import pandas as pd
import numpy as np

bound = 40 # at least 40% right
from color import pltcol

def dominatedBy(target, challenger):
    if np.any(np.greater(target, challenger)):
        return False
    return np.any(np.greater(challenger, target))
    
def text(p):
    return ('%.0f%%' % p) if p >= 25 else ''


m = pd.read_csv('ruleperf.txt', sep = ' ', header = None)
m.columns = ['k', 'q', 'pixels', 'perc']
m['q'] = m['q'].astype('category')
m['k'] = m['k'].astype('category')

q = (m.q).cat
kinds = ['green', 'yellow', 'red', 'leafless', 'ground']
nk = len(kinds)

obj = dict()
count = 5
highest = [(None, None)] * count
for level, data in m.groupby('q'):
    evaluation = dict()
    for cl, subset in data.groupby('k'):
        match = subset.loc[subset.pixels == cl]
        evaluation[cl] = next(iter(match.perc), 0)
    obj[level] = [evaluation[cl] for cl in kinds]
    total = sum(obj[level])
    for pos in range(count):
        (score, lvl) = highest[pos]
        if score is None or score < total:
            highest[pos] = (total, level)
            break

chosen = set([h[1] for h in highest])
for q1 in obj:
    nonDom = True
    for q2 in obj:
        if dominatedBy(obj[q1], obj[q2]):
            nonDom = False
            break
    if nonDom and min(obj[q1]) >= bound:
        chosen.add(q1) # pareto-optimal options always enter

coords = dict()
nq = len(chosen)
assert nq > 0 
r, c = 0, 0
for q in sorted(chosen):
    for k in kinds:
        coords[(q, k)] = (c, r)
        c += 1
        if c == nk:
            c = 0
            r += 1
            
plt.rcParams.update({'font.size': 11})
plt.figure(figsize = (round(nk * 2.2), round(nq * 2.2)))
gs = gridspec.GridSpec(nq, nk)
gs.update(wspace = 0.03, hspace = 0.55, top=0.97) 
incl = m.q.isin(chosen)
m = m[incl]
m.reset_index(inplace = True, drop = True)
m.reindex(sorted(list(set(m.q))), columns = ['q'])

for label, group in m.groupby(['q', 'k']):
    q, k = label
    (c, r) = coords[(q, k)]
    target = plt.subplot(gs[nk * r + c])
    g = group.reset_index()
    values = g.perc
    names = g.pixels
    match = g.loc[g.pixels == k]
    highlight = None
    if not match.empty:
        pos = match.index[0]
        highlight = [0] * len(values)
        highlight[pos] += 0.05
    quantile = '{:.2f}'.format(q)
    target.set_title(f'{k} ({quantile})')
    slices, texts, at = target.pie(g.perc, labels = g.pixels, autopct = text, shadow = False,
                               explode = highlight)
    for s in slices:
        s.set_edgecolor('white')
        s.set_facecolor(pltcol[s.get_label()])
    for t in texts:
        current = t.get_text()
        match = g.loc[g.pixels == current]
        if not match.empty: # present
            m = match.reset_index()
            if m.perc[0] < 25:
                t.set_text('') # erase
a = 0.1 / nq
plt.subplots_adjust(left = 0.05, right = 1, top = 1 - a, bottom = 0)
plt.savefig('ruleperf.png', dpi = 150)
low = None
pick = set()
for q in chosen:
    penalty = sum([max(50 - o, 0) for o in obj[q]])
    if low is None or penalty <= low:
        if low is not None and penalty < low:
            pick = set()
        pick.add(q)
        low = penalty

for q in pick:
    print(('{:.2f}'.format(q)).split('.')[1], low)
