import itertools # herramientas para generar permutaciones de rutas
import time # medir el tiempo de ejecución

from datos_viajante import longitud_recorrido   # cálculo de distancia total de un recorrido

MAX_CIUDADES_EXHAUSTIVO = 11  # límite para la búsqueda exhaustiva

def resolver_exhaustivo_con_traza(instancia):
    ciudades = instancia["ciudades"]  # lista de ciudades disponibles
    total = len(ciudades)  # cantidad total de nodos
    
    if total > MAX_CIUDADES_EXHAUSTIVO:
        # Validación simple
        raise ValueError(f"Demasiadas ciudades para fuerza bruta ({total}). Máximo {MAX_CIUDADES_EXHAUSTIVO}.")
    
    mejor_recorrido = None # mejor ruta encontrada hasta el momento
    mejor_longitud = float("inf") # longitud mínima inicializada en infinito

    trazas = []  # lista de recorridos que mejoran la solución
    
    longitudes_traza = []  # longitudes asociadas a cada mejora registrada

    inicio = time.perf_counter() # marca de tiempo de inicio
    nodos = list(range(total)) # índices de las ciudades

    for permutacion in itertools.permutations(nodos[1:]): # genera rutas fijando el nodo 0 como inicio
        recorrido = [0] + list(permutacion)  # arma el recorrido completo partiendo desde 0
        L = longitud_recorrido(instancia, recorrido)  # calcula la longitud del recorrido actual

        if L < mejor_longitud:  # si mejora la mejor longitud conocida
            mejor_longitud = L # actualiza la mejor distancia
            mejor_recorrido = recorrido # guarda el recorrido óptimo
            trazas.append(recorrido.copy()) # registra la traza de mejora
            longitudes_traza.append(L) # guarda la longitud de la mejora

    duracion = time.perf_counter() - inicio # tiempo total de ejecución
     
    print(
        f"[Exhaustivo] ciudades={total}, L*={mejor_longitud:.4f}, "
        f"tiempo={duracion:.4f} s" 
    )  # mensaje de diagnóstico en consola
 
    return {
            "recorrido": mejor_recorrido,  # recorrido óptimo hallado
            "longitud": mejor_longitud,  # distancia mínima
            "tiempo": duracion # duración del algoritmo
        }, trazas, longitudes_traza  # retorna solución y trazas para animación