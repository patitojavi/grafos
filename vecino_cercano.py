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
    # Obtiene la matriz de distancias y el total de ciudades
    matriz = instancia["matriz_distancias"]
    total = total_ciudades(instancia)

    # Inicio de la medicion del tiempo
    inicio_tiempo = time.perf_counter()

    # Conjunto de ciudades no visitadas y recorrido inicial
    pendientes = set(range(total))
    recorrido: List[int] = [inicio]
    pendientes.remove(inicio)

    # Construccion del recorrido mediante el vecino mas cercano
    while pendientes:
        actual = recorrido[-1]
        siguiente = min(
            pendientes,
            key=lambda ciudad: (matriz[actual][ciudad], ciudad),
        )
        recorrido.append(siguiente)
        pendientes.remove(siguiente)

    # Calculo de la longitud total y tiempo empleado
    L = longitud_recorrido(instancia, recorrido)
    duracion = time.perf_counter() - inicio_tiempo

    # Creacion de la solucion final
    solucion = crear_solucion(
        recorrido=recorrido,
        longitud=L,
        metodo="vecino_cercano",
        tiempo=duracion,
    )

    # Registro basico de resultados
    print(
        f"[Vecino Cercano] inicio={inicio}, ciudades={total}, "
        f"L={L:.4f}, tiempo={duracion:.6f} s"
    )

    # Retorno de la solucion y del recorrido generado
    return solucion, recorrido
