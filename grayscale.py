import matplotlib.pyplot as plt
from PIL import Image
from sys import argv
import warnings

# metadata causes this
warnings.simplefilter('ignore', Image.DecompressionBombWarning)

plt.rcParams.update({'font.size': 14})

def bars(h, t, ax, c = 'black', a = 0.6):
    g = [100 * (h[i] + h[i + 256] + h[i + 512]) / (3 *  t) for i in range(256)] # channel avg
    for i in range(1, 255): # skip all black that corresponds to transparent background
        if g[i] > 0: 
            ax.bar(i, g[i], width = 1, color = c, edgecolor = c, alpha = a)

# visualize the change in the grayscale tones
dataset = argv[1]
orig = Image.open(f'orthomosaics/{dataset}.png')
w, h = orig.size
t = w * h
fig, ax = plt.subplots(figsize = (14, 7)) 
bars(orig.histogram(), t, ax, 'green') # original
bars((Image.open(f'enhanced/{dataset}.png')).histogram(), t, ax, 'blue') # modified
plt.xlim(0, 255)
plt.xlabel('Tone of gray', fontsize = 40)
plt.ylabel('Percent of pixels', fontsize = 40)
fig.tight_layout()
plt.savefig(f'histograms/{dataset}_uniform.png')

