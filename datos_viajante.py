from typing import List, Dict, Any, Tuple

import math

# ---- Tipos básicos ----

Ciudad = Dict[str, Any]
InstanciaViajante = Dict[str, Any]
SolucionViajante = Dict[str, Any]


def crear_ciudad(nombre: str, latitud: float, longitud: float) -> Ciudad:
    return {"nombre": nombre, "latitud": float(latitud), "longitud": float(longitud)}

def crear_matriz_distancias(ciudades: List[Ciudad]) -> List[List[float]]:
    cantidad = len(ciudades)
    matriz = [[0.0 for _ in range(cantidad)] for _ in range(cantidad)] # crea una matriz 9x9 de ceros
    
    coordenadas = [(c["latitud"], c["longitud"]) for c in ciudades] # guarda las coordenadas de cada ciudad

    for i in range(cantidad): # recorre cada ciudad
        x1, y1 = coordenadas[i]
        for j in range(cantidad): # desde esa ciudad recorre cada ciudad
            x2, y2 = coordenadas[j] # toma las coordenadas de la ciudad destino
            dx = x2 - x1    
            dy = y2 - y1
            distancia = math.sqrt(dx * dx + dy * dy) # calcula la distancia euclidiana

            matriz[i][j] = distancia # asigna la distancia en la matriz
    return matriz

def crear_instancia_viajante(ciudades: List[Ciudad]) -> InstanciaViajante:
    matriz = crear_matriz_distancias(ciudades)
    return {"ciudades": ciudades, "matriz_distancias": matriz}

def total_ciudades(instancia: InstanciaViajante) -> int:
    return len(instancia["ciudades"])

def longitud_recorrido(instancia: InstanciaViajante, recorrido: List[int]) -> float:
    if not recorrido:
        return 0.0

    matriz = instancia["matriz_distancias"]
    distancia = 0.0

    for i in range(len(recorrido) - 1):
        origen = recorrido[i]
        destino = recorrido[i + 1]
        distancia += float(matriz[origen][destino])

    distancia += float(matriz[recorrido[-1]][recorrido[0]])
    return distancia

def coordenadas_ciudades(instancia: InstanciaViajante) -> Tuple[List[float], List[float]]:
    longitudes = [c["longitud"] for c in instancia["ciudades"]]
    latitudes = [c["latitud"] for c in instancia["ciudades"]]
    return longitudes, latitudes

def crear_solucion(
    recorrido: List[int],
    longitud: float,
    metodo: str,
    tiempo: float,
) -> SolucionViajante:
    return {
        "recorrido": list(recorrido),
        "longitud": float(longitud),
        "metodo": str(metodo),
        "tiempo": float(tiempo),
    }

TODAS_LAS_CIUDADES: List[Ciudad] = [
    crear_ciudad("Temuco", -38.7399, -72.5901),
    crear_ciudad("Loncoche", -39.3667, -72.6333),
    crear_ciudad("Carahue", -38.7116, -73.1648),
    crear_ciudad("Cunco", -38.9167, -72.0333),
    crear_ciudad("Angol", -37.7988, -72.7086),
    crear_ciudad("Villarrica", -39.2857, -72.2279),
    crear_ciudad("Pucón", -39.2667, -71.9667),
    crear_ciudad("Victoria", -38.2329, -72.3329),
    crear_ciudad("Curacautín", -38.4333, -71.8833),
    crear_ciudad("Nueva Imperial",-38.74490, -72.95220),
    crear_ciudad("Lautaro", -38.53333, -72.43333),
    crear_ciudad("Galvarino", -38.40840, -72.78950),
    crear_ciudad("Saavedra", -38.78333, -73.38333),
    crear_ciudad("Traiguén", -38.25000, -72.68333),
    crear_ciudad("Collipulli", -37.95000, -72.43333),
]

def obtener_ciudades(cantidad: int) -> List[Ciudad]:
    cantidad = max(3, min(cantidad, len(TODAS_LAS_CIUDADES)))
    return TODAS_LAS_CIUDADES[:cantidad]
