import numpy as np
from PIL import Image, ImageDraw
import warnings

debug = False

def circle(d, dc = 0, opacity = 0):
    mask = Image.new("RGBA", (d, d), (0, 0, 0, opacity))
    draw = ImageDraw.Draw(mask)
    draw.ellipse((dc, dc, d - dc, d - dc), fill = (0, 0, 0, 255))
    if debug:
        mask.save(f'mask_{d}.png', quality = 100)
    return mask

def cut(square, d, mask, target, start = 0, end = None):
    c = Image.new('RGBA', (d, d))
    c.paste(square.crop((0, 0, d, d)), (0, 0), mask)
    if end is None:
        end = d
    c.crop((start, start, end, end)).save(target)
