# Proyecto Final Grafos 
# Explorador del Problema del Viajante

Aplicación de escritorio escrita en Python que compara dos enfoques para resolver el Problema del Viajante de Comercio (TSP):

- **Búsqueda exhaustiva** para obtener la solución óptima (limitada a instancias pequeñas por su costo combinatorio).
- **Heurística del vecino más cercano** para construir rápidamente una ruta factible desde una ciudad inicial.

La interfaz gráfica, construida con `tkinter` y `matplotlib`, permite visualizar las ciudades en un mapa 2D y anima los recorridos generados por ambos métodos, mostrando tiempos de cómputo, longitudes y el _gap_ de optimalidad entre la solución heurística y la óptima.

## Requisitos

- Python 3.10 o superior.
- Dependencias de Python:
  - `matplotlib` (para los gráficos y animaciones embebidos en `tkinter`).
- `tkinter` suele venir incluido con las distribuciones oficiales de Python. Si tu entorno no lo trae, instálalo mediante el gestor de paquetes de tu sistema operativo.

Instala las dependencias de Python con:

```bash
python -m pip install matplotlib
```

## Estructura del proyecto

- `main.py`: punto de entrada. Define cuántas ciudades usar, arma la instancia del TSP y lanza la interfaz gráfica.
- `datos_viajante.py`: define el catálogo de ciudades con coordenadas, construye la matriz de distancias y calcula la longitud total de un recorrido.
- `buscador_exhaustivo.py`: implementa la búsqueda exhaustiva (fuerza bruta) con registro de las mejoras sucesivas. Limitado a 11 ciudades por defecto.
- `vecino_cercano.py`: contiene la heurística del vecino más cercano y devuelve el recorrido construido junto con su tiempo y longitud.
- `interfaz_viajante.py`: arma la ventana principal, conecta los paneles de control y gráficos y coordina la ejecución de los algoritmos.
- `interfaz_controles.py`: panel superior con botones para lanzar cada método, selector de ciudad inicial y etiquetas de tiempos/gap.
- `interfaz_graficos.py`: configura la figura de `matplotlib`, dibuja las ciudades y anima los recorridos de ambos enfoques.

## Cómo ejecutar

Desde la raíz del proyecto:

```bash
python main.py
```

El programa abre una ventana titulada **"Problema del Viajante - Exhaustivo vs Vecino Cercano"** con dos áreas principales:

1. **Panel de controles (superior)**
   - Botón **"Ejecutar búsqueda exhaustiva"**: calcula la ruta óptima (si el número de ciudades no supera el límite) y anima las mejoras registradas.
   - Selector **"Ciudad inicial"** y botón **"Ejecutar vecino más cercano"**: lanza la heurística partiendo de la ciudad elegida.
   - Etiquetas informativas de tiempo de ejecución para cada método y del _gap_ de optimalidad (si ya existe una solución óptima).

2. **Panel de gráficos (inferior)**
   - Subgráfico izquierdo: anima el mejor recorrido encontrado por la búsqueda exhaustiva, mostrando la longitud mínima alcanzada en cada mejora.
   - Subgráfico derecho: anima paso a paso la ruta armada por el vecino más cercano desde la ciudad inicial seleccionada.

## Parámetros y límites

- El número de ciudades se define en `main.py` (variable `total_ciudades`). Se recomienda no exceder 11 ciudades si se desea usar la búsqueda exhaustiva (`MAX_CIUDADES_EXHAUSTIVO` en `buscador_exhaustivo.py`).
- El catálogo de ciudades y sus coordenadas se encuentra en `datos_viajante.py` y puede editarse para probar otros conjuntos.

## Flujo interno

1. `main.py` toma un subconjunto del catálogo (`obtener_ciudades`) y construye la instancia del problema (`crear_instancia_viajante`).
2. `interfaz_viajante.iniciar_interfaz` crea la ventana principal y comparte estado entre controles y gráficos.
3. Al pulsar **búsqueda exhaustiva**, `resolver_exhaustivo_con_traza` evalúa todas las permutaciones (fijando la primera ciudad) y devuelve la mejor ruta y una traza de mejoras para animar.
4. Al pulsar **vecino más cercano**, `resolver_vecino_con_traza` elige iterativamente la ciudad no visitada más cercana, guarda el recorrido y lo anima.
5. Si existe una solución óptima previa, se calcula el _gap_ porcentual entre el vecino cercano y el óptimo.

## Notas y sugerencias

- Aumentar mucho el número de ciudades hace que la búsqueda exhaustiva crezca rápidamente en tiempo; la heurística sigue siendo rápida pero no garantiza optimalidad.
- Si deseas partir desde otra ciudad, selecciónala en el combo **"Ciudad inicial"** antes de ejecutar el vecino más cercano.
- Las animaciones pueden detenerse o reiniciarse al volver a ejecutar cada método; el panel de gráficos se limpia y redibuja automáticamente.

