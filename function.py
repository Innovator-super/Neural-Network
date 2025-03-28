from random import uniform
import math
def array1D(w):
    return [0 for _ in range(w)]


def array2D(w, h, random = False):
    return [[uniform(-1, 1) if random else 0 for __ in range(h)]for _ in range(w)]


def rgb(r, g, b):
    r = math.floor(min(max(r, 0), 255))
    g = math.floor(min(max(g, 0), 255))
    b = math.floor(min(max(b, 0), 255))
    return f'#{r:02x}{g:02x}{b:02x}'

def lrelu(x):
    if x > 1:
        return 1 + 0.01 * (x - 1)
    elif x < 0:
        return 0.01 * x
    return x

def dlrelu(x):
    if x > 1:
        return 0.01
    elif x < 0:
        return 0.01
    return 1