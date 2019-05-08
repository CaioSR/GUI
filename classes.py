import functions
import option
import math

class Grid:

    def __init__(self, grid):
        self.xsize = grid[0]
        self.ysize = grid[1]

    def defineMatrix(self, matriz):
        self.matriz = matriz

class Point:

    def __init__(self, widget, point):
        self.x = point[0]
        self.y = point[1]
        self.point = point
        self.widget = widget

    def connectPoints(self, newPoint):
        return functions.bresenham([self.x,self.y], [newPoint.x, newPoint.y])

    def connectCircle(self, newPoint = None, radius = None):
        if newPoint:
            return functions.circle([self.x, self.y], p2 = [newPoint.x, newPoint.y])
        elif radius:
            return functions.circle([self.x, self.y], r = radius)

    def connectCurve(self, points, matriz, grid):
        points.insert(0,[self.x,self.y])
        points[1] = [points[1].x, points[1].y]
        points[2] = [points[2].x, points[2].y]
        points[3] = [points[3].x, points[3].y]
        return functions.curve(points, matriz, grid)

    def recursiveFill(self, grid, matriz):
        functions.recurFill(self.widget, matriz, grid)

    def movePoint(self, newPoint, matriz):
        self.point[0], self.point[1] = int(self.point[0] + newPoint[0]), int(self.point[1] + newPoint[1])
        self.x = self.point[0]
        self.y = self.point[1]
        self.widget = matriz[self.point[1]][self.point[0]]

    def rotatePoint(self, angle, matriz):
        radians = math.radians(angle)
        point = self.point[:]
        self.point[0] = round(point[0]*math.cos(radians) - point[1]*math.sin(radians))
        self.point[1] = round(point[0]*math.sin(radians) + point[1]*math.cos(radians))
        self.x = self.point[0]
        self.y = self.point[1]
        self.widget = matriz[self.point[1]][self.point[0]]

class Line:

    def __init__(self, line):
        self.point1 = line[0]
        self.point2 = line[-1]
        self.points = line

    def update(self, line):
        self.point1 = line[0]
        self.point2 = line[-1]
        self.points = line

    def connectLines(self, newLine):
        pass

    def delFirst(self):
        self.points.pop(0)

class Polyline:

    def __init__(self):
        self.lines = []
        self.fillment = []

    def addLine(self, line):
        self.lines.append(line)

    def mergePolyline(self, polyline):
        for line in polyline.lines:
            if line not in self.lines:
                line.delFirst()
                self.addLine(line)

    def ifVertex(self, line):

        for l in self.lines:
            if l.point1.x == line.point1.x and l.point1.y == line.point1.y:
                return True
            if l.point1.x == line.point2.x and l.point1.y == line.point2.y:
                return True
            if l.point2.x == line.point1.x and l.point2.y == line.point1.y:
                return True
            if l.point2.x == line.point2.x and l.point2.y == line.point2.y:
                return True
        return False

    def scanLine(self, matriz):

        self.fillment = []

        vertices = []

        for line in self.lines:
            if [line.points[0],line.points[-1]] not in vertices:
                vertices.append([line.points[0].point,line.points[-1].point])

        result = functions.scanLine(vertices)

        for point in result:
            self.fillment.append(Point(matriz[point[1]][point[0]], point))

    def translade(self, points, matriz):

        for l in self.lines:
            l.point1.movePoint(points, matriz)
            l.point2.movePoint(points, matriz)

        for l in self.lines:

            generated = l.point1.connectPoints(l.point2)
            transladed = []

            for point in generated:
                transladed.append(Point(matriz[point[1]][point[0]], point))

            l.update(transladed)


    def rotate(self, angle, matriz):

        point = self.lines[0].points[0].point[:]

        point[0],point[1] = point[0]*(-1),point[1]*(-1)
        self.translade(point, matriz)

        for l in self.lines:
            if l.point1.point != point:
                l.point1.rotatePoint(angle, matriz)
            if l.point2.point != point:
                l.point2.rotatePoint(angle, matriz)

        point[0],point[1] = point[0]*(-1),point[1]*(-1)
        self.translade(point, matriz)

        for l in self.lines:
            generated = l.point1.connectPoints(l.point2)
            rotated = []
            for point in generated:
                rotated.append(Point(matriz[point[1]][point[0]], point))

            l.update(rotated)

    def escale(self, escale, matriz):

        point = self.lines[0].points[0].point[:]

        point[0],point[1] = point[0]*(-1),point[1]*(-1)
        self.translade(point, matriz)

        for l in self.lines:
            l.point1.movePoint([escale[0]*l.point1.point[0]-l.point1.point[0], escale[1]*l.point1.point[1]-l.point1.point[1]], matriz)
            l.point2.movePoint([escale[0]*l.point2.point[0]-l.point2.point[0], escale[1]*l.point2.point[1]-l.point2.point[1]], matriz)

        point[0],point[1] = point[0]*(-1),point[1]*(-1)
        self.translade(point, matriz)

        for l in self.lines:
            generated = l.point1.connectPoints(l.point2)
            escaled = []
            for point in generated:
                escaled.append(Point(matriz[point[1]][point[0]], point))

            l.update(escaled)

class Circle:

    def __init__(self, center, r, circunference):
        self.center = center
        self.radius = r
        self.points = circunference

    def translade(self, points, matriz):

        self.center.movePoint(points, matriz)

        generated = self.center.connectCircle(radius = self.radius)
        transladed = []

        for point in generated:
            transladed.append(Point(matriz[point[1]][point[0]], point))

        self.points = transladed

    def escale(self, escale, matriz):

        self.radius = math.floor(self.radius*escale)

        generated = self.center.connectCircle(radius = self.radius)
        escalated = []

        for point in generated:
            escalated.append(Point(matriz[point[1]][point[0]], point))

        self.points = escalated

class Curve:

    def __init__(self, selectedPoints, generatedPoints):
        self.p = selectedPoints
        self.curve = generatedPoints

    def translade(self, points, matriz, grid = None):

        for point in self.p:
            point.movePoint(points, matriz)

        generated = self.p[0].connectCurve([self.p[1],self.p[2],self.p[3]], matriz, grid)
        transladed = []

        for point in generated:
            transladed.append(Point(matriz[point[1]][point[0]], point))

        self.curve = transladed

    def rotate(self, angle, matriz, grid = None):

        pivot = self.p[0].point[:]

        pivot[0],pivot[1] = pivot[0]*(-1),pivot[1]*(-1)
        self.translade(pivot, matriz, grid = grid)

        for point in self.p:
            if point.point != pivot:
                point.rotatePoint(angle, matriz)

        pivot[0],pivot[1] = pivot[0]*(-1), pivot[1]*(-1)
        self.translade(pivot, matriz, grid = grid)

        generated = self.p[0].connectCurve([self.p[1], self.p[2], self.p[3]], matriz, grid)
        rotated = []

        for point in generated:
            rotated.append(Point(matriz[point[1]][point[0]], point))

        self.curve = rotated

    def escale(self, escale, matriz, grid = None):

        pivot = self.p[0].point[:]

        pivot[0],pivot[1] = pivot[0]*(-1),pivot[1]*(-1)
        self.translade(pivot, matriz, grid = grid)

        for p in self.p:
            p.movePoint([escale[0]*p.point[0]-p.point[0], escale[1]*p.point[1]-p.point[1]], matriz)

        pivot[0],pivot[1] = pivot[0]*(-1), pivot[1]*(-1)
        self.translade(pivot, matriz, grid = grid)

        generated = self.p[0].connectCurve([self.p[1], self.p[2], self.p[3]], matriz, grid)
        escalated = []

        for point in generated:
            escalated.append(Point(matriz[point[1]][point[0]], point))

        self.curve = escalated
