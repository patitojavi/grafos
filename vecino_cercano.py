import time
from datos_viajante import longitud_recorrido

# Heuristica de vecino cercano con traza
def resolver_vecino_con_traza(instancia, inicio=0):
    matriz = instancia["matriz_distancias"]
    ciudades = instancia["ciudades"]
    n = len(ciudades)

    inicio_tiempo = time.perf_counter()

    visitados = set()
    recorrido = [inicio]
    visitados.add(inicio)
    
    actual = inicio

    # Mientras falten ciudades por visitar
    while len(visitados) < n:
        mejor_distancia = float("inf")
        siguiente_ciudad = -1
        
        # Busca el no visitado mas cercano
        for candidato in range(n):
            if candidato not in visitados:
                dist = matriz[actual][candidato]
                if dist < mejor_distancia:
                    mejor_distancia = dist
                    siguiente_ciudad = candidato
        
        recorrido.append(siguiente_ciudad)
        visitados.add(siguiente_ciudad)
        actual = siguiente_ciudad

    largo_final = longitud_recorrido(instancia, recorrido)
    
    fin_tiempo = time.perf_counter()
    duracion = fin_tiempo - inicio_tiempo

    print(f"[Vecino] Inicio: {inicio}, Ciudades: {n}, Longitud: {largo_final:.2f}, Tiempo: {duracion:.5f}s")

    return {
        "recorrido": recorrido,
        "longitud": largo_final,
        "tiempo": duracion
    }, recorrido
