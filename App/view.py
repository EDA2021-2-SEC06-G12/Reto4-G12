"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
assert cf

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

#FORMATOS DE RESPUESTA
# Carga de Datos
def formatoCargaG(rta):
    for i in lt.iterator(rta):
        print("\nIATA:", i['IATA'])
        print("Name:", i['Name'])
        print("City:", i['City'])
        print("Country:", i['Country'])
        print("Latitude:", i['Latitude'])
        print("Longitude:", i['Longitude'])

def formatoCarga(rta):
    for i in rta:
        print("\nCity:", i['city'])
        print("Country:", i['country'])
        print("Lat:", i['lat'])
        print("Lng:", i['lng'])
        print("Population:", i['population'])

# Requerimiento 1
def formatoRtaReq1(rta):
    for i in rta:
        aero = i[3]
        conexiones = i[0]
        entran = i[1]
        salen = i[2]
        print("\nName:", aero['Name'])
        print("City:", aero['City'])
        print("Country:", aero['Country'])
        print("IATA:", aero['IATA'])
        print("Connections:", conexiones)
        print("Inbound:", entran)
        print("Outbound:", salen)

# Requerimiento 3
def formato(rta):
    opcion = 1
    for i in lt.iterator(rta):
        print("\nOpcion", opcion)
        print("City:", i['city'])
        print("Country:", i['country'])
        print("Lat:", i['lat'])
        print("Lng:", i['lng'])
        print("Population:", i['population'])
        opcion += 1

def formato2(rta):
    print("\nIATA:", rta['IATA'])
    print("Name:", rta['Name'])
    print("City:", rta['City'])
    print("Country:", rta['Country'])

def formato3(rta):
    Recorrido = 1
    for i in lt.iterator(rta):
        print("\nVuelo:", Recorrido)
        print("Departure:", i['vertexA'])
        print("Destination:", i['vertexB'])
        print("Distancia:", i['weight'], "km")
        Recorrido += 1

# Requerimiento 4
def formatoReq4(lista):
    for i in lt.iterator(lista):
        print("\nDeparture:", i[0])
        print("Destination:", i[1])
        print("Distance:", i[2], "km")

# Requerimiento 5
def formatoRtaReq5(rta_1, rta_2):
    for i in lt.iterator(rta_1):
        print("\nIATA:", i['IATA'])
        print("Name:", i['Name'])
        print("City:", i['City'])
        print("Country:", i['Country'])
    for j in lt.iterator(rta_2):
        print("\nIATA:", j['IATA'])
        print("Name:", j['Name'])
        print("City:", j['City'])
        print("Country:", j['Country'])

#INTERACCIÓN CON EL USUARIO
# Menú de Opciones
def printMenu():
    print("\nBienvenido")
    print("1- Inicializar Catálogo")
    print("2- Cargar información en el catálogo")
    print("3- Encontrar puntos de interconexión aérea")
    print("4- Encontrar clústeres de tráfico aéreo")
    print("5- Encontrar la ruta más corta entre ciudades")
    print("6- Utilizar las millas de viajero")
    print("7- Cuantificar el efecto de un aeropuerto cerrado")
    print("8- Comparar con servicio WEB externo")
    print("0- Salir del Menu")

"""
Menu principal
"""
# Selección de Opciones
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if int(inputs[0]) == 1:
        print("Inicializando Catálogo ....\n")
        cont = controller.initCatalog()
        print("Catálogo Inicializado")

    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ....\n")
        controller.loadData(cont)
        print("En el grafo dirigido, se cargaron", str(controller.NumeroAeropuertosD(cont)), "aeropuertos y",
                str(controller.NumeroRutasD(cont)), "rutas. A continuación, se presentan el primer y el último aeropuerto cargado:")
        formatoCargaG(controller.AeropuertosCargadosD(cont))

        print("\nEn el grafo no dirigido, se cargaron", str(controller.NumeroAeropuertosND(cont)), "aeropuertos y",
                str(controller.NumeroRutasND(cont)), "rutas. A continuación, se presentan el primer y el último aeropuerto cargado:")
        formatoCargaG(controller.AeropuertosCargadosND(cont))

        print("\nEn la red de ciudades, se cargaron un total de", controller.NumeroCiudades(cont),
                "ciudades. A continuación, se presentan la primera y la última ciudad cargada:")
        formatoCarga(controller.Ciudadescargadas(cont))

    elif int(inputs[0]) == 3:
        Algoritmo = controller.InterAerea(cont)
        print("\nDentro de la red, hay un total de", Algoritmo[0], 
                "aeropuertos interconectados. A continuación, se presentan los 5 aeropuertos más interconectados:")
        formatoRtaReq1(Algoritmo[1])

    elif int(inputs[0]) == 4:
        IATA_1 = input('Ingrese código IATA del aeropuerto 1: ') # LED
        IATA_2 = input('Ingrese código IATA del aeropuerto 2: ') # RTP
        sys.setrecursionlimit(2 ** 20)
        Algoritmo = controller.ClusterAereo(cont, IATA_1, IATA_2)
        print("\nDentro de la red, hay un total de", Algoritmo[0], "componentes fuertemente conectados.\n")
        if Algoritmo[1]:
            print("Los aeropuertos ingresados se encuentran dentro del mismo componente.")
        else:
            print("Los aeropuertos ingresados no se encuentran dentro del mismo componente.")
    
    elif int(inputs[0]) == 5:
        origen = input('Ingrese ciudad de origen: ') # St. Petersburg
        destino = input('Ingrese ciudad de destino: ') # Lisbon
        Algoritmo = controller.Seleccionar_Ciudad(cont, origen, destino)
        if Algoritmo[0] > 1:
            print("\nHay un total de", Algoritmo[0], "ciudades de origen con el nombre ingresado:")
            formato(Algoritmo[2])
            origen = input('\nPor favor seleccione la opción que desea analizar: ')
        if Algoritmo[1] > 1:
            print("\nHay un total de", Algoritmo[1], "ciudades de destino con el nombre ingresado:")
            formato(Algoritmo[3])
            destino = input('\nPor favor seleccione la opción que desea analizar: ')
        elif Algoritmo[0] == 1:
            origen = 1        
        elif Algoritmo[1] == 1:
            destino = 1
        Respuesta = controller.RutaCorta(cont, origen, destino, Algoritmo[2], Algoritmo[3])
        print("\nEl aeropuerto de origen es:")
        formato2(Respuesta[0])
        print("\nEl aeropuerto de destino es:")
        formato2(Respuesta[1])
        print("\nLa ruta a seguir es:")
        formato3(Respuesta[2])
        print("\nPara un total de", Respuesta[3], "km.")
        print("\nFinalmente, tenemos un total de", round(Respuesta[3] + Respuesta[4][0] + Respuesta[5][0], 3), "km")
    
    elif int(inputs[0]) == 6:
        millas = input('Ingrese millas disponibles: ') # 19850.0
        origen = input('Ingrese código IATA de origen: ') # LIS
        Algoritmo = controller.MillasViajero(cont, millas, origen)
        print("\nDentro del árbol de expansión mínima, hay un total de", Algoritmo[0], "nodos conectados.")
        print("\nLas millas disponibles del viajero son de", str(Algoritmo[4]) + "(km).")
        print("\nA continuación, se presenta la información relacionada a la ruta más larga posible dentro del árbol de expansión mínima:")
        print("\nLa distancia es de", str(round(Algoritmo[1], 3)) + ".")
        print("\nLos vuelos a tomar son:")
        formatoReq4(Algoritmo[2])
        if Algoritmo[3] < 0:
            print("\nAl viajero le sobran un total de", round(abs(Algoritmo[3]), 3), "millas en su viaje.")
        if Algoritmo[3] > 0:
            print("\nAl viajero le faltan un total de", round(abs(Algoritmo[3]), 3), "millas para poder completar su viaje.")
    
    elif int(inputs[0]) == 7:
        cerrado = input('Ingrese IATA del aeropuerto a cerrar: ') # DXB
        Algoritmo = controller.AeropuertoCerrado(cont, cerrado)
        print("Al cerrar el aeropuerto", cerrado + ",", "se afectan", Algoritmo[0],
                "aeropuertos. A continuación, se presentan los 3 primeros y los 3 últimos aeropuertos afectados:")
        formatoRtaReq5(Algoritmo[1], Algoritmo[2])
    
    elif int(inputs[0]) == 8:
        Algoritmo = controller.WEBExterno()

    else:
        sys.exit(0)
sys.exit(0)
