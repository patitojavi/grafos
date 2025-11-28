import tkinter as tk  # módulo base de interfaces gráficas en python

from matplotlib.animation import FuncAnimation  # clase para crear animaciones cuadro a cuadro
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # integra figuras de matplotlib en tkinter
from matplotlib.figure import Figure  # objeto figura principal de matplotlib

from datos_viajante import coordenadas_ciudades  # función auxiliar que entrega las coordenadas x,y de las ciudades

# panel gráfico para ver recorridos y animaciones
# esta función crea un frame de tkinter que contiene una figura de matplotlib
# con dos subgráficos: uno para búsqueda exhaustiva y otro para vecino cercano

def crear_panel_graficos(master, instancia):
    # crea un frame hijo dentro del contenedor master (normalmente la ventana raíz)
    frame = tk.Frame(master)

    # guarda la instancia completa del problema (incluye ciudades y otros datos)
    frame.instancia = instancia
    # extrae y guarda la lista de ciudades desde la instancia
    frame.ciudades = instancia["ciudades"]

    # crea una figura de matplotlib de tamaño 12x5.5 pulgadas y resolución de 100 dpi
    figura = Figure(figsize=(12, 5.5), dpi=100)
    # agrega un subplot en la posición 1 de una grilla de 1 fila x 2 columnas (eje para método exhaustivo)
    eje_exhaustivo = figura.add_subplot(1, 2, 1)
    # agrega un segundo subplot en la posición 2 (eje para método vecino cercano)
    eje_vecino = figura.add_subplot(1, 2, 2)

    # guarda las referencias a figura y ejes en el frame para que otras funciones internas puedan usarlos
    frame.figura = figura
    frame.eje_exhaustivo = eje_exhaustivo
    frame.eje_vecino = eje_vecino

    # crea un canvas que permite mostrar la figura dentro del widget de tkinter
    lienzo = FigureCanvasTkAgg(figura, master=frame)
    # empaqueta el widget asociado al canvas para que llene todo el espacio disponible
    lienzo.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    # guarda la referencia al canvas en el frame
    frame.lienzo = lienzo

    # inicializa referencias a animaciones como none (no hay animaciones corriendo al inicio)
    frame.animacion_exhaustiva: FuncAnimation | None = None
    frame.animacion_vecino: FuncAnimation | None = None
    # referencias a líneas dibujadas en cada eje (se asignan luego en las funciones de animación)
    frame.linea_exhaustiva = None
    frame.linea_vecino = None

    def dibujar_ciudades(eje):
        # pinta los nodos base (las ciudades) en el eje que se reciba como parámetro
        # obtiene listas de coordenadas x e y desde la función auxiliar
        xs, ys = coordenadas_ciudades(frame.instancia)
        # dibuja los puntos de las ciudades como un scatter: tamaño 60, amarillo, borde negro
        eje.scatter(xs, ys, s=60, color="yellow", edgecolor="black", zorder=3)

        # recorre todas las ciudades y les pone una etiqueta con índice y nombre al lado del punto
        for i, ciudad in enumerate(frame.ciudades):
            eje.annotate(
                f"{i}:{ciudad['nombre']}",  # texto a mostrar 
                (xs[i], ys[i]),             # posición base del texto 
                textcoords="offset points", # indica que el texto se desplazará respecto al punto
                xytext=(4, 4),              # desplazamiento en pixeles (x,y) respecto al punto
                fontsize=8,                 # tamaño de letra pequeño
            )

    def preparar_ejes():
        # deja ambos ejes listos antes de mostrar recorridos o animaciones

        # limpia todo lo dibujado previamente en el eje de búsqueda exhaustiva
        eje_exhaustivo.clear()
        # título del gráfico de búsqueda exhaustiva
        eje_exhaustivo.set_title(
            "Búsqueda exhaustiva\n(mejor recorrido registrado)"
        )
        # etiquetas de los ejes x e y para el gráfico exhaustivo
        eje_exhaustivo.set_xlabel("Longitud (deg)")
        eje_exhaustivo.set_ylabel("Latitud (deg)")
        # dibuja los puntos de las ciudades sobre el eje exhaustivo
        dibujar_ciudades(eje_exhaustivo)
        # activa una grilla suave de fondo para ayudar a la lectura
        eje_exhaustivo.grid(True, alpha=0.3)

        # hace lo mismo para el eje del método vecino cercano
        eje_vecino.clear()
        eje_vecino.set_title("Vecino más cercano")
        eje_vecino.set_xlabel("Longitud (deg)")
        eje_vecino.set_ylabel("Latitud (deg)")
        dibujar_ciudades(eje_vecino)
        eje_vecino.grid(True, alpha=0.3)

        # le dice al canvas que actualice el dibujo de la figura en pantalla
        lienzo.draw_idle()

    def recorrido_a_xy(recorrido):
        # convierte una lista de índices de ciudades 
        xs, ys = coordenadas_ciudades(frame.instancia)
        # arma la lista de x siguiendo el orden del recorrido más el retorno a la ciudad inicial
        camino_x = [float(xs[i]) for i in recorrido] + [float(xs[recorrido[0]])]
        # arma la lista de y de la misma forma
        camino_y = [float(ys[i]) for i in recorrido] + [float(ys[recorrido[0]])]
        # retorna ambas listas listas para graficar con plot
        return camino_x, camino_y

    def detener_animacion(anim):
        # detiene de forma segura una animación si existe y está activa
        if anim is not None and anim.event_source is not None:
            # event_source controla el temporizador interno de la animación
            anim.event_source.stop()

    def animar_exhaustivo(traza, longitudes, on_finish=None):
        # anima la búsqueda exhaustiva paso a paso mostrando el "mejor recorrido" registrado en cada iteración
        # primero detiene una animación anterior si estuviera corriendo
        detener_animacion(frame.animacion_exhaustiva)

        # limpia el contenido del eje de búsqueda exhaustiva
        eje_exhaustivo.clear()
        # vuelve a configurar los ejes x e y
        eje_exhaustivo.set_xlabel("Longitud (deg)")
        eje_exhaustivo.set_ylabel("Latitud (deg)")
        # vuelve a dibujar las ciudades sobre el eje
        dibujar_ciudades(eje_exhaustivo)
        # reactiva la grilla
        eje_exhaustivo.grid(True, alpha=0.3)

        # crea una línea inicial vacía en el eje (sin datos), con un grosor de 2.5
        (linea_exhaustiva,) = eje_exhaustivo.plot([], [], linewidth=2.5)
        # guarda la referencia a la línea en el frame por si se necesita más adelante
        frame.linea_exhaustiva = linea_exhaustiva

        # número total de cuadros de la animación (uno por cada elemento en la traza)
        cuadros = len(traza)

        def init():
            # función de inicialización de la animación
            # deja la línea sin datos al comienzo
            linea_exhaustiva.set_data([], [])
            # configura el título inicial del gráfico
            eje_exhaustivo.set_title(
                "Búsqueda exhaustiva\n(mejor recorrido registrado)"
            )
            # debe retornar una tupla con los artistas que se van a animar
            return (linea_exhaustiva,)

        def actualizar(indice: int):
            # función que se llama en cada cuadro de la animación
            # toma el recorrido y la longitud correspondientes a este índice
            recorrido = traza[indice]
            L = longitudes[indice]
            # convierte el recorrido a coordenadas x e y listas para graficar
            cx, cy = recorrido_a_xy(recorrido)
            # actualiza los datos de la línea con el nuevo camino
            linea_exhaustiva.set_data(cx, cy)
            # actualiza el título para mostrar la mejor longitud actual y el progreso
            eje_exhaustivo.set_title(
                f"Búsqueda exhaustiva\nMejor L*={L:.3f} "
                f"(mejora {indice+1}/{cuadros})"
            )
            # retorna otra vez la línea como artista a redibujar
            return (linea_exhaustiva,)

        # crea la animación usando funcanimation:
        # - figura: sobre qué figura se dibuja
        # - actualizar: función que se ejecuta en cada cuadro
        # - init_func: función de inicialización
        # - frames: cantidad de cuadros
        # - interval: tiempo en milisegundos entre cuadros
        # - blit: false para redibujar todo el eje (más simple)
        # - repeat: false para no repetir en bucle
        frame.animacion_exhaustiva = FuncAnimation(
            figura,
            actualizar,
            init_func=init,
            frames=cuadros,
            interval=400,
            blit=False,
            repeat=False,
        )

        # le indica al canvas que debe redibujar la figura
        lienzo.draw_idle()

        # si se entrega una función on_finish, se programa su ejecución
        # después de que la animación haya terminado (tiempo total aproximado)
        if on_finish is not None:
            total_ms = cuadros * 400 + 100  # tiempo total estimado
            # after programa una función para ejecutarse después de cierto tiempo en ms
            frame.after(total_ms, on_finish)

    def animar_vecino(nombre_inicio, recorrido_vecino, on_finish=None):
        # anima el recorrido construido por el algoritmo de vecino más cercano
        # primero detiene cualquier animación anterior del eje vecino
        detener_animacion(frame.animacion_vecino)

        # limpia el eje del método vecino cercano
        eje_vecino.clear()
        # vuelve a establecer las etiquetas de los ejes
        eje_vecino.set_xlabel("Longitud (deg)")
        eje_vecino.set_ylabel("Latitud (deg)")
        # dibuja las ciudades de fondo
        dibujar_ciudades(eje_vecino)
        eje_vecino.grid(True, alpha=0.3)

        # crea una línea vacía que representará el recorrido del vecino cercano
        (linea_vecino,) = eje_vecino.plot([], [], linewidth=2.5)
        frame.linea_vecino = linea_vecino

        # convierte el recorrido de índices a listas de coordenadas x e y
        camino_x, camino_y = recorrido_a_xy(recorrido_vecino)
        # número total de cuadros de la animación (un punto nuevo por cuadro)
        cuadros = len(camino_x)

        def init():
            # función de inicialización para la animación de vecino cercano
            linea_vecino.set_data([], [])
            # título inicial del gráfico, indicando la ciudad de inicio
            eje_vecino.set_title(
                f"Vecino más cercano (inicio: {nombre_inicio})"
            )
            return (linea_vecino,)

        def actualizar(indice: int):
            # función que se llama en cada cuadro para avanzar el camino
            # se muestran los puntos desde el inicio hasta el índice actual
            linea_vecino.set_data(
                camino_x[: indice + 1],
                camino_y[: indice + 1],
            )
            # actualiza el título mostrando el paso actual y el total
            eje_vecino.set_title(
                f"Vecino más cercano (inicio: {nombre_inicio})\n"
                f"Paso {indice+1}/{cuadros}"
            )
            return (linea_vecino,)

        # crea la animación para el método vecino más cercano con la misma lógica de intervalos
        frame.animacion_vecino = FuncAnimation(
            figura,
            actualizar,
            init_func=init,
            frames=cuadros,
            interval=400,
            blit=False,
            repeat=False,
        )

        # redibuja la figura en el lienzo
        lienzo.draw_idle()

        # programa la función on_finish si se proporcionó
        if on_finish is not None:
            total_ms = cuadros * 400 + 100
            frame.after(total_ms, on_finish)

    # expone las funciones de animación como "métodos" del frame
    # esto permite que otros módulos llamen frame.animar_exhaustivo(...) o frame.animar_vecino(...)
    frame.animar_exhaustivo = animar_exhaustivo
    frame.animar_vecino = animar_vecino

    # deja los ejes listos con las ciudades dibujadas antes de mostrar el frame
    preparar_ejes()

    # retorna el frame completo para integrarlo en la interfaz principal
    return frame
    