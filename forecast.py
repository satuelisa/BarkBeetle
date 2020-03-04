from sys import argv
from collections import defaultdict

cc = {'black': 'gray', 'leafless': 'blue'}
      
def cell(color):
    if color == 'NA':
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
print('ID & June 60 m & July 90 m & July 100 m & Aug 90 m & Aug 100 m & Expert \\\\')
print('\\toprule')
for t in range(1, 31):
    assignments = ''
    for f in flights:
        a = 'NA'
        m = False
        if f in trees[t]:
            (a, m) = trees[t][f]
        c = cell(a)
        if m:
            a = '{\\bf ' + a + '}'
        assignments += ' & ' + c + a
    if 'NA' not in assignments:
        co = cell(observed[t])
        print(t, assignments, '& {\em', co, observed[t], '} \\\\')
    
