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

    def connectPoints(self, newPoint, matriz):
        return functions.bresenham([self.x,self.y], [newPoint.x, newPoint.y], matriz)

    def connectCircle(self, newPoint, matriz):
        return functions.circle([self.x, self.y], [newPoint.x, newPoint.y], matriz)

    def connectCurve(self, points, matriz, grid):
        points.insert(0,[self.x,self.y])
        points[1] = [points[1].x, points[1].y]
        points[2] = [points[2].x, points[2].y]
        points[3] = [points[3].x, points[3].y]
        return functions.curve(points, matriz, grid)

    def recursiveFill(self, grid, matriz):
        functions.recurFill(self.widget, matriz, grid)

    def movePoint(self, newPoint, matriz):
        self.widget.configure(bg='white')
        self.point[0], self.point[1] = self.point[0] + newPoint[0], self.point[1] + newPoint[1]
        self.x = self.point[0]
        self.y = self.point[1]
        self.widget = matriz[self.point[1]][self.point[0]]
        self.widget.configure(bg='blue')

    def rotatePoint(self, angle, matriz):
        self.widget.configure(bg='white')
        radians = math.radians(angle)
        point = self.point[:]
        print(self.point)
        self.point[0] = math.floor(point[0]*math.cos(radians) - point[1]*math.sin(radians)) #erros
        self.point[1] = math.floor(point[0]*math.sin(radians) + point[1]*math.cos(radians))
        self.x = self.point[0]
        self.y = self.point[1]
        print(self.point)
        self.widget = matriz[self.point[1]][self.point[0]]
        self.widget.configure(bg='blue')

class Line:

    def __init__(self, line):
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

    def scanLine(self, grid, matriz):

        vertices = []

        for line in self.lines:
            if [line.points[0],line.points[-1]] not in vertices:
                vertices.append([line.points[0].point,line.points[-1].point])

        return functions.scanLine(vertices)


    def translade(self, points, matriz):

        for l in self.lines:
            for p in l.points:
                p.movePoint(points, matriz)


    def rotate(self, angle, matriz):

        point = self.lines[0].points[0].point[:]

        """
        for l in self.lines:
            if option.distance(l.points[0].point,[0,0]) < option.distance(point,[0,0]):
                point = l.points[0].point[:]
            if option.distance(l.points[-1].point,[0,0]) < option.distance(point,[0,0]):
                point = l.points[0].point[:]
        """


        point[0],point[1] = point[0]*(-1),point[1]*(-1)
        self.translade(point, matriz)

        for l in self.lines:
            for p in l.points:
                p.rotatePoint(angle, matriz)

        point[0],point[1] = point[0]*(-1),point[1]*(-1)
        self.translade(point, matriz)


    def escale(self):
        pass

class Circle:

    def __init__(self, center, r, circunference):
        self.center = center
        self.radius = r
        self.points = circunference

class Curve:

    def __init__(self, selectedPoints, generatedPoints):
        self.p = selectedPoints
        self.curve = generatedPoints