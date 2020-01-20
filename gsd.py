from math import ceil

sample = 400 # cm
GSD = {'jun60': 1.7630, 'jul90': 2.109, 'jul100': 2.175, 'aug90': 1.965, 'aug100': 2.102} # cm

def radius(dataset, factor = 1):
    return int((ceil((sample / GSD[dataset]) / factor))) # in pixels
