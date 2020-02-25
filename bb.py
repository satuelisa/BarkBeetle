LAT = 1
LON = 0
from latlon import latitude, longitude

def parse(line):
    start = line.rfind('(') + 1 
    end = line.rfind(')') 
    coords = [None, None]
    for value in line[start:end].split(','):
        if '"W' in value or '"E' in value:
            coords[LON] = longitude(value.strip().lstrip()) 
        else:
            coords[LAT] = latitude(value.strip().lstrip())
    assert coords[LAT] > 0 and coords[LON] < 0
    return coords

from PIL import Image
from math import fabs, ceil
from collections import defaultdict

flights = ['jun60', 'jul90', 'jul100', 'aug90', 'aug100']
corners = ['Upper Left', 'Lower Left', 'Upper Right', 'Lower Right']
fc = defaultdict(dict)
sizes = dict()
for f in flights:
    with open(f'annotations/{f}.info') as data:
        for line in data:
            if 'Size' in line and 'Pixel' not in line:
                fields = line.strip().split()
                w = int(fields[2][:-1]) # remove ,
                h = int(fields[3])
                sizes[f] = (w, h)
            else:
                for c in corners:
                    if c in line:
                        fc[f][c] = parse(line)
                        break # only one corner per line in the info file
lowLat = set()
highLat = set()
lowLon = set()
highLon = set()
lats = set()
lons = set()
for f in flights:
    corners = fc[f]
    assert len(corners) == 4
    for c in corners:
        corner = corners[c]
        lats.add(corner[LAT])
        lons.add(corner[LON])
    # the inner-most ones to counter the slight tilt
    # LAT (north/south upper/lower)
    lowLat.add(max(corners['Lower Left'][LAT], corners['Lower Right'][LAT]))
    highLat.add(min(corners['Upper Left'][LAT], corners['Upper Right'][LAT]))
    # LON (west/east left/right)
    lowLon.add(max(corners['Lower Left'][LON], corners['Upper Left'][LON]))
    highLon.add(min(corners['Lower Right'][LON], corners['Upper Right'][LON]))
minLon = min(lons)  
maxLon = max(lons)
minLat = min(lats)
maxLat = max(lats)
startLon = max(lowLon)
endLon = min(highLon)
startLat = max(lowLat)
endLat = min(highLat)
delta = 0.0003
assert startLat <= endLat
assert startLon <= endLon
print('set term postscript eps color 15')
print('set xlabel "Longitude (W)"')
print('set ylabel "Latitude (N)"')
print('set output "bb.eps"')
print('set size 1.5, 1.5')
print('# Shared longitude (S-N) goes from', startLon, 'to', endLon)
print(f'set xrange [{minLon - delta}:{maxLon + delta}]')
print('# Shared latitude (W-E) goes from', startLat, 'to', endLat)
print(f'set yrange [{minLat - delta}:{maxLat + delta}]')
i = 1
print(f'set arrow {i} from {startLon}, {startLat} to {startLon}, {endLat} nohead lc rgb "#dddddd" lw 20')
i += 1
print(f'set arrow {i} from {endLon}, {startLat} to {endLon}, {endLat} nohead lc rgb "#dddddd" lw 20')
i += 1
print(f'set arrow {i} from {endLon}, {endLat} to {startLon}, {endLat} nohead lc rgb "#dddddd" lw 20')
i += 1
print(f'set arrow {i} from {endLon}, {startLat} to {startLon}, {startLat} nohead lc rgb "#dddddd" lw 20')
i += 1
color = {'jun60': '#ff0000', 'jul90': '#00cc00', 'jul100': '#66cc33', 'aug90': '#0000cc', 'aug100': '#6633cc'}
label = {'jun60': 'June 60 m', 'jul90': 'July 90 m', 'jul100': 'July 100 m', 'aug90': 'August 90 m', 'aug100': 'August 100 m'}
lc = {'jun60': 2, 'jul90': 0, 'jul100': 0, 'aug90': 2, 'aug100': 2}
aspectratio = set()
for f in fc:
    c = fc[f]
    (w, h) = sizes[f]
    # our LATITUDES are negative (north)
    north = min(c['Upper Left'][LAT], c['Upper Right'][LAT])
    assert north >= endLat
    south = max(c['Lower Left'][LAT], c['Lower Right'][LAT])
    assert south <= startLat
    # our LONGITUDES are POSITIVE (west) 
    west = max(c['Lower Left'][LON], c['Upper Left'][LON]) 
    assert west <= startLon
    east = max(c['Upper Right'][LON], c['Upper Right'][LON]) 
    assert east >= endLon
    sw = east - west # width span
    assert sw > 0
    sh = north - south # height span    
    assert sh > 0
    pw = w / sw # width pixel units
    ph = h / sh # height pixel units
    assert fabs(pw - pw) < 1
    x0 = int(ceil(w * (startLon - west) / sw)) # left margin
    y0 = int(ceil(h * (north - endLat) / sh)) # top margin
    x1 = w - int(ceil(w * (east - endLon) / sw)) # right margin
    y1 = h - int(ceil(h * (startLat - south) / sh)) # top margin
    assert x1 <= w
    assert y1 <= h    
    zone = (x0, y0, x1, y1)
    nw = x1 - x0  
    nh = y1 - y0
    aspectratio.add(nw / nh)
    print('# crop', f, x0, y0, x1, y1, sizes[f], north, south, west, east)
    full = Image.open(f'orthomosaics/{f}.tiff')
    cropped = full.crop(zone)
    cropped.save(f'cropped/{f}.png')
    segments = [(c['Upper Left'], c['Upper Right']), # upper left to upper right
                (c['Upper Right'], c['Lower Right']), # upper right to lower right
                (c['Lower Right'], c['Lower Left']), # lower right to lower left
                (c['Lower Left'], c['Upper Left'])] # lower left to upper left
    pos = lc[f]
    x = sum([s[0] for s in segments[pos]]) / 2
    y = sum([s[1] for s in segments[pos]]) / 2
    print(f'set label {i} "{label[f]}" at {x}, {y} right textcolor "{color[f]}" offset character 1, 1')
    for (p1, p2) in segments:
        (x1, y1) = p1
        (x2, y2) = p2
        print(f'set arrow {i} from {x1}, {y1} to {x2}, {y2} nohead lc rgb "{color[f]}" lw 4')
        i += 1
print('plot NaN t ""')
assert fabs(min(aspectratio) - max(aspectratio)) < 0.1 # should be roughly constant
