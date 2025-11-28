from datos_viajante import obtener_ciudades, crear_instancia_viajante  # funciones para generar la lista de ciudades y armar la instancia del problema
from interfaz_viajante import iniciar_interfaz  # función que construye y lanza la interfaz gráfica principal

def main() -> None:
    # define cuántas ciudades se usarán en la instancia del problema
    # nota: si se aumenta demasiado este número, la búsqueda exhaustiva se vuelve muy costosa
    total_ciudades = 9  # máximo recomendado 11 ciudades por la explosión combinatoria de rutas

    # obtiene una lista de 'total_ciudades' ciudades a partir de los datos definidos en datos_viajante
    ciudades = obtener_ciudades(total_ciudades)

    # crea una instancia del problema del viajante usando la lista de ciudades (distancias, estructura, etc.)
    instancia = crear_instancia_viajante(ciudades)

    # inicia la interfaz gráfica, pasando la instancia completa del problema
    iniciar_interfaz(instancia)


# este bloque se ejecuta solo si el archivo se corre directamente 
if __name__ == "__main__":
    main()
