from sys import argv, stderr
from math import ceil, floor
import numpy as np
import cv2

from gsd import radius

dataset = argv[1]
print('enhancing', dataset, file = stderr)
img = cv2.imread(f'{dataset}_smaller.png')
(h, w, c) = img.shape
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
m = 3 * radius(dataset, factor) # a margin to ensure that the border annotations will be complete
xMin = max(int(floor(xMin / factor)) - m, 0)
yMin = max(int(floor(yMin/ factor)) - m, 0)
xMax = min(int(ceil(xMax / factor)) + m,  w)
yMax = min(int(ceil(yMax / factor)) + m, h)
print(dataset, xMin, yMin, factor) # output the offsets and the scaling factor
img = img[yMin:yMax, xMin:xMax] # crop
cv2.imwrite(f'{dataset}_cropped.png', img) # save cropped version for future use
h, w, ch = img.shape
assert w == xMax - xMin
assert h == yMax - yMin
if ch == 4:
    img = np.delete(img, 3, 2) # drop the original alpha channel if present
    print('alpha channel dropped', file = stderr)
print(f'creating a {h}x{w} template', file = stderr)    
a = np.full((h, w), 255, dtype = 'uint8')
threshold = 350 # a darkness threshold below which pixels are made transparent (background) (420 was too high)
for x in range(w): 
    for y in range(h):
        if sum(img[y, x]) < threshold: # discard the shadows / ground
            a[y, x] = 0 # transparent
            img[y, x] = [0, 0, 0] # black
print('ground removed', file = stderr)
avg = np.mean(np.asarray(img), axis = 2)
q = np.quantile(avg[avg > 0], [0.05, 0.50, 0.95]) # ignore black/transparent
low = int(q[0])
med = int(q[1])
high = int(q[2])
h, w, ch = img.shape
assert ch == 3
(hue, s, v) = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2HSV)) 
brightness = int(np.mean(v)) - med # brightness adjustment
contrast = low - high + 100 # contrast adjustment
saturation = 100 - int(np.mean(s)) # increase saturation to better distinguish tones
hsv = cv2.merge([hue, np.clip(s + saturation, 0, 255), v]) # incorporate adjusted saturation
img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR) # return to BGR
print('applying HSV adjustments', file =  stderr)
for x in range(w): # apply brightness and contrast adjustments
    for y in range(h):
        pixel = img[y, x]
        pixel = pixel * ((255 - brightness) / 255) + brightness
        f = (131 * (contrast + 127)) / (127 * (131 - contrast))
        img[y, x] = np.clip(pixel * f + (127 * (1 - f)), 0, 255)
print('adjustments done', file = stderr)
b, g, r = cv2.split(img)
assert b.shape == a.shape and b.dtype == a.dtype
RGBA = cv2.merge([b, g, r, a], 4) # add alpha channel
cv2.imwrite(f'{dataset}_enhanced.png', RGBA) # save file
