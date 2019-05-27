import pandas as pd

class Camion:
    def __init__(self,dominio):
        self.dominio = dominio
        #self.info = np.array[7][...]
        self.moving = False
        self.beginWork = None
        self.endWork = None
        self.startMoving = None
        self.stopMoving = None
        self.totalTime = None
        self.eventos = []
    def nuevoDato(self,dato): #dato es una linea entera del csv
        #print(dato['Latitud'])
        self.eventos.append(dato)
    def procesarInfo(self):
        print ("soy el camion", self.dominio)
        print (self.eventos)

def main():
    archivo = pd.read_csv("ST.csv", delimiter = ";",encoding = "ISO-8859-1")
    archivo = archivo.sort_values(by = 'Fecha')
    data = archivo.to_dict("index")
    #print (data.keys())
    camiones = dict()
    for dato in data.keys():
        #print(data[dato]['Fecha'])
        dominio = data[dato]['Dominio']
        if dominio in camiones:
            camiones[dominio].nuevoDato(data[dato])
        else:
            camiones[dominio] = Camion(dominio)
            camiones[dominio].nuevoDato(data[dato])
    for camion in camiones.keys():
        camiones[camion].procesarInfo()



main()