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

def printMenu():
    print("Bienvenido")
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
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')


    if int(inputs[0]) == 1:
        print("Inicializando Catálogo ....\n")
        cont = controller.initCatalog()
        print("Catálogo Inicializado\n")

    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ....\n")
        controller.loadData(cont)
        print("Para el grafo dirigido:")
        print("El número de vértices cargados es de:", str(controller.NumeroAeropuertosD(cont)))
        print("El número de rutas cargadas es de:", str(controller.NumeroRutasD(cont)), "\n")
        print("Para el grafo no dirigido:")
        print("El número de vértices cargados es de:", str(controller.NumeroAeropuertosND(cont)))
        print("El número de rutas cargadas es de:", str(controller.NumeroRutasND(cont)), "\n")

        #print(mp.keySet(cont['Aeropuertos']))
        #print(gr.outdegree(cont['Dirigido']))
        #print(gr.indegree(cont['Dirigido']))
    
    elif int(inputs[0]) == 3:
        Algoritmo = controller.InterAerea(cont)
        print(Algoritmo)

    elif int(inputs[0]) == 4:
        Algoritmo = controller.ClusterAereo()
    
    elif int(inputs[0]) == 5:
        Algoritmo = controller.RutaCorta()
    
    elif int(inputs[0]) == 6:
        Algoritmo = controller.MillasViajero()
    
    elif int(inputs[0]) == 7:
        Algoritmo = controller.AeropuertoCerrado()
    
    elif int(inputs[0]) == 8:
        Algoritmo = controller.WEBExterno()

    else:
        sys.exit(0)
sys.exit(0)
