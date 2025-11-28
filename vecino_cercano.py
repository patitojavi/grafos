import time  

from datos_viajante import longitud_recorrido  # función que calcula la longitud total de un recorrido

# heurística de vecino cercano con traza
# esta función construye una solución al problema del viajante eligiendo siempre
# la siguiente ciudad más cercana no visitada, partiendo desde un índice de ciudad "inicio"
def resolver_vecino_con_traza(instancia, inicio=0):
    # obtiene la matriz de distancias entre ciudades desde la instancia
    matriz = instancia["matriz_distancias"]
    # obtiene la lista de ciudades 
    ciudades = instancia["ciudades"]
    # cantidad total de ciudades en la instancia
    n = len(ciudades)

    # toma el tiempo actual (alta precisión) para medir la duración del algoritmo
    inicio_tiempo = time.perf_counter()

    # conjunto de índices de ciudades ya visitadas
    visitados = set()
    # lista que almacenará el recorrido en el orden en que se visitan las ciudades
    recorrido = [inicio]
    # marca la ciudad inicial como visitada
    visitados.add(inicio)
    
    # índice de la ciudad actual (donde está "el viajante" en este momento)
    actual = inicio

    # mientras aún falten ciudades por visitar
    while len(visitados) < n:
        # inicializa la mejor distancia con infinito 
        mejor_distancia = float("inf")
        # índice de la siguiente ciudad candidata 
        siguiente_ciudad = -1
        
        # recorre todas las ciudades posibles para buscar la no visitada más cercana
        for candidato in range(n):
            # solo consideramos las ciudades que aún no han sido visitadas
            if candidato not in visitados:
                # distancia desde la ciudad actual hasta la candidata
                dist = matriz[actual][candidato]
                # si encontramos una distancia menor que la mejor conocida hasta ahora, actualizamos
                if dist < mejor_distancia:
                    mejor_distancia = dist
                    siguiente_ciudad = candidato
        
        # agrega la ciudad elegida al recorrido
        recorrido.append(siguiente_ciudad)
        # la marca como visitada
        visitados.add(siguiente_ciudad)
        # actualiza la ciudad actual a la nueva ciudad elegida
        actual = siguiente_ciudad

    # calcula la longitud total del recorrido completo 
    largo_final = longitud_recorrido(instancia, recorrido)
    
    # toma el tiempo al finalizar el algoritmo
    fin_tiempo = time.perf_counter()
    # calcula la duración como la diferencia entre inicio y fin
    duracion = fin_tiempo - inicio_tiempo

    # imprime un  resumen en consola 
    print(
        f"[Vecino] Inicio: {inicio}, Ciudades: {n}, "
        f"Longitud: {largo_final:.2f}, Tiempo: {duracion:.5f}s"
    )

    # retorna dos cosas:
    # 1) un diccionario con datos de la solución (recorrido, longitud, tiempo)
    # 2) el recorrido como lista de índices (para usarlo directamente en las animaciones)
    return {
        "recorrido": recorrido,
        "longitud": largo_final,
        "tiempo": duracion
    }, recorrido
