import time
from typing import List, Tuple

from datos_viajante import (
    InstanciaViajante,
    SolucionViajante,
    total_ciudades,
    longitud_recorrido,
    crear_solucion,
)


def resolver_vecino_con_traza(
    instancia: InstanciaViajante,
    inicio: int = 0,
) -> Tuple[SolucionViajante, List[int]]:
    matriz = instancia["matriz_distancias"]
    total = total_ciudades(instancia)

    inicio_tiempo = time.perf_counter()

    pendientes = set(range(total))
    recorrido: List[int] = [inicio]
    pendientes.remove(inicio)

    while pendientes:
        actual = recorrido[-1]
        siguiente = min(
            pendientes,
            key=lambda ciudad: (matriz[actual][ciudad], ciudad),
        )
        recorrido.append(siguiente)
        pendientes.remove(siguiente)

    L = longitud_recorrido(instancia, recorrido)
    duracion = time.perf_counter() - inicio_tiempo

    solucion = crear_solucion(
        recorrido=recorrido,
        longitud=L,
        metodo="vecino_cercano",
        tiempo=duracion,
    )

    print(
        f"[Vecino Cercano] inicio={inicio}, ciudades={total}, "
        f"L={L:.4f}, tiempo={duracion:.6f} s"
    )

    return solucion, recorrido
