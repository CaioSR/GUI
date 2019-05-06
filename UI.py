from tkinter import *
import ast
import classes
import option

frameBuffer = {}

root = Tk()

p=[]
l=[]
po=[]
c=[]
cur=[]
editLines=[]
editPoints=[]
grid = classes.Grid([50,30])

def releventPoint(widget):
    widget.configure(bg="black")
    point = option.getCoordinates(grid, widget)
    p.append(classes.Point(widget, point))

def editPoint(widget):
    chosen = False
    leave = False

    if widget['bg'] == 'red':
        for poly in po:
            for line in editLines:
                if line in poly.lines:
                    chosen=True

                if chosen:
                    for li in poly.lines:
                        if li.points != line.points:
                            for point in li.points:
                                point.widget.configure(bg='red')
                    global selectedPolygon
                    selectedPolygon=poly
                    leave = True
                    editLines.remove(line)
                    break
            if leave:
                break

    if widget['bg'] == 'blue':
        for li in l:
            for point in li.points:
                if point.widget == widget:
                    chosen = True
                    editLines.append(li)
                    break
            if chosen:
                for point in li.points:
                    point.widget.configure(bg='red')
                    editPoints.append(point)
                break

def clearAll(widget):
    for i in range(grid.ysize):
        for j in range(grid.xsize):
            widget[i][j].configure(bg="white")

    del p[:]
    del l[:]
    del po[:]
    del c[:]
    del cur[:]
    del editLines[:]
    del editPoints[:]

def translade(translade):
    points = translade.get()
    points = ast.literal_eval(points)
    selectedPolygon.translade(points, matriz)

def rotate(angle):
    angle = angle.get()
    angle = int(angle)
    selectedPolygon.rotate(angle, matriz)

def drawLine():
    generatedPoints = p[-2].connectPoints(p[-1], matriz)

    line = []
    for point in generatedPoints:
        line.append(classes.Point(matriz[point[1]][point[0]], point))

    for point in line:
        point.widget.configure(bg='blue')

    l.append(classes.Line(line))

    newLine = l[-1]

    if l == []:
        newPoly = classes.Polyline()
        newPoly.addLine(newLine)
        po.append(newPoly)

    else:
        added = False
        polylineFound = None

        for poly in po:
            if poly.ifVertex(newLine):
                polylineFound = poly
                poly.addLine(newLine)
                added = True

        if polylineFound:
            for poly in po:
                if poly.ifVertex(newLine) and poly != polylineFound:
                    polylineFound.mergePolyline(poly)
                    po.remove(poly)

        if not added:
            newPoly = classes.Polyline()
            newPoly.addLine(newLine)
            po.append(newPoly)

    l.append(newLine)

def drawCircle():

    r, generatedPoints = p[-2].connectCircle(p[-1], matriz)

    circle = []
    for point in generatedPoints:
        if point[0] >= 0 and point[1] >= 0 and point[0] <= grid.xsize-1 and point[1] <= grid.ysize-1:
            circle.append(classes.Point(matriz[point[1]][point[0]], point))

    p[-2].widget.configure(bg='white')
    p[-1].widget.configure(bg='white')

    for point in circle:
        point.widget.configure(bg='blue')

    c.append(classes.Circle(p[-2], r, circle))


def drawCurve():
    points = [p[-4],p[-3],p[-2],p[-1]]

    generatedPoints = p[-4].connectCurve([p[-3], p[-2], p[-1]], matriz, grid)

    curve = []
    for point in generatedPoints:
        curve.append(classes.Point(matriz[point[1]][point[0]], point))

    for point in points:
        point.widget.configure(bg='white')

    for point in curve:
        point.widget.configure(bg='blue')

    cur.append(classes.Curve(points, curve))


def recursiveFill():
    p[-1].recursiveFill(grid,matriz)

def scanLine():
    generatedPoints = selectedPolygon.scanLine(grid, matriz)

    for point in generatedPoints:
        matriz[point[1]][point[0]].configure(bg='blue')

buttonFrame = Frame(root)
buttonFrame.grid(row=0,column=0, sticky=W, padx=5, pady=5)

inputFrame = Frame(root)
inputFrame.grid(row=1,column=1, sticky=N)

gridFrame = Frame(root)
gridFrame.grid(row=1,column=0)

matriz,linha=[],[]
for i in range(grid.ysize):
    for j in range(grid.xsize):
        linha.append(Frame(gridFrame,bg="white",height=15,width=15,bd=1,relief=SUNKEN))
    matriz.append(linha)
    linha=[]

for i in range(grid.ysize):
    for j in range(grid.xsize):
        matriz[i][j].bind("<Button-1>", lambda event, widget=matriz[i][j] : releventPoint(widget))
        #matriz[i][j].bind("<Button-2>", lambda event, widget=matriz[i][j] : editPoint(widget))
        matriz[i][j].bind("<Button-3>", lambda event, widget=matriz[i][j] : editPoint(widget))
        matriz[i][j].grid(row=i,column=j)

grid.defineMatrix(matriz)

linha = Button(buttonFrame, text="Bresenham", command=lambda : drawLine())
linha.pack(side=LEFT, padx=5)

circulo = Button(buttonFrame, text="Circulo", command=lambda : drawCircle())
circulo.pack(side=LEFT, padx=5)

curva = Button(buttonFrame, text="Curva [4]", command=lambda : drawCurve())
curva.pack(side=LEFT, padx=5)

recur = Button(buttonFrame, text="Preenchimento Recursivo", command=lambda : recursiveFill())
recur.pack(side=LEFT, padx=5)

scan = Button(buttonFrame, text="Scan Line [N funciona]", command=lambda : scanLine())
scan.pack(side=LEFT, padx=5)

buffer = Button(buttonFrame, text="Return buffer", command=lambda : printBuffer())
buffer.pack(side=LEFT, padx=5)

input_Translad = Button(inputFrame, text="Transladar [T1,T2]", command=lambda : translade(trans_input))
input_Translad.pack(side=TOP, padx=5)
trans_input = StringVar()
inputTrans_box = Entry(inputFrame, textvariable=trans_input)
inputTrans_box.pack()

input_Rotation = Button(inputFrame, text="Rotacionar X", command=lambda : rotate(angle_input))
input_Rotation.pack(side=TOP, padx=5)
angle_input = StringVar()
inputAngle_box = Entry(inputFrame, textvariable=angle_input)
inputAngle_box.pack()

clear = Button(buttonFrame, text="Clear", fg="Red", command=lambda : clearAll(matriz) )
clear.pack(side=RIGHT, padx=10)

root.mainloop()
