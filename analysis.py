import pandas as pd
import csv
import datetime


NOMBRE_CSV = "ST_2019_27_05.csv"

DELTA_T = 4*60*60 #4 horas en segundos
T_INI = 6*60*60
T_FIN = 22*60*60
T_MAX = 12*60*60
T_INI_MAX = 7.5*60*60
T_QUIETO = 15*60



class Camion:
    def __init__(self,dominio_):
        self.dominio = dominio_
        self.moving = False
        self.beginWork = 0
        self.endWork = 0
        self.startMoving = 0
        self.stopMoving = 0
        self.totalTime = 0
        self.tiempo = 0
        self.timeExcess = False
        self.forbiddenTime = False
        self.eventos = []

    def nuevoDato(self,dato): #dato es una linea entera del csv
        self.eventos.append(dato)
    def procesarInfo(self):
        print("\n\nCamion:",self.dominio,"\n")
        for ev in self.eventos:
            if (ev['Velocidad'] == 0):
                if (self.moving==True):
                    self.moving = False
                    #   cambio
                    self.tiempo = (int(ev['Fecha'][11]) * 10 + int(ev['Fecha'][12])) * 60 * 60 + (
                                    int(ev['Fecha'][14]) * 10 + int(ev['Fecha'][15]))* 60 + (
                                    int(ev['Fecha'][17]) * 10 + int(ev['Fecha'][18]))
                    self.stopMoving = self.tiempo  #ev['Fecha'][]
                    self.totalTime = self.totalTime + (self.stopMoving - self.startMoving)
                    if((self.stopMoving - self.startMoving)>DELTA_T):
                        self.timeExcess = True
                        print("WARNING: Exceso de delta t")
            else:
                if (self.moving == False):
                    self.moving = True
                    self.tiempo = (int(ev['Fecha'][11]) * 10 + int(ev['Fecha'][12])) * 60 * 60 + (
                            int(ev['Fecha'][14]) * 10 + int(ev['Fecha'][15]) )* 60 + (
                            int(ev['Fecha'][17]) * 10 + int(ev['Fecha'][18]))

                    self.startMoving = self.tiempo

                    if ((self.stopMoving-self.startMoving)>DELTA_T): # Tiempo de manejo
                        print("Tiempo excedido: ", int((self.stopMoving-self.startMoving)/(60*60)),":",
                              int(((self.stopMoving-self.startMoving) % (60*60))/60),":",
                              int((self.stopMoving-self.startMoving) % (60*60) % 60))


                    if (self.beginWork == 0):
                        self.beginWork = self.tiempo
                        print("Comenzo: ", int((self.beginWork)/(60*60)), ":",
                              int((self.beginWork) % (60*60)/60), ":",
                              int(((self.beginWork) % (60*60)) % 60))
        self.endWork = self.stopMoving

        print("Finalizo: ", int((self.endWork)/(60*60)), ":",
              int((self.endWork)%(60*60)/60), ":",
              int(((self.endWork) % (60*60)) % 60))

        if (self.beginWork > T_INI_MAX):
            print("WARNING: Empezo tarde")

        if(self.endWork > T_FIN or self.beginWork < T_INI):
            self.forbiddenTime = True
            print("WARNING: Tiempos prohibidos")

        print("Tiempo total andado: ", int((self.totalTime)/(60*60)), ":",
              int((self.totalTime)%(60*60)/60), ":",
              int(((self.totalTime)%(60*60))%60))
        if(self.totalTime>T_MAX):
            print("WARNING: Se excedio del T_MAX")

            #int(self.to_csv('hrdata_modified.csv')

def main():
    archivo = pd.read_csv(NOMBRE_CSV, delimiter = ";",encoding = "ISO-8859-1", decimal= ",")
    archivo = archivo.sort_values(by = ['Dominio', 'Fecha'])
    data = archivo.to_dict("index")
    camiones = dict()

    for dato in data.keys():
        dominio = data[dato]['Dominio']
        if dominio in camiones:
            camiones[dominio].nuevoDato(data[dato])
        else:
            camiones[dominio] = Camion(dominio)
            camiones[dominio].nuevoDato(data[dato])
    for camion in camiones.keys():
        camiones[camion].procesarInfo()

    csvHeaders = ['Dominio', 'Fecha', 'Hora inicio', 'Hora finalizacion', 'Tiempo total de manejo', 'Exceso de intervalo', 'Tiempos prohibidos']
    with open('Resultados.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(csvHeaders)
        for camion in camiones.keys():
            trackRow = [camiones[camion].dominio, camiones[camion].eventos[0]['Fecha'].rsplit()[0], str(datetime.timedelta(seconds=camiones[camion].beginWork)), str(datetime.timedelta(seconds=camiones[camion].endWork)), str(datetime.timedelta(seconds=camiones[camion].totalTime)), camiones[camion].timeExcess, camiones[camion].forbiddenTime]
            writer.writerow(trackRow)
    csvFile.close()

main()

