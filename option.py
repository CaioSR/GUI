import math

def getCoordinates(grid, p):

    p = str(p)

    if len(p) == 15:
        p = [0,0]

    else:
        p = int(p[15:])

        if p % grid.xsize == 0:
            x_coord = grid.xsize -1
            y_coord = 1
        else:
            x_coord = p % grid.xsize - 1
            y_coord = 0

        p = [x_coord, p // grid.xsize - y_coord]
    return p

def interpol(p1,p2,t):
    inter = []
    for i in range(2):
        inter.append((1-t)*p1[i] + t*p2[i])

    return inter

def distance(p1,p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def m(p1,p2):
    if p2[0] == p1[0]:
        m = 0
    else:
        m = (p2[1]-p1[1])/(p2[0]-p1[0])

    return m