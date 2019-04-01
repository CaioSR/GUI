def bresenham(grid_xsize, grid_ysize,p,matriz):
    try:
        mR,xR,yR = 0,0,0
        
        p1 = str(p[-2])
        p2 = str(p[-1])

        p1 = int(p1[15:])
        p2 = int(p2[15:])

        p1 = [p1 % grid_xsize - 1, p1 // grid_xsize]
        p2 = [p2 % grid_xsize - 1, p2 // grid_xsize]

        print(p1,p2)

        try:
            m = (p2[1]-p1[1])/(p2[0]-p1[0])
        except:
            m = 2

        if m > 1 or m < -1:
            print(p1,p2,m)
            p1[0],p1[1]=p1[1],p1[0]
            p2[0],p2[1]=p2[1],p2[0]
            mR = 1

        if p1[0] > p2[0]:
            print(p1[0],p2[0])
            p1[0] = p1[0]*(-1)
            p2[0] = p2[0]*(-1)
            xR = 1

        if p1[1] > p2[1] :
            print(p1[1],p2[1])
            p1[1] = p1[1]*(-1)
            p2[1] = p2[1]*(-1)
            yR = 1

        x = p1[0]
        y = p1[1]

        m = (p2[1]-p1[1])/(p2[0]-p1[0])
        print(p1,p2,m)

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
            print(mR,xR,yR)
            for p in list:
                
                if mR == 1:
                    p[0],p[1] = p[1],p[0]

                if xR == 1:
                    p[0] = p[0]*(-1)

                if yR == 1:
                    p[1] = p[1]*(-1)
                    
                list[list.index(p)] = p

        for point in list:
            matriz[point[1]][point[0]].configure(bg='blue')

        print(list)

    except:
        pass
