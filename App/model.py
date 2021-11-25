"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT.graph import gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Utils import error as error
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# INICIALIZACIÓN DE CATÁLOGO
#Catálogo Vacío
def newCatalog():
    try:
        catalog = {
                    'aeropuertos': None,
                    'rutas': None,
                    'components': None,
                    'paths': None
                    }

        catalog['aeropuertos'] = mp.newMap(numelements=95000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)

        catalog['rutas'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=95000,
                                              comparefunction=compareStopIds)
        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:newCatalog')

# CARGA DE DATOS AL CATÁLOGO
def addRutas(catalog, ultimo, ruta):
    try:
        origen = FormatoVerticeO(ultimo)
        destino = FormatoVerticeD(ruta)
        cleanServiceDistance(ultimo, ruta)
        distancia = float(ruta['distance_km']) - float(ultimo['distance_km'])
        distancia = abs(distancia)
        addAero(catalog, origen)
        addAero(catalog, destino)
        addRuta(catalog, origen, destino, distancia)
        addAeroRutaO(catalog, ultimo)
        addAeroRutaO(catalog, ruta)
    except Exception as exp:
        error.reraise(exp, 'model:addRuta')

def addAero(catalog, aeropuerto):
    try:
        if not gr.containsVertex(catalog['rutas'], aeropuerto):
            gr.insertVertex(catalog['rutas'], aeropuerto)
        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:addAero')

def addRuta(catalog, origen, destino, distancia):
    arco = gr.getEdge(catalog['rutas'], origen, destino)
    if arco is None:
        gr.addEdge(catalog['rutas'], origen, destino, distancia)
    return catalog

def addAeroRutaO(catalog, ruta):
    entry = mp.get(catalog['aeropuertos'], ruta['Departure'])
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareroutes)
        lt.addLast(lstroutes, ruta['Airline'])
        mp.put(catalog['aeropuertos'], ruta['Departure'], lstroutes)
    else:
        lstroutes = entry['value']
        info = ruta['Airline']
        if not lt.isPresent(lstroutes, info):
            lt.addLast(lstroutes, info)
    return catalog

def addAeroRutaD(catalog, ruta):
    entry = mp.get(catalog['aeropuertos'], ruta['Destination'])
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareroutes)
        lt.addLast(lstroutes, ruta['Airline'])
        mp.put(catalog['aeropuertos'], ruta['Destination'], lstroutes)
    else:
        lstroutes = entry['value']
        info = ruta['Airline']
        if not lt.isPresent(lstroutes, info):
            lt.addLast(lstroutes, info)
    return catalog

# REQUERIMIENTO 1 (ENCONTRAR PUNTOS DE INTERCONEXIÓN AÉREA)
#def InterAerea(catalog):

# REQUERIMIENTO 2 (ENCONTRAR CLÚSTERES DE TRÁFICO AÉRE0)
#def ClusterAereo():

# REQUERIMIENTO 3 (ENCONTRAR LA RUTA MÁS CORTA ENTRE CIUDADES)
#def RutaCorta():

# REQUERIMIENTO 4 (UTILIZAR LAS MILLAS DE VIAJERO)
#def MillasViajero():

# REQUERIMIENTO 5 (CUANTIFICAR EL EFECTO DE UN AEROPUERTO CERRADO)
#def AeropuertoCerrado():

# REQUERIMIENTO 6 (COMPARAR CON SERVICIO WEB EXTERNO)
#def WEBExterno():

# FUNCIONES DE COMPARACIÓN
def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1

# FUNCIONES ADICIONALES
def FormatoVerticeO(aeropuerto):
    formato = aeropuerto['Departure'] + '-'
    formato = formato + aeropuerto['Airline']
    return formato

def FormatoVerticeD(aeropuerto):
    formato = aeropuerto['Destination'] + '-'
    formato = formato + aeropuerto['Airline']
    return formato

def cleanServiceDistance(ultimo, ruta):
    if ruta['distance_km'] == '':
        ruta['distance_km'] = 0
    if ultimo['distance_km'] == '':
        ultimo['distance_km'] = 0

def NumeroAeropuertos(catalog):
    return gr.numVertices(catalog['rutas'])

def NumeroRutas(catalog):
    return gr.numEdges(catalog['rutas'])