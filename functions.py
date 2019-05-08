import math
import option

def bresenham(p1, p2):
    try:
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

        if p1[1] > p2[1] :
            p1[1] = p1[1]*(-1)
            p2[1] = p2[1]*(-1)
            yR = 1

        x = p1[0]
        y = p1[1]

        m = (p2[1]-p1[1])/(p2[0]-p1[0])

        e = m - 0.5

        result_list = []

        result_list.append([x,y])

        while x < p2[0]:
            if e >= 0:
                y += 1
                e -= 1
            x += 1
            e += m

            result_list.append([x,y])

        if mR == 1 or xR == 1 or yR == 1:
            for p in result_list:

                if yR == 1:
                    p[1] = p[1]*(-1)

                if xR == 1:
                    p[0] = p[0]*(-1)

                if mR == 1:
                    p[0],p[1] = p[1],p[0]

                result_list[result_list.index(p)] = p

        return result_list

    except:
        pass

def circle(p1, p2 = None, r = None):
    try:


        if p2:
            point = [p2[0] - p1[0], p2[1] - p1[1]]
            radius = math.floor(math.sqrt((point[0] ** 2 + point[1] ** 2)))
            noRadiusReturn = False
        if r:
            radius = r
            noRadiusReturn = True

        x = 0
        y = radius
        p = 1 - radius

        result = []
        result.append([x,y])
        while(x<y):
            x += 1
            if p < 0:
                p += 2*x + 3
            else:
                y -= 1
                p += 2*x - 2*y + 5
            result.append([x,y])

        leng = len(result)
        ct = 0
        for po in result:
            result.append([po[1],po[0]])
            result.append([po[1]*(-1),po[0]])
            result.append([po[0]*(-1),po[1]])
            result.append([po[0]*(-1),po[1]*(-1)])
            result.append([po[1]*(-1),po[0]*(-1)])
            result.append([po[1],po[0]*(-1)])
            result.append([po[0],po[1]*(-1)])
            ct += 1
            if ct == leng:
                break

        for po in result:
            po[0],po[1] = po[0]+p1[0],po[1]+p1[1]

        if noRadiusReturn:
            return result
        else:
            return radius, result

    except:
        pass



def curve(p, matriz, grid):
    try:
        ip1p2 = []
        ip2p3 = []
        ip3p4 = []
        iIp1 = []
        iIp2 = []
        iIip = []

        result = []
        for i in range(50):
            t = (i*2)/100
            ip1p2.append(option.interpol(p[0],p[1],t))
            ip2p3.append(option.interpol(p[1],p[2],t))
            ip3p4.append(option.interpol(p[2],p[3],t))
            iIp1.append(option.interpol(ip1p2[i],ip2p3[i],t))
            iIp2.append(option.interpol(ip2p3[i],ip3p4[i],t))
            iIip.append(option.interpol(iIp1[i],iIp2[i],t))
            iIip[i][0] = math.floor(iIip[i][0])
            iIip[i][1] = math.floor(iIip[i][1])

            result.append(option.getCoordinates(grid, matriz[iIip[i][1]][iIip[i][0]]))

        return result

    except:
        pass

def recurFill(point, matriz, grid):
    try:

        point.configure(bg='blue')
        p = option.getCoordinates(grid, point)

        if p[1] < grid.ysize-1:
            up = matriz[p[1]+1][p[0]]
            if up['bg'] == 'white': recurFill(up, matriz, grid) #cima
        if p[1] > 0:
            down = matriz[p[1]-1][p[0]]
            if down['bg'] == 'white': recurFill(down, matriz, grid) #baixo
        if p[0] > 0:
            left = matriz[p[1]][p[0]-1]
            if left['bg'] == 'white': recurFill(left, matriz, grid) #esquerda
        if p[0] < grid.xsize-1:
            right = matriz[p[1]][p[0]+1]
            if right['bg'] == 'white': recurFill(right, matriz, grid) #direita

    except:
        pass

def scanLine(vertices):

    lines_table,yList,xList = [],[],[]

    for vertice in vertices:
        if vertice[0][1] <= vertice[1][1]:
            y_min = vertice[0][1]
            y_max = vertice[1][1]
            x_y_min = vertice[0][0]
            x_y_max = vertice[1][0]
        else:
            y_min = vertice[1][1]
            y_max = vertice[0][1]
            x_y_min = vertice[1][0]
            x_y_max = vertice[0][0]

        yList.append(vertice[0][1])
        yList.append(vertice[1][1])
        xList.append(vertice[0][0])
        xList.append(vertice[1][0])

        m = option.m([x_y_min,y_min], [x_y_max,y_max])
        if m == 0: m1 = 0
        else: m1 = 1/m

        lines_table.append([y_min, y_max, x_y_min, m1])

        yList.sort()
        xList.sort()

    result = []
    for y in range(yList[0]+1, yList[-1]):
        intersec = []
        aux = []

        addedLines = []
        repeatedVertex = False
        for line in lines_table:
            if line[0] <= y and y < line[1]:
                x = line[3] * (y - line[0]) + line[2]
                intersec.append(round(x))

        intersec.sort()
        print(intersec)

        i = 0
        while i < len(intersec):
            aux.append([intersec[i], intersec[i + 1]])
            i += 2

        for x in range(xList[0]+1,xList[-1]):
            for a in aux:
                if a[0] <= x and x <= a[1]:
                    result.append([x,y])

        del intersec[:]
        del aux[:]

    return result






