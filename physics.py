''' nomograms by gradient descent
'''
from tkinter import *
from random import random
from math import sin, sqrt
master = Tk()

width=640; height=480
w = Canvas(master, height=height, width=width)
mesh=100
nodes = [i/float(mesh) for i in range(mesh)]
def graph(function, canvas):
    fs = [function(n) for n in nodes]
    for i in range(mesh-1):
        w.create_line((nodes[i  ]+1.0)/2 * width,(fs[i  ]+1.0)/2 * height,
                      (nodes[i+1]+1.0)/2 * width,(fs[i+1]+1.0)/2 * height)
#graph(lambda x: sin(x*6), w)

class snake:
    def __init__(self, numpts, bondlength=0.01, start=[-0.9,-0.9], end=[0.9,0.9]):
        self.pts = [[random()*0.1, random()*0.1] for i in range(numpts)]
        self.moms = [[0.0,0.0] for i in range(len(self.pts))]
        self.pts[0] = start; self.pts[-1] = end
        self.bondlength = bondlength
    def step(self, dt, visco=0.1):
        self.forces = [[0.0, 0.0] for i in range(len(self.pts))]
        for i in range(len(self.pts)-1):
            dist = sqrt(sum((self.pts[i+1][j]-self.pts[i][j])**2 for j in range(2)))
            diff = dist-self.bondlength
            sign = diff/abs(diff)
            for j in range(2):
               self.forces[i][j] += (self.pts[i+1][j] - self.pts[i][j]) * sign
               self.forces[i+1][j] -= (self.pts[i+1][j] - self.pts[i][j]) * sign
        for i in range(len(self.pts)):
            for j in range(2):
               self.forces[i][j] -= visco*self.moms[i][j]
        for i in range(len(self.pts)):
            for j in range(2):
               self.moms[i][j] += dt*self.forces[i][j]
        for i in range(1,len(self.pts)-1):
            for j in range(2):
               self.pts[i][j] += dt*self.moms[i][j]
    def graph(self, canvas):
        for i in range(len(self.pts)-1):
            w.create_line((self.pts[i  ][0]+1.0)/2 * width,(self.pts[i  ][1]+1.0)/2 * height,
                          (self.pts[i+1][0]+1.0)/2 * width,(self.pts[i+1][1]+1.0)/2 * height)

S = snake(100, bondlength=0.025)

w.pack()
STEP=0
def render():
   global w, STEP
   if STEP%10==0:
      w.delete('all')
      S.graph(w)
   S.step(0.1)
   STEP+=1
   w.after(5, render) #render 200 times a second
render()
mainloop()
