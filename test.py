import cv2
import color
from sys import argv

from trees import parse
from gsd import radius

hl = {
    True: (250, 250, 250, 255),
    False: (20, 20, 20, 255)
}

ground = 'ground' in argv
dataset = argv[1]
targets = {
    'original': cv2.imread(f'scaled/original/{dataset}.png', cv2.IMREAD_UNCHANGED),
    'enhanced': cv2.imread(f'scaled/enhanced/{dataset}.png', cv2.IMREAD_UNCHANGED),
    'thresholded': cv2.imread(f'thresholded/{dataset}.png', cv2.IMREAD_UNCHANGED),
    'automaton': cv2.imread(f'automaton/{dataset}.png', cv2.IMREAD_UNCHANGED)}
    
h, w, channels = targets['automaton'].shape
trees, ow = parse(dataset, ground)
factor = ow / w # scaling factor
lw = 3
step = lw + 1
r = radius(dataset, factor)
offsetL = r + 4 * step        
margin = r + offsetL + 50
target = 'ground' if ground else 'air'
for tID in trees:
    (x, y), label = trees[tID]
    x =  int(round(x / factor))
    y =  int(round(y / factor))
    intended = color.BGR[label]
    present = color.majority(x, y, r, w, h, targets['automaton'])
    match = label in present
    print(dataset, tID, label in present, label, ' '.join(present))
    for t in targets.values():
        cv2.circle(t, (x, y), r, hl[match], lw)
        cv2.circle(t, (x, y), r + step, intended, lw)
    i = 2
    for c in present:
        for t in targets.values():
            cv2.circle(t, (x, y), r + i * step, color.BGR[c], lw)
        i += 1
    for t in targets.values():
        cv2.circle(t, (x, y), r + i * step, hl[match], lw)
    lp = (x + offsetL, y + offsetL) # label position
    for t in targets.values():
        cv2.putText(t, str(tID), lp, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (240, 0, 240, 255), 2)
for (name, image) in targets.items():
    cv2.imwrite(f'output/{target}/{name}/{dataset}.png', image)


