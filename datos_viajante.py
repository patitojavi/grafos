import math
# diccionario de ciudades con sus coordenadas
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
    if cantidad > len(TODAS_LAS_CIUDADES):  # si pide más ciudades de las disponibles
        return TODAS_LAS_CIUDADES   # devuelve todas las ciudades
    return TODAS_LAS_CIUDADES[:cantidad] # si no, devuelve las primeras 'n' ciudades

def crear_matriz_distancias(ciudades):
    n = len(ciudades) # lee la cantidad de ciudades
    matriz = [[0.0 for _ in range(n)] for _ in range(n)] # crea una matriz n x n inicializada en 0
    
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
        "ciudades": ciudades,  # retorna un diccionario con las ciudades
        "matriz_distancias": matriz # y la matriz de distancias
    }

def longitud_recorrido(instancia, recorrido): 
    if not recorrido: # si no hay ciudades la distancia es 0
        return 0.0

    matriz = instancia["matriz_distancias"] # extrae la matriz de distancias
    distancia_total = 0.0 # contador de distancia total

    for i in range(len(recorrido) - 1): # recorre el recorrido de ciudades
        origen = recorrido[i] # ciudad actual
        destino = recorrido[i + 1] # ciudad siguiente
        distancia_total += matriz[origen][destino] # suma la distancia entre ambas ciudades

    ultimo = recorrido[-1] # última ciudad del recorrido
    primero = recorrido[0] # primera ciudad del recorrido
    distancia_total += matriz[ultimo][primero] # suma la distancia de regreso a la ciudad inicial
    
    return distancia_total # devuelve la distancia total del recorrido

def coordenadas_ciudades(instancia): 
    longitudes = [c["longitud"] for c in instancia["ciudades"]] 
    latitudes = [c["latitud"] for c in instancia["ciudades"]]
    return longitudes, latitudes # devuelve la lista de longitudes y latitudes
