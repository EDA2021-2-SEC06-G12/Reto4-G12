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
    rutas = cf.data_dir + 'routes_full.csv'
    archivo_rutas = csv.DictReader(open(rutas, encoding="utf-8"))
    ultimo = None
    for ruta in archivo_rutas:
        if ultimo is not None:
            aerolinea = ultimo['Airline'] == ruta['Airline']
            origen = ultimo['Departure'] == ruta['Departure']
            destino = ultimo['Destination'] == ruta['Destination']
            if origen and destino and not aerolinea:
                model.addRutas(catalog, ultimo, ruta)
        ultimo = ruta
    return catalog

# REQUERIMIENTO 1 (ENCONTRAR PUNTOS DE INTERCONEXIÓN AÉREA)
def InterAerea(catalog):
    Algoritmo = model.InterAerea(catalog)
    return Algoritmo

# REQUERIMIENTO 2 (ENCONTRAR CLÚSTERES DE TRÁFICO AÉRE0)
def ClusterAereo():
    Algoritmo = model.ClusterAereo()
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
def NumeroAeropuertos(catalog):
    return model.NumeroAeropuertos(catalog)

def NumeroRutas(catalog):
    return model.NumeroRutas(catalog)