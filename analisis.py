import csv
import numpy as np

def read_csv(filename):
    data = dict()
    data["patente"] = []
    data["evento"] = []
    data["datos"] = []
    data["ubicacion"] = []
    data["fecha"] = []
    data["vel"] = []
    data["latitud"] = []
    data["longitud"] = []

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
    return data

DELTA_T = 4*60 #4 horas en minutos
T_INI = 6*6
T_FIN = 22*60
T_MAX = 12*60
T_INI_MAX = 7*60
T_QUIETO = 15

class Camion(object):
    patent = None
    info = np.array[7][...]
    moving = False
    beginWork = None
    endWork = None
    startMoving = None
    stopMoving = None
    totalTime = None

##########
#VER CUANTAS PATENTES HAY

class MyClass(object):
    def __init__(self, number):
        self.number = number

my_objects = []

for i in range(cantPatentes):
    my_objects.append(MyClass(i))

# later

for obj in my_objects:
    print obj.number
###########


for x in camiones
    for y in camiones[x]
        if camion.vel


