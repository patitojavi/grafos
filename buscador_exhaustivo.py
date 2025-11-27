import itertools
import time
from typing import List, Tuple

from datos_viajante import (
    InstanciaViajante,
    SolucionViajante,
    total_ciudades,
    longitud_recorrido,
    crear_solucion,
)

MAX_CIUDADES_EXHAUSTIVO = 11

def resolver_exhaustivo_con_traza(
    instancia: InstanciaViajante,
) -> Tuple[SolucionViajante, List[List[int]], List[float]]:
    total = total_ciudades(instancia)
    if total > MAX_CIUDADES_EXHAUSTIVO:
        raise ValueError(
            f"Búsqueda exhaustiva impracticable para {total} ciudades. "
            f"Límite configurado: {MAX_CIUDADES_EXHAUSTIVO}."
        )

    mejor_recorrido: List[int] | None = None
    mejor_longitud = float("inf")
    trazas: List[List[int]] = []
    longitudes_traza: List[float] = []

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

    solucion = crear_solucion(
        recorrido=mejor_recorrido or [],
        longitud=mejor_longitud,
        metodo="exhaustivo",
        tiempo=duracion,
    )

    print(
        f"[Exhaustivo] ciudades={total}, L*={mejor_longitud:.4f}, "
        f"tiempo={duracion:.4f} s"
    )

    return solucion, trazas, longitudes_traza
