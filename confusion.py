from collections import defaultdict

overall = defaultdict(int)
specific = dict()
classes = set()
repl = {
    'jun60': 'June 60 m',
    'jul90': 'July 90 m', 
    'jul100': 'July 100 m',
    'aug90': 'August 90 m',
    'aug100': 'August 100 m'
}

from math import floor, log

def display(l, m, o, latex = False):
    w = max(max([len(c) for c in o]), max([int(floor(log(v, 2))) + 1 for v in m.values()])) + 1
    fs = '{:' + str(w) + 'd}'
    if not latex:
        print(w * ' ' + ''.join([' ' * (w - len(c)) + c for c in o]))
    else:
        l = l.capitalize()
        if l != 'Global':
            l = l[:3] + ' ' + l[3:] + ' m'
    print('\\midrule % CM \n\\multirow{' + str(len(o) + 1) + '}{*}{' + case + '} & & ' + ' & '.join([c for c in o]) + ' \\\\ % CM')
    for row in o:
        r = ('& ' if latex else '') + ' ' * (w - len(row)) + row if not latex else f' & {row}'
        for col in o:
            if not latex:
                r += fs.format(m[(row, col)])
            else:
                
                before = '' if col != row else '{\\bf '
                after = '' if col != row else '}'
                r += f' & {before}{m[(row, col)]}{after}'
        print(r, '\\\\ % CM' if latex else '')

from sys import argv

latex = 'tex' in argv
with open(argv[1]) as data:
    for line in data:
        fields = line.split()
        dataset = fields.pop(0)
        tree = fields.pop(0)
        match = bool(fields.pop(0))
        predicted = fields.pop(0)
        expected = fields.pop(0)
        if len(fields) > 0:
            print(f'WARNING: Multiple matches for {tree} in {dataset}')
        classes.update({predicted, expected})
        overall[(expected, predicted)] += 1
        if dataset not in specific:
            specific[dataset] = defaultdict(int)
        specific[dataset][(expected, predicted)] += 1

order = ['green', 'yellow', 'red', 'leafless', 'ground']
for (case, matrix) in [('global', overall)] + list(specific.items()):
    correct = sum([matrix.get((c, c), 0) for c in classes])
    total = sum(matrix.values())
    accuracy = correct / total
    error = 1 - accuracy
    sep = ' & ' if latex else '\t'
    e = 'Error' if not latex else '$\\epsilon$'
    a = 'Accuracy' if not latex else '$\\alpha$'
    fe = '{\\bf ' + f'{error:.2f}' + '}' if latex else f'{error:.2f}'
    fa = '{\\bf ' + f'{accuracy:.2f}' + '}' if latex else f'{accuracy:.2f}'
    if case == 'global' and latex:
        case = '{\\bf ' + case + '}'
    if latex:
        if case in repl:
            case = repl[case]
    print(f'{case}{sep}{e}{sep}{fe}{sep}{a}{sep}{fa} \\\\ % STATS')
    for c in classes:
        if c != 'black': 
            tp = matrix.get((c, c), 0) # predicted == expected
            cs = sum([matrix.get((c, o), 0) for o in classes]) # where the class is expected
            rs = sum([matrix.get((o, c), 0) for o in classes]) # where the class is predicted
            fn = cs - tp # expected but not predicted
            fp = rs - tp # predicted but not expected
            tn = total - (tp + fn + fp) # all the other cases
            sensitivity = 0 # when it is the class
            if tp + fn > 0: # success rate in recognizing when the sample belongs in the class
                sensitivity = tp / (tp + fn)
            se = 'Sensitivity' if not latex else '$S_e$'
            specificity = 0 # when it is not in the class
            if tn + fp > 0: # success rate in recognizing when the sample does not belong in the class
                specificity = tn / (tn + fp)
            sp = 'Specificity' if not latex else '$S_p$'
            print(f'{c:s}{sep}{se}{sep}{sensitivity:.2f}{sep}{sp}{sep}{specificity:.2f} \\\\ % STATS')
    if latex:
        print('\\midrule % STATS')
    
    display(case, matrix, order, latex)


