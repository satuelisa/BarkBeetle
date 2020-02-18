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
img = cv2.imread('orthomosaics/{:s}.png'.format(dataset))
with open('annotations/{:s}.map'.format(dataset)) as data:
    for line in data:
        if '#' not in line:
            fields = line.split()
            treeID = int(fields.pop(0))
            label = fields.pop(0)
            x = int(fields.pop(0))
            y = int(fields.pop(0))
            trees.append((treeID, (x, y), label, treeID <= 30))
lw = 20
air = img.copy()
ground = img.copy()
both = img.copy()
offset = int(1.2 * r)
for (tID, tree, label, source) in trees:
    c = color[label]
    (x, y) = tree
    # frames according to target
    if tID <= 30:
        cv2.rectangle(ground, (x - r, y - r), (x + r, y + r), c, lw)
        cv2.rectangle(both, (x - r, y - r), (x + r, y + r), c, lw)
    else:
        cv2.circle(air, tree, r, c, lw)
        cv2.circle(both, tree, r, c, lw)
    # text labels in all three
    lp = (x + offset, y + offset)
    cv2.putText(air, str(tID), lp, cv2.FONT_HERSHEY_SIMPLEX, 5.0, (240, 0, 240, 255), 12)
    cv2.putText(ground, str(tID), lp, cv2.FONT_HERSHEY_SIMPLEX, 5.0, (240, 0, 240, 255), 12)
    cv2.putText(both, str(tID), lp, cv2.FONT_HERSHEY_SIMPLEX, 5.0, (240, 0, 240, 255), 12)                
cv2.imwrite(f'validation/{dataset}_air.png', air)
cv2.imwrite(f'validation/{dataset}_ground.png', ground)
cv2.imwrite(f'validation/{dataset}.png', both)
        
