def reflect(p1,p2):
    mR,xR,yR = 0,0,0

    try:
        m = (p2[1]-p1[1])/(p2[0]-p1[0])
    except:
        m = 2

    if m > 1 or m < -1:
        p1[0],p1[1]=p1[1],p1[0]
        p2[0],p2[1]=p2[1],p2[0]
        mR = 1

    if p1[0] > p2[0]:
        p1[0] = p1[0]*(-1)
        p2[0] = p2[0]*(-1)
        xR = 1

    print(p1[1],p2[1])
    if p1[1] > p2[1]:
        p1[1] = p1[1]*(-1)
        p2[1] = p2[1]*(-1)
        yR = 1

    return p1,p2,mR,xR,yR

def dereflect(p,mR,xR,yR):
    if mR == 1:
        p[0],p[1] = p[1],p[0]

    if xR == 1:
        p[0] = p[0]*(-1)

    if yR == 1:
        p[1] = p[1]*(-1)

    return p

def bresenham(p1,p2):



    p1,p2,mR,xR,yR = reflect(p1,p2)

    x = p1[0]
    y = p1[1]

    try:
        m = (p2[1]-p1[1])/(p2[0]-p1[0])
    except:
        m = 1

    e = m - 0.5

    list,result = [],[]

    list.append([x,y])

    while x < p2[0]:
        if e >= 0:
            y += 1
            e -= 1
        x += 1
        e += m

        list.append([x,y])

    if mR == 1 or xR == 1 or yR == 1:
        for p in list:
            p = dereflect(p,mR,xR,yR)
            list[list.index(p)] = p
    return list

p1,p2 = [18,5],[13,13]

result = bresenham(p1,p2)

print(result)
