from tkinter import *
from bresenham_gui import *

root = Tk()

p=[]
def releventPoint(widget):
    widget.configure(bg='black')
    p.append(widget)

def irreleventPoint(widget):
    widget.configure(bg='red')

def clearPoint(widget):
    if widget['bg'] == 'black':
        p.remove(widget)
    widget.configure(bg='white')

def clearAll(widget):
    for i in range(grid_ysize):
        for j in range(grid_xsize):
            widget[i][j].configure(bg='white')

buttonFrame = Frame(root)
buttonFrame.grid(row=0,column=0,sticky=W, padx=5, pady=5)
gridFrame = Frame(root)
gridFrame.grid(row=1,column=0)
grid_xsize = 70
grid_ysize = 30

matriz,linha=[],[]
for i in range(grid_ysize):
    for j in range(grid_xsize):
        linha.append(Frame(gridFrame,bg='white',height=15,width=15,bd=1,relief=SUNKEN))
    matriz.append(linha)
    linha=[]

for i in range(grid_ysize):
    for j in range(grid_xsize):
        matriz[i][j].bind('<Button-1>', lambda event, widget=matriz[i][j] : releventPoint(widget))
        matriz[i][j].bind('<Button-2>', lambda event, widget=matriz[i][j] : irreleventPoint(widget))
        matriz[i][j].bind('<Button-3>', lambda event, widget=matriz[i][j] : clearPoint(widget))
        matriz[i][j].grid(row=i,column=j)


linha = Button(buttonFrame, text='Bresenham', command=lambda : bresenham(grid_xsize, grid_ysize,p,matriz))
linha.pack(side=LEFT)

circulo = Button(buttonFrame, text='Circulo')
circulo.pack(side=LEFT, padx=5)

curva = Button(buttonFrame, text='Curva')
curva.pack(side=LEFT, padx=5)

clear = Button(buttonFrame, text='Clear', fg='Red', command=lambda : clearAll(matriz) )
clear.pack(side=RIGHT, padx=10)

root.mainloop()
