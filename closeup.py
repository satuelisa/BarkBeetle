from sys import argv
from PIL import Image
from gsd import radius

dataset = argv[1]
r = radius(dataset)
img = Image.open('{:s}.tiff'.format(dataset))
with open('{:s}.map'.format(dataset)) as data:
    for line in data:
        if '#' not in line:
            fields = line.split()
            treeID = int(fields.pop(0))
            if treeID > 30:
                label = fields.pop(0)
                x = int(fields.pop(0))
                y = int(fields.pop(0))
                zoom = img.crop((x - r, y - r, x + r, y + r))
                zoom.save(f'{dataset}_{label}_t{treeID}.png')
