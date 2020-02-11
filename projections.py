import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

plt.rcParams.update({'font.size': 18})

def jitter(n, scale = 0.5):
    return scale * (-1 + 2 * np.random.randn(n))
    
def scatter(title, groups, xl, yl, output, show = False):  # based on https://jakevdp.github.io/PythonDataScienceHandbook/04.08-multiple-subplots.html
    fig = plt.figure(figsize = (6, 6))
    ax = fig.add_axes([0, 0, 1, 1])
    grid = plt.GridSpec(4, 4, hspace = 0.1, wspace = 0.1)
    main = fig.add_subplot(grid[:-1, 1:])
    hori = fig.add_subplot(grid[:-1, 0], xticklabels = [], sharey = main)
    hori.invert_xaxis()        
    vert = fig.add_subplot(grid[-1, 1:], yticklabels = [], sharex = main)
    vert.invert_yaxis()
    if show:
        plt.text(0.5, 0.9, title, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    for (x, y, c) in groups:
        assert len(x) == len(y)
        n = len(x)
        main.plot(x + jitter(n), y + jitter(n), 'o', markersize = 0.1, alpha = 0.4, color = c)
        vert.hist(x, 40, histtype = 'stepfilled', orientation = 'vertical', color = c, alpha = 0.5)
        hori.hist(y, 40, histtype = 'stepfilled', orientation = 'horizontal', color = c, alpha = 0.5)
    plt.setp(main.get_xticklabels(), visible=False)
    plt.setp(main.get_yticklabels(), visible=False)
    plt.setp(hori.get_yticklabels(), visible=False)
    plt.setp(vert.get_xticklabels(), visible=False)
    hori.set_ylabel(yl)
    vert.set_xlabel(xl)
    ax.axis('off')
    plt.savefig(output, bbox_inches='tight', pad_inches=0, width=8000)
    plt.close() 

def analyze(pixels):
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
    minnl = np.min(nonLeafless, axis = 1)

    # channel maximum
    maxl = np.max(leafless, axis = 1)
    maxg = np.max(green, axis = 1)
    maxy = np.max(yellow, axis = 1)
    maxr = np.max(red, axis = 1)
    maxnl = np.max(nonLeafless, axis = 1)    
    
    # red channel
    gr = green[:, 0]
    yr = yellow[:, 0]
    rr = red[:, 0]
    lr = leafless[: , 0]
    nyr = nonYellow[:, 0]
    nlr = nonLeafless[:, 0]    
    
    # green channel
    gg = green[:, 1]
    yg = yellow[:, 1]
    rg = red[:, 1]
    lg = leafless[:, 1]
    nyg = nonYellow[:, 1]
    nlg = nonLeafless[:, 2]
    
    # blue channel
    gb = green[:, 2]
    yb = yellow[:, 2]
    rb = red[:, 2]
    lb = leafless[: , 2]
    nlb = nonLeafless[:, 2]
    
    # R - G
    grg = gr - gg
    yrg = yr - yg
    rrg = rr - rg
    lrg = lr - lg
    nyrg = nyr - nyg
    
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
    nlrg = (nlg + nlr) / 2
    
    # B - avg RG
    gbarg = gb - grg
    ybarg = yb - yrg
    rbarg = rb - rrg
    lbarg = lb - lrg
    nlbarg = nlb - nlrg
    
    # grayscale
    gn = (gr + gr + gb) / 3
    rn = (rr + rr + rb) / 3
    yn = (yr + yr + yb) / 3
    ln = (lr + lr + lb) / 3
    nln = (nlr + nlr + nlb) / 3    
    
    scatter('Leafless versus others',
            [(minnl, maxnl, '#000000'),
             (minl, maxl, '#0000ff')],
            'Minimum channel value', 'Maximum channel value', 'max_vs_min.png')

    scatter('Yellow versus red',
            [(rn, rrg, '#ff0000'),
             (yn, yrg, '#999900')],
            'Grayscale tone', 'R - G channel difference', 'gray_vs_rgd.png')

    scatter('Leafless versus others',
            [(nlb, maxnl, '#000000'),
             (lb, maxl, '#0000ff')],
            'Blue channel', 'Maximum channel value', 'blue_vs_maximum.png')
    
    scatter('Leafless versus others',
            [(nln, nlbarg, '#000000'),
             (ln, lbarg, '#0000ff')],
            'Grayscale tone', 'B - (R + G) / 2', 'blue_vs_arg.png')

    scatter('Green versus yellow',
            [(gg, grg, '#00ff00'),
            (yg, yrg, '#000000')], 
            'Green channel', 'R - G channel difference', 'green_vs_rgd.png')
    
    scatter('Green versus yellow',
            [(gg, gr, '#00ff00'),
             (yg, yr, '#000000')], 
            'Green channel', 'Red channel', 'green_vs_yellow.png')
    
    scatter('Green versus red',
            [(gg, gr, '#00ff00'),
             (rg, rr, '#aa0000')], 
            'Green channel', 'Red channel',  'green_vs_red.png')
    
    scatter('Yellow versus red',
            [(yg, yr, '#000000'),
             (rg, rr, '#aa0000')], 
            'Green channel', 'Red channel', 'yellow_vs_red.png')

    scatter('Leafless versus green',
            [(lg, lb, '#0000ff'),
             (gg, gb, '#00ff00')], 
            'Green channel', 'Blue channel', 'leafless_vs_green.png')
    
    scatter('Leafless versus red',
            [(lr, lb, '#0000ff'),
             (rr, rb, '#aa0000')], 
            'Red channel', 'Blue channel', 'leafless_vs_red.png')
    
    scatter('Leafless versus yellow',
            [(lg, lb, '#0000ff'),
             (yg, yb, '#000000')], 
            'Green channel', 'Blue channel', 'leafless_vs_yellow.png')

classes = ['green', 'yellow', 'red', 'leafless']
datasets = ['jun60', 'jul90', 'jul100', 'aug90', 'aug100']
pixels = dict()
for kind in classes:
    for dataset in datasets:
        image = Image.open(f'{dataset}_{kind}.png')
        a = np.array(image)
        dim = a.shape
        a = a[a[:,:,3] > 0] # take the non-transparent ones
        a = a[:, :3] # drop the alpha channel        
        if kind not in pixels:
            pixels[kind] = a
        else:
            pixels[kind] = np.concatenate((pixels[kind], a), axis = 0)            
analyze(pixels)


    
