import cv2
import os

import color
from gsd import radius

hl = {
    True: (250, 250, 250, 255),
    False: (20, 20, 20, 255)
}

def crop(array, dim):
    return array[dim[1]:dim[3], dim[0]:dim[2]]

for f in os.listdir('.'):
    fn = os.fsdecode(f)
    if fn.endswith('_majority.png'):
        dataset = fn.split('_')[0].split('.')[0]
        offsetX = None
        offsetY = None
        factor = None
        with open('offsets.txt') as data:
            for line in data:
                fields = line.split()
                if fields[0] == dataset: # do NOT break, use the LAST value (the file gets appended)
                    offsetX = int(fields[1])
                    offsetY = int(fields[2])
                    factor = float(fields[3])
        assert offsetX is not None
        result = cv2.imread(fn, cv2.IMREAD_UNCHANGED)
        h, w, channels = result.shape
        orig = cv2.imread(fn.replace('majority', 'smaller'))[offsetX : offsetX + w, offsetY : offsetY + h] # crop the same way
        trees = dict()
        kind = dict()
        with open('{:s}.map'.format(dataset)) as data:
            for line in data:
                if '#' not in line:
                    fields = line.split()
                    treeID = int(fields.pop(0))
                    if treeID <= 30:
                        continue # not the ground annotations
                    label = fields.pop(0)
                    x = round(int(fields.pop(0)) / factor) 
                    y = round(int(fields.pop(0)) / factor) 
                    trees[treeID] = (x - offsetX, y - offsetY)
                    kind[treeID] = label
        xMin = min(t[0] for t in trees.values()) 
        xMax = max(t[0] for t in trees.values()) 
        yMin = min(t[1] for t in trees.values()) 
        yMax = max(t[1] for t in trees.values()) 
        lw = 3
        step = lw + 1
        rc = result.copy()
        oc = orig.copy()
        r = radius(dataset, factor)
        offsetL = r + 4 * step        
        margin = r + offsetL + 50
        for tID in trees:
            (x, y) = trees[tID]
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
            cv2.putText(rc, str(tID), (x + offsetL, y + offsetL), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (240, 0, 240, 255), 3)
            cv2.putText(oc, str(tID), (x + offsetL, y + offsetL), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (240, 0, 240, 255), 3)
        dim = (max(0, xMin - margin), max(0, yMin - margin), min(w, xMax + margin), min(h, yMax + margin))
        cv2.imwrite(fn.replace('majority', 'output'), crop(rc, dim))
        cv2.imwrite(fn.replace('majority', 'origout'), crop(oc, dim))

