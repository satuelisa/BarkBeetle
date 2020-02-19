import cv2
import color
from sys import argv
from gsd import radius

hl = {
    True: (250, 250, 250, 255),
    False: (20, 20, 20, 255)
}

ground = 'ground' in argv
dataset = argv[1]
orig = cv2.imread(f'scaled/original/{dataset}.png', cv2.IMREAD_UNCHANGED)
thr = cv2.imread(f'thresholded/{dataset}.png', cv2.IMREAD_UNCHANGED)
result = cv2.imread(f'automaton/{dataset}.png', cv2.IMREAD_UNCHANGED)
h, w, channels = result.shape
trees = dict()
kind = dict()
relabel = {'red': 'red', 'dry': 'red',
           'leafless': 'leafless',
           'green': 'green', 'infested': 'green',
           'yellow': 'yellow', 'orange': 'yellow'}
with open('annotations/{:s}.map'.format(dataset)) as data:
    for line in data:
        if '#' not in line:
            fields = line.split()
            treeID = int(fields.pop(0))
            if ground and treeID > 30:
                continue
            elif not ground and treeID <= 30:
                continue
            label = relabel[fields.pop(0)]
            x = int(fields.pop(0))
            y = int(fields.pop(0))
            trees[treeID] = (x, y)
            kind[treeID] = label
        elif 'Coordinates' in line:
             factor = int(line.split()[4]) / w # scaling factor
lw = 3
step = lw + 1
names = ['automaton', 'original', 'thresholded']
targets = [result.copy(), orig.copy(), thr.copy()]
r = radius(dataset, factor)
offsetL = r + 4 * step        
margin = r + offsetL + 50
target = 'ground' if ground else 'air'
for tID in trees:
    (x, y) = trees[tID]
    x =  int(round(x / factor))
    y =  int(round(y / factor))
    label = kind[tID]
    intended = color.BGR[label]
    present = color.majority(x, y, r, w, h, result)
    match = label in present
    print(dataset, tID, label in present, label, ' '.join(present))
    for t in targets:
        cv2.circle(t, (x, y), r, hl[match], lw)
        cv2.circle(t, (x, y), r + step, intended, lw)
    i = 2
    for c in present:
        for t in targets:
            cv2.circle(t, (x, y), r + i * step, color.BGR[c], lw)
        i += 1
    for t in targets:
        cv2.circle(t, (x, y), r + i * step, hl[match], lw)
    lp = (x + offsetL, y + offsetL) # label position
    for t in targets:
        cv2.putText(t, str(tID), lp, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (240, 0, 240, 255), 2)
for t in targets:
    name = names.pop(0)
    cv2.imwrite(f'output/{target}/{name}/{dataset}.png', t)


