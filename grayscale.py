import matplotlib.pyplot as plt
from PIL import Image
from sys import argv

plt.rcParams.update({'font.size': 25})

def bars(h, t, ax, c = 'black', a = 0.6):
    g = [100 * (h[i] + h[i + 256] + h[i + 512]) / (3 *  t) for i in range(256)] # channel avg
    for i in range(1, 255): # skip all black that corresponds to transparent background
        if g[i] > 0: 
            ax.bar(i, g[i], width = 1, color = c, edgecolor = c, alpha = a)

# visualize the change in the grayscale tones
dataset = argv[1]
orig = Image.open(f'{dataset}_cropped.png')
w, h = orig.size
t = w * h
fig, ax = plt.subplots(figsize = (14, 7)) 
bars((Image.open(f'{dataset}_cropped.png')).histogram(), t, ax, 'green') # original
bars((Image.open(f'{dataset}_cropped_enhanced.png')).histogram(), t, ax, 'blue') # modified
plt.xlim(0, 255)
plt.xlabel('Tone of gray', fontsize = 40)
plt.ylabel('Percent of pixels', fontsize = 40)
plt.savefig(f'{dataset}_eh.png')

