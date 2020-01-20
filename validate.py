from math import ceil
from sys import argv
import cv2

# CV2 BGR
# four categories
# red: red, dry
# yellow: yellow, orange
# blue: leafless
# green: green, infested

from gsd import radius

color = {'red': (0, 0, 255, 255), 'green': (0, 255, 0, 255),
         'yellow': (0, 255, 255, 255), 'orange': (0, 255, 255, 255),
         'leafless': (255, 0, 0, 255), 'dry': (0, 0, 255, 255),
         'infested': (0, 255, 0, 255)}

dataset = argv[1]
r = radius(dataset)
trees = []
img = cv2.imread('{:s}.tiff'.format(dataset))
with open('{:s}.map'.format(dataset)) as data:
    for line in data:
        if '#' not in line:
            fields = line.split()
            treeID = int(fields.pop(0))
            label = fields.pop(0)
            x = int(fields.pop(0))
            y = int(fields.pop(0))
            trees.append((treeID, (x, y), label, treeID <= 30))
lw = 20
copy = img.copy()
for (tID, tree, label, expert) in trees:
    c = color[label]
    if expert: # group annotation
        (x, y) = tree
        cv2.rectangle(copy, (x - r, y - r), (x + r, y + r), c, lw)
    else: # image-based annotation
        cv2.circle(copy, tree, r, c, lw)
    cv2.putText(copy, str(tID), tree, cv2.FONT_HERSHEY_SIMPLEX, 4.0, (240, 0, 240, 255), 8)                
cv2.imwrite(f'{dataset}_validation.png', copy)
        
