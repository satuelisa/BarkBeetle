relabel = {'red': 'red', 'dry': 'red',
           'leafless': 'leafless',
           'green': 'green', 'infested': 'green',
           'yellow': 'yellow', 'orange': 'yellow'}

offsets = dict()
with open('offsets.txt') as data:
    for line in data:
        fields = line.split()
        f = fields[2]
        x0 = int(fields[3])
        y0 = int(fields[4])
        x1 = int(fields[4])
        y1 = int(fields[5])
        ar = float(fields[6])
        ow = int(fields[7][1:-1]) # skip ( and ,
        oh = int(fields[8][:-1]) # skip )
        offsets[f] = (x0, y0, ow - x1) # x offset, y offset, right horizontal crop

def parse(dataset, ground = False):
    trees = dict()
    with open('annotations/{:s}.map'.format(dataset)) as data:
        for line in data:
            if '#' not in line:
                fields = line.split()
                treeID = int(fields.pop(0))
                if ground and treeID > 30:
                    continue
                elif not ground and treeID <= 30:
                    continue
                label = relabel[fields.pop(0)]
                x = int(fields.pop(0)) - offsets[dataset][0]
                y = int(fields.pop(0)) - offsets[dataset][2]
                trees[treeID] = ((x, y), label)
            elif 'Coordinates' in line:
                width = int(line.split()[4])
                width -= offsets[dataset][0] # left crop
                width -= offsets[dataset][3] # right crop
    return(trees, width)
            
