from datos_viajante import obtener_ciudades, crear_instancia_viajante

def main() -> None:
    total_ciudades = 9 # maximo 11 ciudades debio al conjunto de datos
    ciudades = obtener_ciudades(total_ciudades) # obtiene las ciudades
    instancia = crear_instancia_viajante(ciudades) # crea la instancia del viajante

if __name__ == "__main__":
    main()
