from tkinter import *
import numpy as np
from PIL import Image, ImageTk
from datetime import datetime

now = datetime.now()


# Palettes de couleurs
#----------------------
#col_hex = ["#03071e", "#370617", "#6a040f", "#9d0208", "#d00000", "#dc2f02", "#e85d04", "#f48c06", "#faa307", "#ffba08"]
#col_hex = ["#386641", "#6a994e", "#a7c957", "#f2e8cf", "#bc4749"]
#col_hex = ["#0081a7", "#00afb9", "#fdfcdc", "#fed9b7", "#f07167"]
#col_hex = ["#7400b8", "#6930c3", "#5e60ce", "#5390d9", "#4ea8de", "#48bfe3", "#56cfe1", "#64dfdf", "#72efdd", "#80ffdb"]
col_hex = ["#10451d", "#155d27", "#1a7431", "#208b3a", "#25a244", "#2dc653", "#4ad66d", "#6ede8a", "#92e6a7", "#b7efc5"]
#col_hex = ["#af4d98", "#d66ba0", "#e5a9a9", "#f4e4ba", "#9df7e5"]
colors = np.zeros((len(col_hex), 3), dtype=np.uint8)

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

for i in range(len(col_hex)):
    colors[i, :] = hex_to_rgb(col_hex[i])


# Définition des constantes
#---------------------------
sizeX = 1080
sizeY = 1920
degP = 10
iters = 9
degP = min(degP, len(col_hex))


# Préparation de l'Affichage
#----------------------------
fen = Tk()
fen.geometry(str(sizeY + 10) + "x" + str(sizeX + 10))
can = Canvas(fen, width = sizeY, height = sizeX, bg = 'black')
can.pack()


# Initialisation des points
#---------------------------
print("Initialisation des points...")
XY = np.zeros((sizeX, sizeY), dtype=np.complex_)
for i in range(sizeX):
    for j in range(sizeY):
        XY[i, j] = complex(i, j) - complex(sizeX / 2, sizeY / 2)


# Initialisation des racines
#----------------------------
print("Initialisation des racines...")
roots = np.zeros((degP,), dtype=np.complex_)
for i in range(degP):
    roots[i] = max(sizeX, sizeY) * (complex(np.random.random() - 0.5, np.random.random() - 0.5))
    print("Racine ", i, ": ", roots[i])


# Calcul du polynôme à partir des racines
#-----------------------------------------
print("Calcul du polynôme à partir des racines...")
P = np.zeros((degP + 1,), dtype=np.complex_)
P[0] = 1
for i in range(degP):
    P = np.concatenate(([0], P[:-1])) - roots[i] * P


# Calcul du polynome dérivé
#---------------------------
print("Calcul du polynôme dérivé...")
Q = np.zeros((degP,), dtype=np.complex_)
for i in range(degP):
    Q[i] = (i + 1) * P[i + 1]


# Sauvegarde de la distance parcourue par chaque point à la dernière itération (pour le contraste)
#--------------------------------------------------------------------------------------------------
S = np.zeros(XY.shape, dtype=np.complex_)


# Calcul de l'algorithme de Newton
#----------------------------------
print("Algorithme de Newton...")
for i in range(iters):
    PXY = np.zeros(XY.shape, dtype=np.complex_)
    QXY = np.zeros(XY.shape, dtype=np.complex_)
    for j in range(degP):
        PXY += P[j] * np.power(XY, j)
    for j in range(degP - 1):
        QXY += Q[j] * np.power(XY, j)
    S = PXY/QXY
    XY -= S


# Préparation de l'image
#------------------------
print("Préparation de l'image...")
S = np.abs(S)
R = np.zeros((sizeX, sizeY, degP))
for i in range(degP):
    R[:,:,i] = np.abs(XY - roots[i] * np.ones(XY.shape))
R = np.argmin(R, axis = 2)


# Calcul de l'image
#-------------------
print("Calcul de l'image...")
imageExport = np.zeros((sizeX, sizeY, 3), dtype=np.uint8)
for i in range(degP):
    for j in range(3):
        imageExport[:, :, j] += np.uint8(colors[i, j] * (R == i) * (1 / (S + 1)))


# Sauvegarde de l'image
#-----------------------
print("Sauvegarde de l'image...")
dt_string = now.strftime("%d%m%Y%H%M%S")
PIL_image = Image.fromarray( np.uint8( imageExport ) )
PIL_image.save("./Images/"+dt_string+".png")


print("Terminé!")


# Affichage de l'image
#----------------------
img = ImageTk.PhotoImage(Image.fromarray(np.uint8(imageExport)))
can.create_image(0, 0, anchor=NW, image = img)

fen.mainloop()
