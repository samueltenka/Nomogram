''' nomograms by gradient descent
'''
from random import random, randrange
from math import sqrt

dot = lambda v,w: sum(v[i]*w[i] for i in range(2))
norm = lambda v: sqrt(dot(v,v))
rot = lambda v: [-v[1],v[0]]
scale = lambda l,v: [l*v[i] for i in range(2)]
plus = lambda v,w: [v[i]+w[i] for i in range(2)]
minus = lambda v,w: [v[i]-w[i] for i in range(2)]
zero = lambda: [0.0 for i in range(2)]
randpt = lambda scale: [random()*scale for i in range(2)]

from tkinter import *
master = Tk()
width=640; height=480
w = Canvas(master, height=height, width=width)
class snake:
    def __init__(self, numpts, bondlength, start, end):
        self.pts = [plus(randpt(0.01),plus(scale(1.0-i/float(numpts-1), start), scale(i/float(numpts-1), end))) for i in range(numpts)]
        self.moms = [zero() for i in range(len(self))]
        #self.pts[0] = start; self.pts[-1] = end
        self.bondlength = bondlength
        self.vals = [float(i)/(len(self)-1) for i in range(len(self))]
    def __len__(self):
        return len(self.pts)
    def init_forces(self):
        self.forces = [zero() for i in range(len(self))]
    def compute_spring(self, kons=0.1): #beware, k is iteration dummy!
        for i in range(len(self)-1):
            diffvec = minus(self.pts[i+1], self.pts[i])
            discomfort = norm(diffvec)-self.bondlength
            sign = discomfort/abs(discomfort)
            self.forces[i] = plus(self.forces[i], scale(kons*sign, diffvec))
            self.forces[i+1] = plus(self.forces[i+1], scale(-kons*sign,diffvec))
    def compute_visco(self, visco=1.0):
        for i in range(len(self)):
            self.forces[i] = plus(self.forces[i], scale(-visco, self.moms[i]))
    def compute_nomo(self, o2, o3, me_func, kons=1.0):
        # idea: randomly sample ~sqrt of these O(n^2) combinations?
        # idea: uniformly sample ~sqrt of these O(n^2) combinations?
        for r in range(len(self)):
            j = randrange(len(o2))
            k = randrange(len(o3))

            i = int(me_func(o2.vals[j],o3.vals[k])*len(self))
            if not (0<=i<len(self)): continue
            paravec = minus(o3.pts[k],o2.pts[j])
            perpvec = rot(paravec); n=norm(perpvec)
            perpvec = [p/n for p in perpvec]
            dist = dot(self.pts[i],perpvec) - dot(o3.pts[k],perpvec)

            self.forces[i] = plus(self.forces[i], scale(-kons*dist, perpvec))

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

A = snake(30, start=(-0.9,-0.9), end=(-0.9,0.9), bondlength=0.03)
X = snake(30, start=(0.0,-0.9), end=(0.0,0.9), bondlength=0.03)
B = snake(30, start=(+0.9,-0.9), end=(+0.9,0.9), bondlength=0.03)
snakes =  [A,X,B]
to_a = lambda x,b: 2*x-b
to_x = lambda a,b: (a+b)/2
to_b = lambda a,x: 2*x-a

w.pack()
STEP=0
def render():
   global w, STEP
   if STEP%10==0:
      w.delete('all')
      for S in snakes:
          S.graph(w)
   for S in snakes:
       S.init_forces()
       S.compute_spring()
       S.compute_visco()
   A.compute_nomo(X,B,to_a)
   X.compute_nomo(A,B,to_x)
   B.compute_nomo(A,X,to_b)
   for S in snakes:
       S.step(0.1)
   STEP+=1
   w.after(5, render) #render 200 times a second
render()
mainloop()
