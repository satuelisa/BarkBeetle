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

def lat2y(d, o):
    span = o['N'] - o['S']
    assert span > 0    
    assert o['S'] <= d
    assert d <= o['N']
    pos = (d - o['S']) / span
    h = o['height']
    return round(o['y0'] + pos * h)

def lon2x(d, o):
    span = o['E'] - o['W']
    assert span > 0
    assert o['W'] <= d
    assert d <= o['E']
    pos = (d - o['E']) / span
    w = o['width']
    return round(o['x0'] + pos * w)
    
