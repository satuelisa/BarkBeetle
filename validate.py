from sys import argv
import cv2

# CV2 BGR
# four categories
# red: red, dry
# yellow: yellow, orange
# blue: leafless
# green: green, infested

from gsd import radius
from trees import parse

color = {'red': (0, 0, 255, 255), 'green': (0, 255, 0, 255),
         'yellow': (0, 255, 255, 255), 'orange': (0, 255, 255, 255),
         'leafless': (255, 0, 0, 255), 'dry': (0, 0, 255, 255),
         'infested': (0, 255, 0, 255)}

def place(trees, r, frames, labels):
    offset = int(1.2 * r)
    assert len(frames) == len(labels) - 1
    for tID in trees:
        pos, label = trees[tID]
        (x, y) = pos
        for img in frames:
            cv2.rectangle(img, (x - r, y - r), (x + r, y + r), color[label], 20)
        for img in labels:
            cv2.putText(img, str(tID), (x + offset, y + offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 5.0, (240, 0, 240, 255), 12)

dataset = argv[1]
rad = radius(dataset)
img = cv2.imread('orthomosaics/{:s}.png'.format(dataset))
targets = [img.copy(), img.copy(), img.copy()]
place(parse(dataset, True)[0], rad, targets[1:], targets)
place(parse(dataset, False)[0], rad, targets[:2], targets)
cv2.imwrite(f'validation/{dataset}_air.png', targets[0])
cv2.imwrite(f'validation/{dataset}_both.png', targets[1])
cv2.imwrite(f'validation/{dataset}_ground.png', targets[2])
        
