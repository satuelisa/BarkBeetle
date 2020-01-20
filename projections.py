import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def jitter(n, scale = 0.5):
    return scale * (-1 + 2 * np.random.randn(n))
    
def scatter(groups, xl, yl, output):  # based on https://jakevdp.github.io/PythonDataScienceHandbook/04.08-multiple-subplots.html
    fig = plt.figure(figsize = (6, 6))
    grid = plt.GridSpec(4, 4, hspace = 0.1, wspace = 0.1)
    main = fig.add_subplot(grid[:-1, 1:])
    hori = fig.add_subplot(grid[:-1, 0], xticklabels = [], sharey = main)
    hori.invert_xaxis()        
    vert = fig.add_subplot(grid[-1, 1:], yticklabels = [], sharex = main)
    vert.invert_yaxis()
    for (x, y, c) in groups:
        assert len(x) == len(y)
        n = len(x)
        main.plot(x + jitter(n), y + jitter(n), 'o', markersize = 0.5, alpha = 0.3, color = c)
        vert.hist(x, 40, histtype = 'stepfilled', orientation = 'vertical', color = c, alpha = 0.3)
        hori.hist(y, 40, histtype = 'stepfilled', orientation = 'horizontal', color = c, alpha = 0.3)
    plt.setp(main.get_xticklabels(), visible=False)
    plt.setp(main.get_yticklabels(), visible=False)
    plt.setp(hori.get_yticklabels(), visible=False)
    plt.setp(vert.get_xticklabels(), visible=False)
    hori.set_ylabel(yl)
    vert.set_xlabel(xl)    
    plt.savefig(output)
    plt.close() 

def analyze(pixels, dataset):
    # classes
    leafless = pixels['leafless']
    red = pixels['red']
    yellow = pixels['yellow']
    green = pixels['green']
    
    # others
    nonLeafless = np.concatenate([pixels['green'], pixels['yellow'], pixels['red']])
    nonGreen = np.concatenate([pixels['leafless'], pixels['yellow'], pixels['red']])
    nonYellow = np.concatenate([pixels['green'], pixels['leafless'], pixels['red']])
    nonRed = np.concatenate([pixels['green'], pixels['yellow'], pixels['leafless']])
    
    # channel minimum
    minl = np.min(leafless, axis = 1)
    ming = np.min(green, axis = 1)
    miny = np.min(yellow, axis = 1)
    minr = np.min(red, axis = 1)

    # channel maximum
    maxl = np.max(leafless, axis = 1)
    maxg = np.max(green, axis = 1)
    maxy = np.max(yellow, axis = 1)
    maxr = np.max(red, axis = 1)
    
    # red channel
    gr = green[:, 0]
    yr = yellow[:, 0]
    rr = red[:, 0]
    lr = leafless[: , 0]
    
    # green channel
    gg = green[:, 1]
    yg = yellow[:, 1]
    rg = red[:, 1]
    lg = leafless[: , 1]
    
    # blue channel
    gb = green[:, 2]
    yb = yellow[:, 2]
    rb = red[:, 2]
    lb = leafless[: , 2]
    
    # R - G
    grg = gr - gg
    yrg = yr - yg
    rrg = rr - rg
    lrg = lr - lg
    
    # R - B
    grb = gr - gb
    yrb = yr - yb
    rrb = rr - rb
    lrb = lr - lb

    # G - B
    ggb = gg - gb
    ygb = yg - yb
    rgb = rg - rb
    lgb = lg - lb
    
    # avg RG
    grg = (gg + gr) / 2
    yrg = (yg + yr) / 2
    rrg = (rg + rr) / 2
    lrg = (lg + lr) / 2
    
    # B - avg RG
    gbarg = gb - grg
    ybarg = yb - yrg
    rbarg = rb - rrg
    lbarg = lb - lrg
    
    # grayscale
    gn = (gr + gr + gb) / 3
    rn = (rr + rr + rb) / 3
    yn = (yr + yr + yb) / 3
    ln = (lr + lr + lb) / 3
    
    scatter([(minr, maxr, '#ff0000'),
             (ming, maxg, '#00ff00'),
             (miny, maxy, '#ffff00'),
             (minl, maxl, '#0000ff')],
            'Minimum channel value', 'Maximum channel value', dataset + '_max_vs_min.png')

    scatter([(rn, rrg, '#ff0000'),
             (gn, grg, '#00ff00'),
             (yn, yrg, '#ffff00'),
             (ln, lrg, '#0000ff')],
            'Grayscale tone', 'R - G channel difference', dataset + '_gray_vs_rgd.png')

    scatter([(rg, rrg, '#ff0000'),
             (gg, grg, '#00ff00'),
             (yg, yrg, '#ffff00'),
             (lg, lrg, '#0000ff')],
            'Blue channel', 'Maximum channel value', dataset + '_blue_vs_maximum.png')
    
    scatter([(rn, rbarg, '#ff0000'),
             (gn, gbarg, '#00ff00'),
             (yn, ybarg, '#ffff00'),
             (ln, lbarg, '#0000ff')],
            'Grayscale tone', 'B - (R + G) / 2', dataset + '_blue_vs_arg.png')
    
    scatter([(rg, rrg, '#ff0000'),
             (gg, grg, '#00ff00'),
             (yg, yrg, '#ffff00'),
             (lg, lrg, '#0000ff')],
            'Green channel', 'R - G channel difference', dataset + '_green_vs_rgd.png')

classes = ['green', 'yellow', 'red', 'leafless']
datasets = ['jun60', 'jul90', 'jul100', 'aug90', 'aug100']
for dataset in datasets:
    pixels = dict() # non-transparent pixels per class
    for kind in classes:
        image = Image.open(f'{dataset}_{kind}.png')
        a = np.array(image)
        a = a[a[:,:,3] > 0] # take the non-transparent ones
        a = a[:, :3] # drop the alpha channel        
        pixels[kind] = a
    analyze(pixels, dataset)


    
