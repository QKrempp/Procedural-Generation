import tkinter
import time
from PIL import Image, ImageDraw, ImageTk
import numpy as np


#   Données relatives à l'affichage
#-----------------------------------
sizeX       = 1600
sizeY       = 900
Ball_Radius = 10
#col_hex     = ["#7400b8", "#6930c3", "#5e60ce", "#5390d9", "#4ea8de", "#48bfe3", "#56cfe1", "#64dfdf", "#72efdd", "#80ffdb"]    # Palette de couleurs
delay       = 0.01    # Délai entre chaque frame

def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


#   Données physiques du problème
#---------------------------------
nbBody      = 20
speedRange  = 100
G           = 10000 # Constante gravitationnelle
t           = 0.01  # Unité de temps
eps         = 100   # Paramètre limitant les "collisions transparentes" sans lequel les corps peuvent se retrouver avec des vitesses quasi infinies après s'être passées à travers
coeff_fr    = 0.999 # Frottements, sans lesquels les vitesses augmentent fortement avec le temps (du fait des rebonds)
trainee     = 40
incert      = 1e-12  # Incertitude sur l'initialisation dans "circle_init"

class Sim:

    def __init__(self, color):
        self.col_hex = [color]
        self.M = 300 * np.ones((nbBody, 1))
        self.X = (sizeY / 3) * (np.cos(np.reshape(np.arange(0, nbBody), (nbBody, 1)) * 2 * np.pi / nbBody)) + sizeX / 2 + incert * np.random.random((nbBody, 1))
        self.Y = (sizeY / 3) * (np.sin(np.reshape(np.arange(0, nbBody), (nbBody, 1)) * 2 * np.pi / nbBody)) + sizeY / 2 + incert * np.random.random((nbBody, 1))
        self.VX = speedRange * np.cos(np.reshape(np.arange(0, nbBody), (nbBody, 1)) * 2 * np.pi / nbBody + np.pi / 2)
        self.VY = speedRange * np.sin(np.reshape(np.arange(0, nbBody), (nbBody, 1)) * 2 * np.pi / nbBody + np.pi / 2)
        self.AX = np.zeros((nbBody, 1))
        self.AY = np.zeros((nbBody, 1))
        self.X_toDraw = 20 * np.ones((nbBody, trainee))  # Positions des morceaux de tainée
        self.Y_toDraw = 20 * np.ones((nbBody, trainee))

    #   Fonctions de calcul du modèle physique discrétisé
    #-----------------------------------------------------
    def calc_acc(self):
        D = np.power(self.X @ np.ones((1, nbBody)) - np.ones((nbBody, 1)) @ self.X.T, 2) + np.power(self.Y @ np.ones((1, nbBody)) - np.ones((nbBody, 1)) @ self.Y.T, 2) + eps * np.ones((nbBody, nbBody))
        self.AX = -G * self.M * ((self.X @ np.ones((1, nbBody)) - np.ones((nbBody, 1)) @ self.X.T) * np.power(D, -3/2)) @ np.ones((nbBody, 1))
        self.AY = -G * self.M * ((self.Y @ np.ones((1, nbBody)) - np.ones((nbBody, 1)) @ self.Y.T) * np.power(D, -3/2)) @ np.ones((nbBody, 1))

    def calc_vit(self):
        self.VX = coeff_fr * (np.ones((nbBody, 1)) - 2 * ((self.X <= 0) + (self.X >= sizeX))) * self.VX + self.AX * t
        self.VY = coeff_fr * (np.ones((nbBody, 1)) - 2 * ((self.Y <= 0) + (self.Y >= sizeY))) * self.VY + self.AY * t

    def calc_pos(self):
        self.X = self.X + self.VX * t
        self.Y = self.Y + self.VY * t
        self.X_toDraw = np.concatenate((self.X_toDraw[:,1:], self.X), axis=1)
        self.Y_toDraw = np.concatenate((self.Y_toDraw[:,1:], self.Y), axis=1)

    def init_repr(self, canvas):
        self.balls = []
        for i in range(nbBody):       # Initialisation des données
            for j in range(trainee):
                k = trainee - (j + 1)
                self.balls.append(canvas.create_oval(int(self.X_toDraw[i,j]) - (Ball_Radius + int(self.M[i]) // 50), int(self.Y_toDraw[i,j]) - (Ball_Radius + int(self.M[i]) // 50), int(self.X_toDraw[i,j]) + (Ball_Radius + int(self.M[i]) // 50), int(self.Y_toDraw[i,j]) + (Ball_Radius + int(self.M[i]) // 50), fill=eclaircir(self.col_hex[i % len(self.col_hex)], k), width=0))

    def refresh(self, canvas):
        for j in range(trainee):    #Déplacement des corps
            for i in range(nbBody):
                canvas.coords(self.balls[i * trainee + j], int(self.X_toDraw[i,j]) - (Ball_Radius + int(self.M[i]) // 100), int(self.Y_toDraw[i,j]) - (Ball_Radius + int(self.M[i]) // 100), int(self.X_toDraw[i,j]) + (Ball_Radius + int(self.M[i]) // 100), int(self.Y_toDraw[i,j]) + (Ball_Radius + int(self.M[i]) // 100))

#   Fonctions outils pour l'animation
#-------------------------------------
def eclaircir(color, indice):
    col = hex_to_rgb(color)
    return rgb_to_hex((min(col[0] + indice * (255 // trainee), 255), min(col[1] + indice * (255 // trainee), 255), min(col[2] + indice * (255 // trainee), 255)))

def create_animation_window():
  Window = tkinter.Tk()
  Window.title("Problème des 3 corps")

  Window.geometry(str(sizeX) + "x" + str(sizeY))
  return Window

def create_animation_canvas(Window):
  canvas = tkinter.Canvas(Window)
  canvas.configure(bg="White")
  canvas.pack(fill="both", expand=True)
  return canvas


#   Boucle d'animation
#----------------------
def animate_ball(Window, canvas):
    A = Sim("#0000ff")
    B = Sim("#ff0000")
    A.init_repr(canvas)
    B.init_repr(canvas)
    while True:
        A.calc_acc()  # Actualisation des données du modèle
        A.calc_vit()
        A.calc_pos()
        B.calc_acc()  # Actualisation des données du modèle
        B.calc_vit()
        B.calc_pos()
        A.refresh(canvas)
        B.refresh(canvas)
        Window.update()
        time.sleep(delay)


#   Lancement du script
#-----------------------
Animation_Window = create_animation_window()
Animation_canvas = create_animation_canvas(Animation_Window)
animate_ball(Animation_Window,Animation_canvas)
