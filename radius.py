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
