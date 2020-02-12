from math import sqrt
from sys import argv

from gsd import radius

dataset = argv[1]
threshold = 1.5 * radius(dataset)
pos = set()
nID = 31
with open('{:s}.annot'.format(dataset)) as data:
    for line in data:
        line = line.strip()
        if '#' not in line:
            fields = line.split()
            treeID = int(fields.pop(0))
            if treeID > 30:
                label = fields.pop(0)
                x = int(fields.pop(0))
                y = int(fields.pop(0))
                p = (x, y)
                ok = True
                for (tx, ty) in pos:
                    if sqrt((x - tx)**2  +  (y - ty)**2) < threshold:
                        ok = False
                        break
                if ok:
                    print(nID, label, str(x), str(y))
                    pos.add(p)
                    nID += 1
            else:
                print(line)
        else:
            print(line)
        