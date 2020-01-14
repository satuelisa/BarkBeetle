import matplotlib.pyplot as plt
from PIL import Image
from sys import argv
import numpy as np
import cv2

def bars(h, t, ax, c = 'black', a = 0.6):
    g = [100 * (h[i] + h[i + 256] + h[i + 512]) / (3 *  t) for i in range(256)] # channel avg
    for i in range(1, 255): # skip all black that corresponds to transparent background
        if g[i] > 0: 
            ax.bar(i, g[i], width = 1, color = c, edgecolor = c, alpha = a)

inputFile = argv[1]
img = Image.open(inputFile) # filename as a command-line argument
imgAr = np.array(img)
(w, h, c) = imgAr.shape
print(f'Enhancing a {w} by {h} image...')
if c == 4:
    imgAr = np.delete(imgAr, 3, 2) # drop the original alpha channel if present
    img = Image.fromarray(imgAr)
avg = np.mean(np.asarray(imgAr), axis = 2)
q = np.quantile(avg[avg > 0], [0.05, 0.50, 0.95]) # ignore black/transparent
low = int(q[0])
med = int(q[1])
high = int(q[2])
cvImg = imgAr[:, :, ::-1].copy() # order as BGR for OpenCV
h, w, ch = cvImg.shape
assert ch == 3
a = np.full((h, w), 255, dtype = 'uint8')
(hue, s, v) = cv2.split(cv2.cvtColor(cvImg, cv2.COLOR_BGR2HSV)) 
brightness = int(np.mean(v)) - med # brightness adjustment
contrast = low - high + 180 # contrast adjustment
saturation = 128 - int(np.mean(s)) # increase saturation to better distinguish tones
print(low, med, high, '\tb', brightness, '\tc', contrast, '\ts', saturation)
hsv = cv2.merge([hue, np.clip(s + saturation, 0, 255), v]) # incorporate adjusted saturation
cvImg = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR) # return to BGR
for x in range(w): # apply brightness and contrast adjustments
    for y in range(h):
        pixel = cvImg[y, x]
        s = sum(pixel)
        if s == 0: # black
            a[y, x] = 0 # transparent
        else:
            pixel = pixel * ((255 - brightness) / 255) + brightness
            f = (131 * (contrast + 127)) / (127 * (131 - contrast))
            pixel = np.clip(pixel * f + (127 * (1 - f)), 0, 255)
            cvImg[y, x] = pixel
b, g, r = cv2.split(cvImg)
assert b.shape == a.shape and b.dtype == a.dtype
t = w * h
fig, ax = plt.subplots(figsize = (14, 7)) # plot grayscale histograms of original and modified
bars(img.histogram(), t, ax, 'green')
bars((Image.fromarray(cvImg)).histogram(), t, ax, 'blue')
plt.xlim(0, 255)
plt.xlabel('Tone of gray', fontsize = 40)
plt.ylabel('Percent of pixels', fontsize = 40)
plt.savefig(inputFile.replace('.png', '_eh.png')) 
RGBA = cv2.merge([b, g, r, a], 4) # add alpha channel
cv2.imwrite(inputFile.replace('.png', '_enhanced.png'), RGBA) # save file


    
