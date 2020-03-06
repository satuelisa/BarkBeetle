def decimal(string):
    pd = string.find('d')
    pm = string.find('\'')
    ps = string.find('"')
    d = int(string[0:pd])
    m = int(string[(pd + 1):pm])
    s = float(string[(pm + 1):ps])
    v = d + m / 60 + s / 60**2
    return v if string[-1] in 'NE' else -v

def latitude(s):
    assert 'N' in s or 'S' in s    
    return decimal(s)    

def longitude(s):
    assert 'E' in s or 'W' in s    
    return decimal(s)    

def translate(pos, start, end, scale, offset, invert):
    span = end - start # degree span
    assert span > 0 # there is a span
    assert start <= pos # position comes after it starts
    assert pos <= end # position comes before it ends
    assert offset >= 0
    r = (pos - start) / span # relative position
    if invert: # origin in the top left corner for pixels
        r = 1 - r
    originalPixel = round(r * scale) - offset
    return originalPixel 

def lat2y(d, o):
    return translate(d, o['S'], o['N'], o['hOrig'], o['y0'], True)

def lon2x(d, o):
    return translate(d, o['W'], o['E'], o['wOrig'], o['x0'], False)
    
