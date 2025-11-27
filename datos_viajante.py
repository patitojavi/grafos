import math

TODAS_LAS_CIUDADES = [
    {"nombre": "Temuco", "latitud": -38.7399, "longitud": -72.5901},
    {"nombre": "Loncoche", "latitud": -39.3667, "longitud": -72.6333},
    {"nombre": "Carahue", "latitud": -38.7116, "longitud": -73.1648},
    {"nombre": "Cunco", "latitud": -38.9167, "longitud": -72.0333},
    {"nombre": "Angol", "latitud": -37.7988, "longitud": -72.7086},
    {"nombre": "Villarrica", "latitud": -39.2857, "longitud": -72.2279},
    {"nombre": "Pucón", "latitud": -39.2667, "longitud": -71.9667},
    {"nombre": "Victoria", "latitud": -38.2329, "longitud": -72.3329},
    {"nombre": "Curacautín", "latitud": -38.4333, "longitud": -71.8833},
    {"nombre": "Nueva Imperial", "latitud": -38.74490, "longitud": -72.95220},
    {"nombre": "Lautaro", "latitud": -38.53333, "longitud": -72.43333},
    {"nombre": "Galvarino", "latitud": -38.40840, "longitud": -72.78950},
    {"nombre": "Saavedra", "latitud": -38.78333, "longitud": -73.38333},
    {"nombre": "Traiguén", "latitud": -38.25000, "longitud": -72.68333},
    {"nombre": "Collipulli", "latitud": -37.95000, "longitud": -72.43333},
]

def obtener_ciudades(cantidad):
    if cantidad > len(TODAS_LAS_CIUDADES):
        return TODAS_LAS_CIUDADES
    return TODAS_LAS_CIUDADES[:cantidad]

def crear_matriz_distancias(ciudades):
    n = len(ciudades)
    matriz = [[0 for _ in range(n)] for _ in range(n)] # crea una matriz 9x9 de ceros
    
    coordenadas = [(c["latitud"], c["longitud"]) for c in ciudades] # guarda las coordenadas de cada ciudad

    for i in range(n): # recorre cada ciudad
        x1, y1 = coordenadas[i]
        for j in range(n): # desde esa ciudad i recorre cada ciudad j
            x2, y2 = coordenadas[j] # toma las coordenadas de la ciudad destino
            dx = x2 - x1    
            dy = y2 - y1
            distancia = math.sqrt(dx * dx + dy * dy) # calcula la distancia euclidiana

            matriz[i][j] = distancia # asigna la distancia en la matriz
    return matriz

def crear_instancia_viajante(ciudades):
    matriz = crear_matriz_distancias(ciudades)
    return {
        "ciudades": ciudades, 
        "matriz_distancias": matriz
    }

def longitud_recorrido(instancia, recorrido):
    if not recorrido:
        return 0.0

    matriz = instancia["matriz_distancias"]
    distancia_total = 0.0

    # Sumar distancias del camino
    for i in range(len(recorrido) - 1):
        origen = recorrido[i]
        destino = recorrido[i + 1]
        distancia_total += matriz[origen][destino]

    # Sumar vuelta al inicio (ciclo)
    ultimo = recorrido[-1]
    primero = recorrido[0]
    distancia_total += matriz[ultimo][primero]
    
    return distancia_total

def coordenadas_ciudades(instancia):
    longitudes = [c["longitud"] for c in instancia["ciudades"]]
    latitudes = [c["latitud"] for c in instancia["ciudades"]]
    return longitudes, latitudes
