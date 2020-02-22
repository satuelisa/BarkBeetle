from collections import defaultdict

overall = defaultdict(int)
specific = dict()
classes = set()

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
        print('\multirow{' + str(len(o) + 1) + '}{*}{' + l + '} & & ' + ' & '.join([c for c in o]), '\\\\ \\hline')
    for row in o:
        r = ('& ' if latex else '') + ' ' * (w - len(row)) + row if not latex else f' & {row}'
        for col in o:
            if not latex:
                r += fs.format(m[(row, col)])
            else:
                
                before = '' if col != row else '{\\bf '
                after = '' if col != row else '}'
                r += f' & {before}{m[(row, col)]}{after}'
        print(r, '\\\\' if latex else '')

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

order = sorted(list(classes))
for (case, matrix) in [('global', overall)] + list(specific.items()):
    correct = sum([matrix.get((c, c), 0) for c in classes])
    total = sum(matrix.values())
    accuracy = correct / total
    error = 1 - accuracy
    sep = ' & ' if latex else '\t'
    e = 'Error' if not latex else ' & $\mathcal{E}$'
    a = 'Accuracy' if not latex else ' & $\mathcal{A}$'
    fe = '{\\bf' + f'{error:.2f}' + '}' if latex else f'{error:.2f}'
    fa = '{\\bf' + f'{accuracy:.2f}' + '}' if latex else f'{accuracy:.2f}'
    print(f'{case}{sep}{e}{sep}{fe}{sep}{a}{sep}{fa}')
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
            print(f'{sep}{c:s}{sep}{se}{sep}{sensitivity:.2f}{sep}{c:s}{sep}{sp}{sep}{specificity:.2f}')
    display(case, matrix, order, latex)


