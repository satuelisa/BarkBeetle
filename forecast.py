from sys import argv
from collections import defaultdict

cc = {'black': 'gray', 'leafless': 'blue'}
      
def cell(color):
    if color == '' or color == 'NA':
        return 'NA' # will get cut
    return '\\cellcolor{' + cc.get(color, color) + '!50}'

flights = ['jun60', 'jul90', 'jul100', 'aug90', 'aug100']
observed = dict()
trees = defaultdict(dict)
with open(argv[1]) as data:
    for line in data:
        fields = line.strip().split()
        flight = fields.pop(0)
        treeID = int(fields.pop(0))
        if treeID <= 30:
            match = (fields.pop(0) == 'True')
            expert = fields.pop(0)
            if treeID in observed:
                assert observed[treeID] == expert
            else:
                observed[treeID] = expert
            assigned = ' '.join(fields)
            trees[treeID][flight] = (assigned, match)
print('ID & June 60 m & July 90 m & July 100 m & Aug 90 m & Aug 100 m & Expert & Original & \\# \\\\')
print('\\toprule')
orig = dict()
with open('trees.txt') as data:
    data.readline() # skip header row
    for line in data:
        fields = line.split()
        treeID = int(fields[0])
        orig[treeID] = fields[1]
for t in range(1, 31):
    assignments = ''
    matches = 0
    for f in flights:
        a = 'NA'
        m = False
        if f in trees[t]:
            (a, m) = trees[t][f]
        c = cell(a)
        matches += 1 * m
        assignments += ' & ' + c + m * '{\\bf ' + a + m * '}'
    if 'NA' not in assignments:
        co = cell(observed[t])
        print(t, assignments, '&', co, '{\\em '+ observed[t], '} & {\em ', orig[t], '} &', matches, '\\\\')
    
