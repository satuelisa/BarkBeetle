relabel = {'red': 'red', 'ground': 'ground',
           'dry': 'leafless', 'leafless': 'leafless',
           'green': 'green', 'infested': 'green',
           'yellow': 'yellow', 'orange': 'yellow'}

def parse(dataset, ground = False):
    width = None
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
                x = int(fields.pop(0))
                y = int(fields.pop(0))
                trees[treeID] = ((x, y), label)
            elif '# dim' in line:
                width = int(line.split()[2])
    return(trees, width)
