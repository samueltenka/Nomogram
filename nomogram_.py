''' nomograms by gradient descent
'''
from random import random
from math import sqrt

dot = lambda v,w: sum(v[i]*w[i] for i in range(2))
norm = lambda v: sqrt(dot(v,v))
rot = lambda v: [-v[1],v[0]]
plus = lambda v,w: [v[i]+w[i] for i in range(2)]
minus = lambda v,w: [v[i]-w[i] for i in range(2)]

from tkinter import *
master = Tk()
width=640; height=480
w = Canvas(master, height=height, width=width)
class snake:
    def __init__(self, numpts, bondlength=0.01, start=[-0.9,-0.9], end=[0.9,0.9]):
        self.pts = [[random()*0.1, random()*0.1] for i in range(numpts)]
        self.moms = [[0.0,0.0] for i in range(len(self))]
        self.pts[0] = start; self.pts[-1] = end
        self.bondlength = bondlength
        self.vals = [float(i)/len(self) for i in range(len(self))]
    def __len__(self):
        return len(self.pts)
    def init_forces(self):
        self.forces = [[0.0, 0.0] for i in range(len(self))]
    def compute_spring(self, k=1.0):
        for i in range(len(self)-1):
            dist = sqrt(sum((self.pts[i+1][j]-self.pts[i][j])**2 for j in range(2)))
            diff = dist-self.bondlength
            sign = diff/abs(diff)
            for j in range(2):
               self.forces[i][j] += k*(self.pts[i+1][j] - self.pts[i][j]) * sign
               self.forces[i+1][j] -= k*(self.pts[i+1][j] - self.pts[i][j]) * sign
    def compute_visco(self, visco=0.1):
        for i in range(len(self)):
            for j in range(2):
               self.forces[i][j] -= visco*self.moms[i][j]
    def compute_nomo(self, o2, o3, me_func):
        for j in range(len(o2)-1):
            for k in range(len(o3)-1):
                i = int(me_func(o2.vals[j],o3.vals[k])*len(self))
                if not (0<=i<len(self)): continue
                paravec = minus(o3.pts[k],o2.pts[j])
                perpvec = rot(paravec); n=norm(perpvec)
                perpvec = [p/n for p in perpvec]
            for j in range(2):
               self.forces[i][j] += k*(self.pts[i+1][j] - self.pts[i][j]) * sign
               self.forces[i+1][j] -= k*(self.pts[i+1][j] - self.pts[i][j]) * sign
    def step(self, dt):
        for i in range(1, len(self)-1): # don't update ends
            for j in range(2):
               self.moms[i][j] += dt*self.forces[i][j]
               self.pts[i][j] += dt*self.moms[i][j]

    def graph(self, canvas):
        for i in range(len(self)-1):
            w.create_line((self.pts[i  ][0]+1.0)/2 * width,(self.pts[i  ][1]+1.0)/2 * height,
                          (self.pts[i+1][0]+1.0)/2 * width,(self.pts[i+1][1]+1.0)/2 * height,
                          fill='#'+'00'+hex(int(self.vals[i]*256))[2:].rjust(2,'0')*2)

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
