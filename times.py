import os.path
import datetime
from sys import argv

f = '%H:%M:%S'
ref = datetime.datetime(1900,1,1)
with open(argv[1]) as phases:
    print('{\\bf Phase} & {\\bf Runtime} & $n$ \\\\')
    print('\\toprule')
    for phase in phases:
        phase = phase.strip()
        values = dict()
        k = dict()
        for step in ['start', 'end']:
            filename = f'timestamps/{phase}_{step}_time.txt'
            if os.path.exists(filename):
                with open(filename) as data:
                    k[step] = int(data.readline().strip())
                    t = datetime.datetime.strptime(data.readline().split()[3], f)
                    values[step] = (t - ref).total_seconds()
        if 'start' not in values or 'end' not in values:
            print(phase, '& no valid time stamps stored \\\\')
        else:
            n = k['start']
            assert n == k['end']
            diff = (values['end'] - values['start']) / n
            minutes = int(diff // 60)
            dur = f'{minutes:d}:'
            seconds = round(diff - 60 * minutes)
            dur += f'{seconds:02d}'
            print(phase, '&', dur, '&', n, '\\\\')
