import pandas as pd
import csv

DELTA_T = 4*60*60 #4 horas en segundos
T_INI = 6*60*60
T_FIN = 22*60*60
T_MAX = 12*60*60
T_INI_MAX = 7*60*60
T_QUIETO = 15*60

class Camion:
    def __init__(self,dominio):
        self.dominio = dominio
        #self.info = np.array[7][...]
        self.moving = False
        self.beginWork = 0
        self.endWork = 0
        self.startMoving = 0
        self.stopMoving = 0
        self.totalTime = 0
        self.tiempo = 0
        self.eventos = []
    def nuevoDato(self,dato): #dato es una linea entera del csv
        #print(dato['Latitud'])
        self.eventos.append(dato)
    def procesarInfo(self):
        print("soy el camion", self.dominio)
        #print (self.eventos[0])
        for ev in self.eventos:

           # print(ev['Velocidad'])
           # ev['Fecha'][0]
           #print(ev['Fecha'])
           # print(ev['Fecha'][11])
           #ev['Fecha'][11]     hora
           #ev['Fecha'][12]     hora
           #ev['Fecha'][14]     min
           #ev['Fecha'][15]     min
           #ev['Fecha'][17]     seg
           #ev['Fecha'][18]     seg

           # self.tiempo = (int(ev['Fecha'][11]) * 10 + int(ev['Fecha'][12])) * 60 + (int(ev['Fecha'][14]) * 10 + int(ev['Fecha'][15]))
            #print ("tiempo: ", self.tiempo, "minutos")
            if (ev['Velocidad'] == 0):
                if (self.moving==True):
                    self.moving = False
                    #   cambio
                    self.tiempo = (int(ev['Fecha'][11]) * 10 + int(ev['Fecha'][12])) * 60 *60 + (
                                    int(ev['Fecha'][14]) * 10 + int(ev['Fecha'][15]))* 60 + (
                                    int(ev['Fecha'][17]) * 10 + int(ev['Fecha'][18]))
                    self.stopMoving = self.tiempo  #ev['Fecha'][]
                    print("stop moving: ", int((self.stopMoving)/(60*60)), ":",
                          int(((self.stopMoving)%(60*60))/60), ":",
                          int((self.stopMoving)%(60*60)%60))
                    self.totalTime = self.totalTime + (self.stopMoving - self.startMoving)
                    #print("total time: ", int((self.totalTime)/60), "hs",(self.totalTime)%60, "mins")
                    if((self.stopMoving - self.startMoving)>DELTA_T):
                        print("WARNING: Exceso de delta t")
            else:
                #print("distinta de cero")
                if (self.moving == False):
                    self.moving = True
                    #self.tiempo = (int(ev['Fecha'][11]) * 10 + int(ev['Fecha'][12])) * 60 + (
                    #        int(ev['Fecha'][14]) * 10 + int(ev['Fecha'][15]))
                    self.tiempo = (int(ev['Fecha'][11]) * 10 + int(ev['Fecha'][12])) * 60 * 60 + (
                            int(ev['Fecha'][14]) * 10 + int(ev['Fecha'][15]) )* 60 + (
                            int(ev['Fecha'][17]) * 10 + int(ev['Fecha'][18]))
                    self.startMoving = self.tiempo
                    #if((self.stopMoving != 0) & (self.beginWork != 0)):
                    if (self.beginWork != 0):
                        print("delta t quieto: ", int((self.startMoving-self.stopMoving)/(60*60)), "hs",
                              int(((self.startMoving-self.stopMoving) % (60*60))/60), "mins",
                              int((self.startMoving-self.stopMoving) % (60*60) % 60), "s" )
                        if(((self.startMoving-self.stopMoving)<T_QUIETO) & (self.beginWork != 0)):
                            print("WARNING: descanso poco")
                    print("startMoving: ", int((self.startMoving)/(60*60)), ":",
                          int((self.startMoving) % (60*60)/60), ":",
                          int(((self.startMoving) % (60*60)) % 60))
                    if (self.beginWork == 0):
                        self.beginWork = self.tiempo
                        print("begin work: ", int((self.beginWork)/(60*60)), ":",
                              int((self.beginWork) % (60*60)/60), ":",
                              int(((self.beginWork) % (60*60)) % 60))
        self.endWork = self.stopMoving
        print("hora de finalizacion: ", int((self.endWork)/(60*60)), ":",
              int((self.endWork)%(60*60)/60), ":",
              int(((self.endWork) % (60*60)) % 60))
        if(self.endWork > T_FIN):
            print("WARNING: Termino tarde")
        print("tiempo total andando: ", int((self.totalTime)/(60*60)), "hs",
              int((self.totalTime)%(60*60)/60), "mins",
              int(((self.totalTime)%(60*60))%60))
        if(self.totalTime>T_MAX):
            print("WARNING: Se excedio del T_MAX")

def main():
    archivo = pd.read_csv("ST_2019_27_05.csv", delimiter=";", encoding="ISO-8859-1")
    archivo = archivo.sort_values(by = ['Dominio', 'Fecha'])
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

    # csvData = [['Person', 'Age'], ['Peter', '22'], ['Jasmine', '21'], ['Sam', '24']]
    # with open('person.csv', 'w') as csvFile:
    #     writer = csv.writer(csvFile)
    #     writer.writerows(csvData)
    # csvFile.close()


main()