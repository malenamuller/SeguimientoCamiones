import csv

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

#definicion de ctes:
DELTA_T = 4*60 #4 horas en minutos
T_INI = 6*6
T_FIN = 22*60
T_MAX = 12*60
T_INI_MAX = 7*60
T_QUIETO = 15

class Camion:
    patente = None
    infoCamino
    moving = False
    beginWork = None
    endWork = None
    startMoving = None
    stopMoving = None
    totalTime = None


