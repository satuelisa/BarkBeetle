sample = None # sample radius in cm
with open('radius.dat') as data:
    for line in data:
        if 'radius' in line:
            sample = float(line.split()[-1]) * 100 
            
GSD = dict() # cm per pixel

output = (__name__ == "__main__")

if output:
    print('''\multirow{2}{*}{}
    & Alt.\ & GSD & Scale
    & \multicolumn{2}{c}{Image width} & \multicolumn{2}{c}{Image height} \\\\
    & m & cm/px & px/m & px  & $\\approx$ m & px & $\\approx$ m \\\\ ''')

for dataset in ['jun60', 'jul90', 'jul100', 'aug90', 'aug100']:
    w, h = None, None
    with open(f'annotations/{dataset}.info'.format(dataset)) as data:
        for line in data:
            if 'Size is' in line:
                w = int(line.split()[2][:-1])
                h = int(line.split()[3])
            if 'Pixel Size' in line:
                ps = 100 * float(line.split()[3].split(',')[0][1:])
                GSD[dataset] = ps
                if output:
                    month = dataset[:3].capitalize()
                    alt = dataset[3:]
                    wm = "{:.2f}".format(ps * w / 100)
                    hm = "{:.2f}".format(ps * h / 100)
                    pm = round(100 / ps)
                    fields = [month, alt, "{:.5f}".format(ps), pm,  w, wm, h, hm, '\\\\']
                    print(' & '.join([str(f) for f in fields]))
                    
def radius(dataset, factor = 1):
    return int(round((sample / GSD[dataset]) / factor))
