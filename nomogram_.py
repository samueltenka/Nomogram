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
randpt = lambda scale: [(random()-0.5)*scale for i in range(2)]

from tkinter import *
master = Tk()
width=640; height=480
w = Canvas(master, height=height, width=width)
class snake:
    def __init__(self, numpts, bondlength, viscosity, endslooseness, springkons, start, end):
        self.pts = [plus(randpt(0.1),plus(scale(1.0-i/float(numpts-1), start), scale(i/float(numpts-1), end))) for i in range(numpts)]
        self.moms = [zero() for i in range(len(self))]
        self.pts[0] = start; self.pts[-1] = end
        self.bondlength, self.viscosity, self.springkons, self.endslooseness = bondlength, viscosity, springkons, endslooseness
        self.vals = [float(i)/(len(self)-1) for i in range(len(self))]
    def __len__(self):
        return len(self.pts)
    def init_forces(self):
        self.forces = [zero() for i in range(len(self))]
    def compute_spring(self):
        for i in range(len(self)-1):
            diffvec = minus(self.pts[i+1], self.pts[i])
            discomfort = norm(diffvec)-self.bondlength
            sign = discomfort/abs(discomfort)
            self.forces[i] = plus(self.forces[i], scale(self.springkons*sign, diffvec))
            self.forces[i+1] = plus(self.forces[i+1], scale(-self.springkons*sign,diffvec))
    def compute_visco(self):
        for i in range(len(self)):
            self.forces[i] = plus(self.forces[i], scale(-self.viscosity, self.moms[i]))
    def compute_nomo(self, o2, o3, me_func, kons=1.0, thoroughness=1):
        # idea: randomly sample ~sqrt of these O(n^2) combinations?
        # idea: uniformly sample ~sqrt of these O(n^2) combinations?
        acc = 0.0
        for r in range(len(self)*thoroughness):
            j = randrange(len(o2))
            k = randrange(len(o3))

            i = int(me_func(o2.vals[j],o3.vals[k])*len(self))
            if not (0<=i<len(self)): continue
            paravec = minus(o3.pts[k],o2.pts[j])
            perpvec = rot(paravec); n=norm(perpvec)
            perpvec = [p/n for p in perpvec]
            dist = dot(self.pts[i],perpvec) - dot(o3.pts[k],perpvec)
            acc += abs(dist)

            self.forces[i] = plus(self.forces[i], scale(-kons*dist, perpvec))
        if random()<0.1:
            print('acc=%f' % (acc/(len(self)*thoroughness)))
    def step(self, dt):
        #self.moms[0] = scale(self.endslooseness,self.moms[0])
        #self.moms[-1] = scale(self.endslooseness,self.moms[-1])
        self.forces[0] = scale(self.endslooseness,self.forces[0])
        self.forces[-1] = scale(self.endslooseness,self.forces[-1])
        for i in range(len(self)): # don't update ends
            for j in range(2):
               self.moms[i][j] += dt*self.forces[i][j]
               self.pts[i][j] += dt*self.moms[i][j]

    def graph(self, canvas):
        for i in range(len(self)-1):
            w.create_line((self.pts[i  ][0]+1.0)/2 * width,(self.pts[i  ][1]+1.0)/2 * height,
                          (self.pts[i+1][0]+1.0)/2 * width,(self.pts[i+1][1]+1.0)/2 * height,
                          fill='#'+'00'+hex(int(self.vals[i]*256))[2:].rjust(2,'0')*2)

A = snake(30, start=[-0.9,-0.9], end=[-0.9,0.9], bondlength=0.04, viscosity=1.0, springkons=0.1, endslooseness=0.0)
X = snake(40, start=[0.0,-0.9], end=[0.0,0.9], bondlength=0.03, viscosity=1.0, springkons=0.01, endslooseness=0.1 )
B = snake(30, start=[+0.9,-0.9], end=[+0.9,0.9], bondlength=0.04, viscosity=1.0, springkons=0.1, endslooseness=0.0)
snakes =  [A,X,B]
#to_a = lambda x,b: 2*x**0.5-b
#to_x = lambda a,b: ((a+b)/2)**2
#to_b = lambda a,x: 2*x**0.5-a

to_a = lambda x,b: (3*x-b)/2
to_x = lambda a,b: (2*a+b)/3
to_b = lambda a,x: 3*x-2*a

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
   #A.compute_nomo(X,B,to_a, kons=0.01)
   X.compute_nomo(A,B,to_x, kons=1.0)
   #B.compute_nomo(A,X,to_b, kons=0.01)
   for S in snakes:
       S.step(0.1)
   STEP+=1
   w.after(5, render) #render 200 times a second
render()
mainloop()
