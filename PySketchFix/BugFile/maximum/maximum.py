def maximum(x, y, z):
    m = x
    if y > x:
        m = x # Fix m = y
    if z > m:
        m = z
    return m
