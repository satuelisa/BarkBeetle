import datetime
from sys import argv

phases = None
with open(argv[1]) as data:
    phases = data.readlines()

f = '%H:%M:%S'
print('{\\bf Phase} & {\\bf Runtime} \\\\')
print('\\hline')
for phase in phases:
    phase = phase.strip()
    try: # see if the files exist
        values = dict()
        for step in ['start', 'end']:
            with open(f'timestamps/{phase}_{step}_time.txt') as data:
                values[step] = datetime.datetime.strptime(data.readline().split()[3], f)
        diff = values['end'] - values['start']
        dur = f'{diff}'
        if dur.startswith('0:'):
            dur = dur[2:] # skip the empty hours
        print(phase, '&', dur, '\\\\')
    except:
        print(phase, '& no valid time stamps stored \\\\')
