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
 """

import config as cf
import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# INICIALIZACIÓN DEL CATÁLOGO
def initCatalog():
    catalog = model.newCatalog()
    return catalog

# CARGA DE DATOS AL CATÁLOGO
def loadData(catalog):
    rutas = cf.data_dir + 'routes-utf8-small.csv'
    archivo_rutas = csv.DictReader(open(rutas, encoding="utf-8"))

    aeropuertos = cf.data_dir + 'airports-utf8-small.csv'
    archivo_aeropuertos = csv.DictReader(open(aeropuertos, encoding="utf-8"))

    ciudades = cf.data_dir + 'worldcities-utf8.csv'
    archivo_ciudades = csv.DictReader(open(ciudades, encoding="utf-8"))

    for aeropuerto in archivo_aeropuertos:
        codigo = aeropuerto['IATA']
        model.addAeroD(catalog, codigo)
        model.addAeroND(catalog, codigo)
        model.addAeropuerto(catalog, aeropuerto)
    
    for ruta in archivo_rutas:
        origen = ruta['Departure']
        destino = ruta['Destination']
        distancia = ruta['distance_km']
        model.addEdgeD(catalog, origen, destino, distancia)
        #model.addAeroRuta(catalog, ruta)
    
    for ciudad in archivo_ciudades:
        model.addCiudad(catalog, ciudad)
            
    return catalog


# REQUERIMIENTO 1 (ENCONTRAR PUNTOS DE INTERCONEXIÓN AÉREA)
def InterAerea(catalog):
    Algoritmo = model.InterAerea(catalog)
    return Algoritmo

# REQUERIMIENTO 2 (ENCONTRAR CLÚSTERES DE TRÁFICO AÉRE0)
def ClusterAereo(catalog, IATA_1, IATA_2):
    Algoritmo = model.ClusterAereo(catalog, IATA_1, IATA_2)
    return Algoritmo

# REQUERIMIENTO 3 (ENCONTRAR LA RUTA MÁS CORTA ENTRE CIUDADES)
def RutaCorta():
    Algoritmo = model.RutaCorta()
    return Algoritmo

# REQUERIMIENTO 4 (UTILIZAR LAS MILLAS DE VIAJERO)
def MillasViajero():
    Algoritmo = model.MillasViajero()
    return Algoritmo

# REQUERIMIENTO 5 (CUANTIFICAR EL EFECTO DE UN AEROPUERTO CERRADO)
def AeropuertoCerrado():
    Algoritmo = model.AeropuertoCerrado()
    return Algoritmo

# REQUERIMIENTO 6 (COMPARAR CON SERVICIO WEB EXTERNO)
def WEBExterno():
    Algoritmo = model.WEBExterno()
    return Algoritmo

# FUNCIONES ADICIONALES
def NumeroAeropuertosD(catalog):
    return model.NumeroAeropuertosD(catalog)

def NumeroRutasD(catalog):
    return model.NumeroRutasD(catalog)

def NumeroAeropuertosND(catalog):
    return model.NumeroAeropuertosD(catalog)

def NumeroRutasND(catalog):
    return model.NumeroRutasND(catalog)