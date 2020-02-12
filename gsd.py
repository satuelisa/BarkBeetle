sample = None # sample radius in cm
with open('radius.dat') as data:
    for line in data:
        if 'radius' in line:
            sample = float(line.split()[-1]) * 100 
            
GSD = {'jun60': 1.7630, 'jul90': 2.109, 'jul100': 2.175, 'aug90': 1.965, 'aug100': 2.102} # cm

def radius(dataset, factor = 1):
    return int(round((sample / GSD[dataset]) / factor))
