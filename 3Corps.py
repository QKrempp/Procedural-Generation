import tkinter
import time
from PIL import Image, ImageDraw, ImageTk
import numpy as np


#   Données relatives à l'affichage
#-----------------------------------
sizeX       = 1600
sizeY       = 900
Ball_Radius = 10
col_hex     = ["#7400b8", "#6930c3", "#5e60ce", "#5390d9", "#4ea8de", "#48bfe3", "#56cfe1", "#64dfdf", "#72efdd", "#80ffdb"]    # Palette de couleurs
delay       = 0.01    # Délai entre chaque frame

def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


#   Données physiques du problème
#---------------------------------
nbBody      = 30
speedRange  = 100
G           = 10000 # Constante gravitationnelle
t           = 0.01  # Unité de temps
eps         = 100   # Paramètre limitant les "collisions transparentes" sans lequel les corps peuvent se retrouver avec des vitesses quasi infinies après s'être passées à travers
coeff_fr    = 0.999 # Frottements, sans lesquels les vitesses augmentent fortement avec le temps (du fait des rebonds)
trainee     = 50
incert      = 1e-5  # Incertitude sur l'initialisation dans "circle_init"

AX = np.zeros((nbBody, 1))
AY = np.zeros((nbBody, 1))
X_toDraw = 20 * np.ones((nbBody, trainee))  # Positions des morceaux de tainée
Y_toDraw = 20 * np.ones((nbBody, trainee))


#   Initialisation aléatoire du problème
#----------------------------------------
def random_init():
    global M
    global X
    global Y
    global VX
    global VY
    M = np.random.randint(100, 1000, (nbBody, 1))
    X = sizeX * np.random.random((nbBody, 1))
    Y = sizeY * np.random.random((nbBody, 1))
    VX = speedRange * (np.random.random((nbBody, 1)) - 0.5)
    VY = speedRange * (np.random.random((nbBody, 1)) - 0.5)


#   Initialisation en cercle pour observer l'aspect chaotique du système entre deux simulations identiques à "incert" près
#--------------------------------------------------------------------------------------------------------------------------
def circle_init():
    global M
    global X
    global Y
    global VX
    global VY
    M = 300 * np.ones((nbBody, 1))
    X = (sizeY / 3) * (np.cos(np.reshape(np.arange(0, nbBody), (nbBody, 1)) * 2 * np.pi / nbBody)) + sizeX / 2 + incert * np.random.random((nbBody, 1))
    Y = (sizeY / 3) * (np.sin(np.reshape(np.arange(0, nbBody), (nbBody, 1)) * 2 * np.pi / nbBody)) + sizeY / 2 + incert * np.random.random((nbBody, 1))
    VX = 500 * np.cos(np.reshape(np.arange(0, nbBody), (nbBody, 1)) * 2 * np.pi / nbBody + np.pi / 2)
    VY = 500 * np.sin(np.reshape(np.arange(0, nbBody), (nbBody, 1)) * 2 * np.pi / nbBody + np.pi / 2)


#   Fonctions de calcul du modèle physique discrétisé
#-----------------------------------------------------
def calc_acc():
    global AX
    global AY
    D = np.power(X @ np.ones((1, nbBody)) - np.ones((nbBody, 1)) @ X.T, 2) + np.power(Y @ np.ones((1, nbBody)) - np.ones((nbBody, 1)) @ Y.T, 2) + eps * np.ones((nbBody, nbBody))
    AX = -G * M * ((X @ np.ones((1, nbBody)) - np.ones((nbBody, 1)) @ X.T) * np.power(D, -3/2)) @ np.ones((nbBody, 1))
    AY = -G * M * ((Y @ np.ones((1, nbBody)) - np.ones((nbBody, 1)) @ Y.T) * np.power(D, -3/2)) @ np.ones((nbBody, 1))

def calc_vit():
    global VX
    global VY
    VX = coeff_fr * (np.ones((nbBody, 1)) - 2 * ((X <= 0) + (X >= sizeX))) * VX + AX * t
    VY = coeff_fr * (np.ones((nbBody, 1)) - 2 * ((Y <= 0) + (Y >= sizeY))) * VY + AY * t

def calc_pos():
    global X
    global Y
    global X_toDraw
    global Y_toDraw
    X = X + VX * t
    Y = Y + VY * t
    X_toDraw = np.concatenate((X_toDraw[:,1:], X), axis=1)
    Y_toDraw = np.concatenate((Y_toDraw[:,1:], Y), axis=1)


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
  global X_toDraw
  global Y_toDraw
  balls = []
  for i in range(nbBody):       # Initialisation des données
      for j in range(trainee):
        k = trainee - (j + 1)
        balls.append(canvas.create_oval(int(X_toDraw[i,j]) - (Ball_Radius + int(M[i]) // 50), int(Y_toDraw[i,j]) - (Ball_Radius + int(M[i]) // 50), int(X_toDraw[i,j]) + (Ball_Radius + int(M[i]) // 50), int(Y_toDraw[i,j]) + (Ball_Radius + int(M[i]) // 50), fill=eclaircir(col_hex[i % len(col_hex)], k), width=0))
  while True:
    calc_acc()  # Actualisation des données du modèle
    calc_vit()
    calc_pos()
    for j in range(trainee):    #Déplacement des corps
        for i in range(nbBody):
            canvas.coords(balls[i * trainee + j], int(X_toDraw[i,j]) - (Ball_Radius + int(M[i]) // 100), int(Y_toDraw[i,j]) - (Ball_Radius + int(M[i]) // 100), int(X_toDraw[i,j]) + (Ball_Radius + int(M[i]) // 100), int(Y_toDraw[i,j]) + (Ball_Radius + int(M[i]) // 100))
    Window.update()
    time.sleep(delay)


#   Lancement du script
#-----------------------
circle_init()
Animation_Window = create_animation_window()
Animation_canvas = create_animation_canvas(Animation_Window)
animate_ball(Animation_Window,Animation_canvas)
