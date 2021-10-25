from tkinter import *
from math import cos, sin, pi
from random import random, randint

theta = pi / 7
decroiss = 1/250
feuilles = 50
N = 900

def from_rgb(rgb):
    return "#%02x%02x%02x" % rgb

class Branch:
    def __init__(self, anim, pos_x, pos_y, size, dir_x, dir_y, omega, prob, color):
        self.anim = anim
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size = size
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.omega = omega
        self.prob = prob
        self.color = color
    
    def draw_branch(self):
        anim.create_oval((int(self.pos_x + 3 * self.dir_x - self.size), int(self.pos_y + 3 * self.dir_y - self.size), int(self.pos_x + 3 * self.dir_x + self.size), int(self.pos_y + 3 * self.dir_y + self.size)), width = 0, fill=self.color)
        anim.create_oval((int(self.pos_x - self.size + 1), int(self.pos_y - self.size + 1), int(self.pos_x + self.size - 1), int(self.pos_y + self.size - 1)), width = 0, fill='black')

    def draw_leaves(self):
        r_x = randint(-feuilles, feuilles)
        r_y = randint(-feuilles, feuilles)
        r_c = random()
        feuille_size = 3 + randint(0, 3)
        anim.create_oval((int(self.pos_x) + r_x - feuille_size, int(self.pos_y) + r_y - feuille_size, int(self.pos_x) + r_x + feuille_size, int(self.pos_y) + r_y + feuille_size), width = 0, fill = from_rgb((255, int(r_c * 255), int(r_c * 128) + 127)))
            
    def update(self, tree):
        r = random()
        self.pos_x += self.dir_x
        self.pos_y += self.dir_y
        self.size *= (1 - decroiss)
        if r > self.prob:
            self.dir_x = self.dir_x * cos(self.omega) - self.dir_y * sin(self.omega)
            self.dir_y = self.dir_x * sin(self.omega) + self.dir_y * cos(self.omega)
            self.omega = 0.99 * self.omega +  (2 * random() - 1) / 3000
            self.prob *= (1 + decroiss)
        else:
            r = 1 - r
            s = 2 * randint(0, 1) - 1
            self.color = 'white'
            tree.append(Branch(anim, self.pos_x, self.pos_y, r * (1 - decroiss) * self.size, (cos(-s * (1 - r) * theta) * self.dir_x - sin(-s * (1 - r) * theta) * self.dir_y), (sin(-s * (1 - r) * theta) * self.dir_x + cos(-s * (1 - r) * theta) * self.dir_y), -self.omega, self.prob, 'white'))
            self.dir_x = self.dir_x * cos(s * r * theta) - self.dir_y * sin(s * r * theta)
            self.dir_y = self.dir_x * sin(s * r * theta) + self.dir_y * cos(s * r * theta)
            
fen = Tk()
fen.title("Tahuga!")
fen.geometry("1500x1000")

anim = Canvas(fen, width=1500, height = 1000, bd=0, bg = 'black')

def replay():
    anim.delete("all")
    
    Tree = [Branch(anim, 750, 1050, 100, 0, -1, 0, 0.0006, 'white')]
    
    N = 900
    while N > 0:
        for i in Tree:
            i.update(Tree)
        if N > 5:
            for i in Tree:
                i.draw_branch()
        else:
            for i in Tree:
                i.draw_leaves()
        anim.update()
        N -= 1

def reset():
    anim.delete("all")

replayButton = Button(fen, text = "Tahuga!", command=replay, bg = 'white')
#discardButton = Button(fen, text = "Reset", command = reset, bg = 'white')
replayButton.pack()
#discardButton.pack()
anim.pack()

fen.mainloop()
