import cv2
import color
from sys import argv
from gsd import radius

hl = {
    True: (250, 250, 250, 255),
    False: (20, 20, 20, 255)
}

dataset = argv[1]
filename = f'automaton/{dataset}.png'
result = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
h, w, channels = result.shape
orig = cv2.imread(f'scaled/original/{dataset}.png')
trees = dict()
kind = dict()
with open('annotations/{:s}.map'.format(dataset)) as data:
    for line in data:
        if '#' not in line:
            fields = line.split()
            treeID = int(fields.pop(0))
            if treeID <= 30:
                continue # not the ground annotations
            label = fields.pop(0)
            x = int(fields.pop(0))
            y = int(fields.pop(0))
            trees[treeID] = (x, y)
            kind[treeID] = label
        elif 'Coordinates' in line:
             factor = int(line.split()[4]) / w # scaling factor
lw = 3
step = lw + 1
rc = result.copy()
oc = orig.copy()
r = radius(dataset, factor)
offsetL = r + 4 * step        
margin = r + offsetL + 50
for tID in trees:
    (x, y) = trees[tID]
    x =  int(round(x / factor))
    y =  int(round(y / factor))
    label = kind[tID]
    intended = color.BGR[label]
    present = color.majority(x, y, r, w, h, result)
    match = label in present
    print(dataset, tID, label in present, label, ' '.join(present))
    cv2.circle(rc, (x, y), r, hl[match], lw)
    cv2.circle(oc, (x, y), r, hl[match], lw)            
    cv2.circle(rc, (x, y), r + step, intended, lw)
    cv2.circle(oc, (x, y), r + step, intended, lw)
    i = 2
    for c in present:
        cv2.circle(rc, (x, y), r + i * step, color.BGR[c], lw)
        cv2.circle(oc, (x, y), r + i * step, color.BGR[c], lw)
        i += 1
    cv2.circle(rc, (x, y), r + i * step, hl[match], lw)
    cv2.circle(oc, (x, y), r + i * step, hl[match], lw)
    lp = (x + offsetL, y + offsetL) # label position
    cv2.putText(rc, str(tID), lp, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (240, 0, 240, 255), 2)
    cv2.putText(oc, str(tID), lp, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (240, 0, 240, 255), 2)
cv2.imwrite(f'output/automaton/{dataset}.png', rc)
cv2.imwrite(f'output/original/{dataset}.png', oc)

