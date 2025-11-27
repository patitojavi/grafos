from datos_viajante import obtener_ciudades, crear_instancia_viajante
from interfaz_viajante import iniciar_interfaz

def main() -> None:
    total_ciudades = 9 # maximo 11 ciudades o explota debito a la gran cantidad de rutas
    ciudades = obtener_ciudades(total_ciudades) 
    instancia = crear_instancia_viajante(ciudades)

    iniciar_interfaz(instancia)

if __name__ == "__main__":
    main()
