import matplotlib.pyplot as plt
from sys import argv, stderr
from math import ceil, floor
from PIL import Image
import numpy as np
import cv2

from gsd import radius

def bars(h, t, ax, c = 'black', a = 0.6):
    g = [100 * (h[i] + h[i + 256] + h[i + 512]) / (3 *  t) for i in range(256)] # channel avg
    for i in range(1, 255): # skip all black that corresponds to transparent background
        if g[i] > 0: 
            ax.bar(i, g[i], width = 1, color = c, edgecolor = c, alpha = a)

dataset = argv[1]
img = Image.open(f'{dataset}_smaller.png') # filename as a command-line argument
imgAr = np.array(img)
(h, w, c) = imgAr.shape
xMin = w
xMax = 0
yMin = h
yMax = 0
factor = None
with open('{:s}.map'.format(dataset)) as data:
    for line in data:
        fields = line.split()
        if '#' in line and factor is None:
            ow = int(fields[4])
            factor = ow / w        
        elif '#' not in line: # skip other comments
            treeID = int(fields.pop(0))
            kind = fields.pop(0)
            x = int(fields.pop(0))
            y = int(fields.pop(0))
            xMin = min(x, xMin)
            xMax = max(x, xMax)
            yMin = min(y, yMin)
            yMax = max(y, yMax)
print('trees located', file = stderr)            
m = 2 * radius(dataset, factor) # a margin to ensure that the border annotations will be complete
xMin = max(xMin - m, 0)
yMin = max(yMin - m, 0)
xMax = max(xMax + m, w)
yMax = max(yMax + m, h)
xMin = int(floor(xMin / factor))
yMin = int(floor(yMin/ factor))
xMax = int(ceil(xMax / factor))
yMax = int(ceil(yMax / factor))
print(dataset, xMin, yMin, factor) # output the offsets and the scaling factor
imgAr = np.array(img.crop((xMin, yMin, xMax, yMax)))
(h, w, c) = imgAr.shape
assert w == xMax - xMin
assert h == yMax - yMin
if c == 4:
    imgAr = np.delete(imgAr, 3, 2) # drop the original alpha channel if present
    print('alpha channel dropped', file = stderr)
print(f'creating a {h}x{w} template', file = stderr)    
a = np.full((h, w), 255, dtype = 'uint8')
threshold = 350 # a darkness threshold below which pixels are made transparent (background) (420 was too high)
for x in range(w): 
    for y in range(h):
        if sum(imgAr[y, x]) < threshold: # discard the shadows / ground
            a[y, x] = 0 # transparent
            imgAr[y, x] = [0, 0, 0] # black
print('ground removed', file = stderr)
avg = np.mean(np.asarray(imgAr), axis = 2)
q = np.quantile(avg[avg > 0], [0.05, 0.50, 0.95]) # ignore black/transparent
low = int(q[0])
med = int(q[1])
high = int(q[2])
cvImg = imgAr[:, :, ::-1].copy() # order as BGR for OpenCV
h, w, ch = cvImg.shape
assert ch == 3
(hue, s, v) = cv2.split(cv2.cvtColor(cvImg, cv2.COLOR_BGR2HSV)) 
brightness = int(np.mean(v)) - med # brightness adjustment
contrast = low - high + 100 # contrast adjustment
saturation = 100 - int(np.mean(s)) # increase saturation to better distinguish tones
hsv = cv2.merge([hue, np.clip(s + saturation, 0, 255), v]) # incorporate adjusted saturation
cvImg = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR) # return to BGR
for x in range(w): # apply brightness and contrast adjustments
    for y in range(h):
        pixel = cvImg[y, x]
        pixel = pixel * ((255 - brightness) / 255) + brightness
        f = (131 * (contrast + 127)) / (127 * (131 - contrast))
        cvImg[y, x] = np.clip(pixel * f + (127 * (1 - f)), 0, 255)
b, g, r = cv2.split(cvImg)
print('adjustments done', file = stderr)
assert b.shape == a.shape and b.dtype == a.dtype
t = w * h
fig, ax = plt.subplots(figsize = (14, 7)) # plot grayscale histograms of original and modified
bars(img.histogram(), t, ax, 'green')
bars((Image.fromarray(cvImg)).histogram(), t, ax, 'blue')
plt.xlim(0, 255)
plt.xlabel('Tone of gray', fontsize = 40)
plt.ylabel('Percent of pixels', fontsize = 40)
plt.savefig(f'{dataset}_eh.png')
print('histogram saved', file = stderr)
RGBA = cv2.merge([b, g, r, a], 4) # add alpha channel
cv2.imwrite(f'{dataset}_enhanced.png', RGBA) # save file
