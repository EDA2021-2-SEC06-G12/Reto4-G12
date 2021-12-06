﻿"""
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
from DISClib.Utils import error as error
from DISClib.Algorithms.Sorting import mergesort as mrgs
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as dj
from DISClib.Algorithms.Graphs import prim
import folium 
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
                    'Aeropuertos': None,
                    'Ciudades': None,
                    'Rutas_D': None,
                    'Lista_Ciudades': None,
                    'Dirigido': None,
                    'No_Dirigido': None
                    }

        catalog['Aeropuertos'] = mp.newMap(numelements=100000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)
        
        catalog['Ciudades'] = mp.newMap(numelements=45000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)
        
        catalog['Rutas_D'] = mp.newMap(numelements=45000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)

        catalog['ListaCiudades'] = lt.newList('SINGLE_LINKED')

        catalog['Dirigido'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=100000,
                                              comparefunction=compareStopIds)
        
        catalog['No_Dirigido'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=100000,
                                              comparefunction=compareStopIds)
        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:newCatalog')

# CARGA DE DATOS AL CATÁLOGO
def addAeroD(catalog, aeropuerto):
    try:
        if not gr.containsVertex(catalog['Dirigido'], aeropuerto):
            gr.insertVertex(catalog['Dirigido'], aeropuerto)
        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:addAeroD')

def addEdgeD(catalog, origen, destino, distancia):
    gr.addEdge(catalog['Dirigido'], origen, destino, distancia)
    return catalog

def addAeroND(catalog, aeropuerto):
    try:
        if not gr.containsVertex(catalog['No_Dirigido'], aeropuerto):
            gr.insertVertex(catalog['No_Dirigido'], aeropuerto)
        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:addAeroND')

def addEdgeND(catalog, origen, destino, distancia):
    if gr.getEdge(catalog['No_Dirigido'], origen, destino) is None:
        gr.addEdge(catalog['No_Dirigido'], origen, destino, distancia)
    return catalog

def addAeroRuta(catalog, ruta):
    entry = mp.get(catalog['Rutas_D'], ruta['Departure'])
    if entry is None:
        lstroutes = lt.newList('ARRAY_LIST')
        lt.addLast(lstroutes, ruta['Destination'])
        mp.put(catalog['Rutas_D'], ruta['Departure'], lstroutes)
    else:
        lstroutes = entry['value']
        info = ruta['Destination']
        if not lt.isPresent(lstroutes, info):
            lt.addLast(lstroutes, info)
    return catalog

def verificar(catalog, origen, destino, distancia):
    entry = mp.get(catalog['Rutas_D'], destino)
    if entry is not None:
        lista = me.getValue(entry)
        for i in lt.iterator(lista):
            if i == origen:
                addEdgeND(catalog, origen, destino, distancia)
    return catalog

def addAeropuerto(catalog, aeropuerto):
    aeropuertos = catalog['Aeropuertos']
    exist = mp.contains(aeropuertos, aeropuerto['IATA'])
    if not exist:
        mp.put(aeropuertos, aeropuerto['IATA'], aeropuerto)

def addCiudad(catalog, ciudad):
    ciudades = catalog['Ciudades']
    exist = mp.contains(ciudades, ciudad['city'])
    if not exist:
        lst_ciudades=lt.newList('ARRAY_LIST')
        lt.addLast(lst_ciudades,ciudad)
        mp.put(ciudades, ciudad['city'], lst_ciudades)

    if exist:       
        lista= me.getValue(mp.get(ciudades,ciudad['city']))
        lt.addLast(lista,ciudad)
    lt.addLast(catalog['ListaCiudades'], ciudad)

# REQUERIMIENTO 1 (ENCONTRAR PUNTOS DE INTERCONEXIÓN AÉREA)
def InterAerea(catalog):
    lista = lt.newList('ARRAY_LIST')
    lista_c = lt.newList('ARRAY_LIST')
    lista_f = lt.newList('ARRAY_LIST')
    vertices = gr.vertices(catalog['Dirigido'])
    for i in lt.iterator(vertices):
        in_d = gr.indegree(catalog['Dirigido'], i)
        out_d = gr.outdegree(catalog['Dirigido'], i)
        total = in_d + out_d
        if total != 0:
            lt.addLast(lista, (total, i, str(in_d), str(out_d)))
    
    orden = ordenamiento(lista)
    mayores = lt.subList(orden, 1, 5)

    for j in lt.iterator(mayores):
        IATA = j[1]
        entry = mp.get(catalog['Aeropuertos'], IATA)
        value = me.getValue(entry)
        lt.addLast(lista_f, (j[0], j[2], j[3], value))
        lt.addLast(lista_c, value)
    
    cuantos = lt.size(orden)

    Visualizar(lista_c, 'Requerimiento 1.html')

    return cuantos, lista_f['elements']

# REQUERIMIENTO 2 (ENCONTRAR CLÚSTERES DE TRÁFICO AÉRE0)
def ClusterAereo(catalog, IATA_1, IATA_2):
    componentes = scc.KosarajuSCC(catalog['Dirigido'])
    cuantos = scc.connectedComponents(componentes)
    pertenecen = scc.stronglyConnected(componentes, IATA_1, IATA_2)
    return cuantos, pertenecen

# REQUERIMIENTO 3 (ENCONTRAR LA RUTA MÁS CORTA ENTRE CIUDADES)
def RutaCorta(catalog, origen, destino, lista_1, lista_2):
    origen = lt.getElement(lista_1, int(origen))
    destino = lt.getElement(lista_2, int(destino))
    pais_o = origen['country']
    pais_d = destino['country']
    return pais_o, pais_d

def Seleccionar_Ciudad(catalog, origen, destino):
    len_O = len(origen)
    len_D = len(destino)
    ciudades_1 = lt.newList('ARRAY_LIST')
    ciudades_2 = lt.newList('ARRAY_LIST')
    lista = mp.keySet(catalog['Ciudades'])
    for i in lt.iterator(lista):
        if len_O > 6:
            if origen[::-1][0:int(len(origen)/2) + 1] in i[::-1][0:int(len(i)/2) + 1]:
                entry = mp.get(catalog['Ciudades'], i)
                value = me.getValue(entry)
                lt.addLast(ciudades_1, (i, value))
        if len_D > 6:
            if destino[::-1][0:int(len(destino)/2) + 1] in i[::-1][0:int(len(i)/2) + 1]:
                entry = mp.get(catalog['Ciudades'], i)
                value = me.getValue(entry)
                lt.addLast(ciudades_2, (i, value))
        else:
            if i == origen:
                entry = mp.get(catalog['Ciudades'], i)
                value = me.getValue(entry)
                lt.addLast(ciudades_1, (i, value))
            if i == destino:
                entry = mp.get(catalog['Ciudades'], i)
                value = me.getValue(entry)
                lt.addLast(ciudades_2, (i, value))

    x = Contar(ciudades_1)
    y = Contar(ciudades_2)

    return x[0], y[0], x[1], y[1]

def Contar(lista):
    ciudades_1 = lt.newList('ARRAY_LIST')
    for i in lt.iterator(lista):
        lista_1 = i[1]
        for j in lt.iterator(lista_1):
            lt.addLast(ciudades_1, j)
    x = lt.size(ciudades_1)
    return x, ciudades_1

# REQUERIMIENTO 4 (UTILIZAR LAS MILLAS DE VIAJERO)
def MillasViajero(catalog, millas, origen):
    millas = float(millas) * 1.60
    MST = prim.PrimMST(catalog['No_Dirigido'])
    '''MST = prim.edgesMST(catalog['No_Dirigido'], MST)
    mst = MST['edgeTo']['table']['elements']
    for i in mst:
        if i['key'] is not None:
            print(i)'''
    return MST['edgeTo']

# REQUERIMIENTO 5 (CUANTIFICAR EL EFECTO DE UN AEROPUERTO CERRADO)
def AeropuertoCerrado(catalog, cerrado):
    lista = lt.newList('ARRAY_LIST')
    AD = gr.adjacents(catalog['No_Dirigido'], cerrado)
    for i in lt.iterator(AD):
        entry = mp.get(catalog['Aeropuertos'], i)
        value = me.getValue(entry)
        lt.addLast(lista, value)

    cuantos = lt.size(lista)

    primeros_3 = lt.subList(lista, 1, 3)
    ultimos_3 = lt.subList(lista, len(lista) - 3, 3)

    Visualizar(lista, 'Requerimiento 5.html')

    return cuantos, primeros_3, ultimos_3

# REQUERIMIENTO 6 (COMPARAR CON SERVICIO WEB EXTERNO)
#def WEBExterno():

# REQUERIMIENTO 7 (VISUALIZAR GRÁFICAMENTE LOS REQUERIMIENTOS)
def Visualizar(lista, nombre_mapa):
    aeropuertos = lista
    mapa = folium.Map()
    tooltip = '¿Cuál aeropuerto es?: ¡Click para ver!'
    for i in lt.iterator(aeropuertos):
        nombre = i['Name'],(i['IATA'])
        folium.Marker([i['Latitude'], i['Longitude']], tooltip=tooltip,
                        popup=nombre).add_to(mapa)
    mapa.save(nombre_mapa)

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

def cmpA_IN(artist1, artist2):
    if artist1 > artist2:
        r = True
    else:
        r = False 
    return r

#FUNCIONES DE ORDENAMIENTO
def ordenamiento(Lista):
    sorted_list = mrgs.sort(Lista, cmpfunction=cmpA_IN)
    return sorted_list

# FUNCIONES ADICIONALES
def cleanServiceDistance(ruta):
    if ruta['distance_km'] == '':
        ruta['distance_km'] = 0

def NumeroAeropuertosD(catalog):
    return gr.numVertices(catalog['Dirigido'])

def NumeroRutasD(catalog):
    return gr.numEdges(catalog['Dirigido'])

def NumeroAeropuertosND(catalog):
    return gr.numVertices(catalog['No_Dirigido'])

def NumeroRutasND(catalog):
    return gr.numEdges(catalog['No_Dirigido'])

def NumeroCiudades(catalog):
    return lt.size(catalog['ListaCiudades'])

def Ciudadescargadas(catalog):
    primera = lt.firstElement(catalog['ListaCiudades'])
    ultima = lt.lastElement(catalog['ListaCiudades'])
    return primera, ultima

def AeropuertosCargadosD(catalog):
    lista = lt.newList('ARRAY_LIST')
    vertices = gr.vertices(catalog['Dirigido'])
    primero = lt.firstElement(vertices)
    ultimo = lt.lastElement(vertices)
    tupla = primero, ultimo
    for i in tupla:
        entry = mp.get(catalog['Aeropuertos'], i)
        value = me.getValue(entry)
        lt.addLast(lista, value)
    return lista

def AeropuertosCargadosND(catalog):
    lista = lt.newList('ARRAY_LIST')
    vertices = gr.vertices(catalog['No_Dirigido'])
    primero = lt.firstElement(vertices)
    ultimo = lt.lastElement(vertices)
    tupla = primero, ultimo
    for i in tupla:
        entry = mp.get(catalog['Aeropuertos'], i)
        value = me.getValue(entry)
        lt.addLast(lista, value)
    return lista