import itertools
import time

from datos_viajante import longitud_recorrido

MAX_CIUDADES_EXHAUSTIVO = 11

def resolver_exhaustivo_con_traza(instancia):
    ciudades = instancia["ciudades"]
    total = len(ciudades)
    
    if total > MAX_CIUDADES_EXHAUSTIVO:
        # Validación simple
        raise ValueError(f"Demasiadas ciudades para fuerza bruta ({total}). Máximo {MAX_CIUDADES_EXHAUSTIVO}.")
    
    mejor_recorrido = None
    mejor_longitud = float("inf")

    trazas = []
    
    longitudes_traza = []

    inicio = time.perf_counter()
    nodos = list(range(total))

    for permutacion in itertools.permutations(nodos[1:]):
        recorrido = [0] + list(permutacion)
        L = longitud_recorrido(instancia, recorrido)

        if L < mejor_longitud:
            mejor_longitud = L
            mejor_recorrido = recorrido
            trazas.append(recorrido.copy())
            longitudes_traza.append(L)

    duracion = time.perf_counter() - inicio
    
    print(
        f"[Exhaustivo] ciudades={total}, L*={mejor_longitud:.4f}, "
        f"tiempo={duracion:.4f} s"
    )

    return {
            "recorrido": mejor_recorrido,
            "longitud": mejor_longitud,
            "tiempo": duracion
        }, trazas, longitudes_traza