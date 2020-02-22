from math import sqrt
from collections import defaultdict

# matplotlib pie chart colors
pltcol = {'green': '#00ff00', 'red': '#ff0000', 'yellow': '#ffff00', 'leafless': '#0000ff', 'background': 'k', 'black': 'k'}

BGR = { 'red': (0, 0, 255, 255),
        'green': (0, 255, 0, 255),
        'yellow': (0, 255, 255, 255),
        'leafless': (255, 0, 0, 255),
        'black': (0, 0, 0, 255),
        'blue': (255, 0, 0, 255) }

def col2str(col, cv = True):
    b = col[0] if cv else col[2]
    g = col[1] 
    r = col[2] if cv else col[0]
    if len(col) == 4:
        if col[3] < 255: # transparent
            return 'black'
    if r == 0 and b == 255 and g == 0:
        return 'blue'
    elif r == 0 and b == 0 and g == 255:
        return 'green'
    elif r == 255 and b == 0 and g == 0:
        return 'red'
    elif r == 255 and b == 0 and g == 255:
        return 'yellow'
    elif r == 0 and g == 0 and b == 0:
        return 'black'
    else:
        return 'undefined {:d} {:d} {:d}'.format(r, g, b)

def match(colstr): # openCV pixels output at strings
    green = False
    colstr = colstr.replace('[', '')
    fields = colstr.split()
    if int(fields.pop(0)) == 255: # B
        return 'leafless' # blue
    if int(fields.pop(0)) == 255: #  G
        green = True
    if int(fields.pop(0)) == 255: # R
        if green: # R and G
            return 'yellow'
        else:
            return 'red'
    if green:
        return 'green'
    else:
        return 'black'

def majority(x, y, r, w, h, img):
    freq = defaultdict(int)
    for col in range(max(0, x - r), min(x + r + 1, w)):
        dx = (x - col)**2
        for row in range(max(0, y - r), min(y + r + 1, h)):
            dy = (y - row)**2
            if sqrt(dx + dy) <= r: # within
                freq[str(img[y, x])] += 1
    most = 0
    chosen = set()
    for c in freq:
        if freq[c] > most:
            chosen = { match(c) }
            most = freq[c]
        elif freq[c] == most:
            chosen.add(match(c))
    return chosen

if __name__ == '__main__':
    for c in BGR:
        b, g, r, a = BGR[c]
        print(c, match(f'[{b} {g} {r} {a}] '))
    
    
    
    
