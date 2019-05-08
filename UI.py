from tkinter import *
import ast
import classes
import option

#frameBuffer = {}

root = Tk()

p=[]
l=[]
po=[]
c=[]
cur=[]
editLines=[]
editPoints=[]
selected=None
grid = classes.Grid([50,30])

def selectedBlank(selected):
    if isinstance(selected, classes.Polyline):

        for line in selected.lines:
            for point in line.points:
                point.widget.configure(bg='white')

        if selected.fillment:
            for point in selected.fillment:
                point.widget.configure(bg='white')

    elif isinstance(selected, classes.Circle):

        for point in selected.points:
            point.widget.configure(bg='white')

    elif isinstance(selected, classes.Curve):

        for point in selected.curve:
            point.widget.configure(bg='white')

def releventPoint(widget):
    widget.configure(bg="black")
    point = option.getCoordinates(grid, widget)
    p.append(classes.Point(widget, point))

def editPoint(widget):
    global selected

    if widget['bg'] == 'blue':
        for poly in po:
            for li in poly.lines:
                for point in li.points:
                    if point.widget == widget:
                        selected = poly

            if selected:
                for li in poly.lines:
                    for point in li.points:
                        point.widget.configure(bg='red')
                break

        for circle in c:
            for point in circle.points:
                if point.widget == widget:
                    selected = circle

            if selected:
                for point in circle.points:
                    point.widget.configure(bg='red')

        for curve in cur:
            for point in curve.curve:
                if point.widget == widget:
                    selected = curve

            if selected:
                for point in curve.curve:
                    point.widget.configure(bg='red')


def clearAll(widget):
    for i in range(grid.ysize):
        for j in range(grid.xsize):
            widget[i][j].configure(bg="white")

    del p[:]
    del l[:]
    del po[:]
    del c[:]
    del cur[:]
    global selected
    selected = None

def translade(translade,selected):

    selectedBlank(selected)

    points = translade.get()
    points = ast.literal_eval(points)


    if isinstance(selected, classes.Polyline):

        selected.translade(points, matriz)

        if selected.fillment: scanLine(selected)

        for line in selected.lines:
            for point in line.points:
                point.widget.configure(bg='red')

    if isinstance(selected, classes.Circle):

        selected.translade(points, matriz)

        for point in selected.points:
            point.widget.configure(bg='red')

    if isinstance(selected, classes.Curve):

        selected.translade(points, matriz, grid = grid)

        for point in selected.curve:
            point.widget.configure(bg='red')

def rotate(angle,selected):
    selectedBlank(selected)

    angle = angle.get()
    angle = int(angle)

    if isinstance(selected, classes.Polyline):

        selected.rotate(angle, matriz)

        if selected.fillment: scanLine(selected)

        for line in selected.lines:
            for points in line.points:
                points.widget.configure(bg='red')

    elif isinstance(selected, classes.Curve):

        selected.rotate(angle, matriz, grid = grid)

        for point in selected.curve:
            point.widget.configure(bg='red')

def escale(escale, selected):

    selectedBlank(selected)

    escale = escale.get()
    escale = ast.literal_eval(escale)


    if isinstance(selected, classes.Polyline):

        selected.escale(escale, matriz)

        if selected.fillment: scanLine(selected)

        for line in selected.lines:
            for point in line.points:
                point.widget.configure(bg='red')

    elif isinstance(selected, classes.Circle):

        selected.escale(escale, matriz)

        for point in selected.points:
            point.widget.configure(bg='red')

    elif isinstance(selected, classes.Curve):

        selected.escale(escale, matriz, grid = grid)

        for point in selected.curve:
            point.widget.configure(bg='red')

def scanLine(selected):
    if isinstance(selected, classes.Polyline):

        selected.scanLine(matriz)

        for point in selected.fillment:
            point.widget.configure(bg='blue')

        for lines in selected.lines:
            for point in lines.points:
                point.widget.configure(bg='red')

def recursiveFill():
    p[-1].recursiveFill(grid,matriz)

    del p[:]

def drawLine():
    generatedPoints = p[-2].connectPoints(p[-1])

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

    del p[:]

def drawCircle():

    r, generatedPoints = p[-2].connectCircle(newPoint = p[-1])

    circle = []
    for point in generatedPoints:
        if point[0] >= 0 and point[1] >= 0 and point[0] <= grid.xsize-1 and point[1] <= grid.ysize-1:
            circle.append(classes.Point(matriz[point[1]][point[0]], point))

    p[-2].widget.configure(bg='white')
    p[-1].widget.configure(bg='white')

    for point in circle:
        point.widget.configure(bg='blue')

    c.append(classes.Circle(p[-2], r, circle))

    del p[:]

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

    del p[:]

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

scan = Button(buttonFrame, text="Scan Line", command=lambda : scanLine(selected))
scan.pack(side=LEFT, padx=5)

#buffer = Button(buttonFrame, text="Return buffer", command=lambda : printBuffer())
#buffer.pack(side=LEFT, padx=5)

input_Translad = Button(inputFrame, text="Transladar [T1,T2]", command=lambda : translade(trans_input, selected))
input_Translad.pack(side=TOP, padx=5)
trans_input = StringVar()
inputTrans_box = Entry(inputFrame, textvariable=trans_input)
inputTrans_box.pack()

input_Rotation = Button(inputFrame, text="Rotacionar X", command=lambda : rotate(angle_input, selected))
input_Rotation.pack(side=TOP, padx=5)
angle_input = StringVar()
inputAngle_box = Entry(inputFrame, textvariable=angle_input)
inputAngle_box.pack()

input_Escalation = Button(inputFrame, text="Escalar [S1,S2]", command=lambda : escale(escale_input, selected))
input_Escalation.pack(side=TOP, padx=5)
escale_input = StringVar()
inputEscale_box = Entry(inputFrame, textvariable=escale_input)
inputEscale_box.pack()


clear = Button(buttonFrame, text="Clear", fg="Red", command=lambda : clearAll(matriz) )
clear.pack(side=RIGHT, padx=10)

root.mainloop()
