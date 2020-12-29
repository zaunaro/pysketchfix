def minimum(x, y, z):
    m = x
    if y < m:
        m = x # Fix1 m = y
    if z < m:
        m = x # Fix2 m = z
    return m
