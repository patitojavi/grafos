import tkinter as tk

from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from datos_viajante import coordenadas_ciudades

# Panel grafico para ver recorridos y animaciones

def crear_panel_graficos(master, instancia):
    frame = tk.Frame(master)

    frame.instancia = instancia
    frame.ciudades = instancia["ciudades"]

    figura = Figure(figsize=(12, 5.5), dpi=100)
    eje_exhaustivo = figura.add_subplot(1, 2, 1)
    eje_vecino = figura.add_subplot(1, 2, 2)

    frame.figura = figura
    frame.eje_exhaustivo = eje_exhaustivo
    frame.eje_vecino = eje_vecino

    lienzo = FigureCanvasTkAgg(figura, master=frame)
    lienzo.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    frame.lienzo = lienzo

    frame.animacion_exhaustiva: FuncAnimation | None = None
    frame.animacion_vecino: FuncAnimation | None = None
    frame.linea_exhaustiva = None
    frame.linea_vecino = None

    def dibujar_ciudades(eje):
        # Pinta nodos base en ambos ejes
        xs, ys = coordenadas_ciudades(frame.instancia)
        eje.scatter(xs, ys, s=60, color="yellow", edgecolor="black", zorder=3)
        for i, ciudad in enumerate(frame.ciudades):
            eje.annotate(
                f"{i}:{ciudad['nombre']}",
                (xs[i], ys[i]),
                textcoords="offset points",
                xytext=(4, 4),
                fontsize=8,
            )

    def preparar_ejes():
        eje_exhaustivo.clear()
        eje_exhaustivo.set_title(
            "Búsqueda exhaustiva\n(mejor recorrido registrado)"
        )
        eje_exhaustivo.set_xlabel("Longitud (deg)")
        eje_exhaustivo.set_ylabel("Latitud (deg)")
        dibujar_ciudades(eje_exhaustivo)
        eje_exhaustivo.grid(True, alpha=0.3)

        eje_vecino.clear()
        eje_vecino.set_title("Vecino más cercano")
        eje_vecino.set_xlabel("Longitud (deg)")
        eje_vecino.set_ylabel("Latitud (deg)")
        dibujar_ciudades(eje_vecino)
        eje_vecino.grid(True, alpha=0.3)

        lienzo.draw_idle()

    def recorrido_a_xy(recorrido):
        xs, ys = coordenadas_ciudades(frame.instancia)
        camino_x = [float(xs[i]) for i in recorrido] + [float(xs[recorrido[0]])]
        camino_y = [float(ys[i]) for i in recorrido] + [float(ys[recorrido[0]])]
        return camino_x, camino_y

    def detener_animacion(anim):
        if anim is not None and anim.event_source is not None:
            anim.event_source.stop()

    def animar_exhaustivo(traza, longitudes, on_finish=None):
        # Anima la busqueda exhaustiva paso a paso
        detener_animacion(frame.animacion_exhaustiva)

        eje_exhaustivo.clear()
        eje_exhaustivo.set_xlabel("Longitud (deg)")
        eje_exhaustivo.set_ylabel("Latitud (deg)")
        dibujar_ciudades(eje_exhaustivo)
        eje_exhaustivo.grid(True, alpha=0.3)

        (linea_exhaustiva,) = eje_exhaustivo.plot([], [], linewidth=2.5)
        frame.linea_exhaustiva = linea_exhaustiva

        cuadros = len(traza)

        def init():
            linea_exhaustiva.set_data([], [])
            eje_exhaustivo.set_title(
                "Búsqueda exhaustiva\n(mejor recorrido registrado)"
            )
            return (linea_exhaustiva,)

        def actualizar(indice: int):
            recorrido = traza[indice]
            L = longitudes[indice]
            cx, cy = recorrido_a_xy(recorrido)
            linea_exhaustiva.set_data(cx, cy)
            eje_exhaustivo.set_title(
                f"Búsqueda exhaustiva\nMejor L*={L:.3f} "
                f"(mejora {indice+1}/{cuadros})"
            )
            return (linea_exhaustiva,)

        from matplotlib.animation import FuncAnimation  # por si hiciera falta local

        frame.animacion_exhaustiva = FuncAnimation(
            figura,
            actualizar,
            init_func=init,
            frames=cuadros,
            interval=400,
            blit=False,
            repeat=False,
        )

        lienzo.draw_idle()

        if on_finish is not None:
            total_ms = cuadros * 400 + 100
            frame.after(total_ms, on_finish)

    def animar_vecino(nombre_inicio, recorrido_vecino, on_finish= None):
        # Anima el recorrido construido por vecino cercano
        detener_animacion(frame.animacion_vecino)

        eje_vecino.clear()
        eje_vecino.set_xlabel("Longitud (deg)")
        eje_vecino.set_ylabel("Latitud (deg)")
        dibujar_ciudades(eje_vecino)
        eje_vecino.grid(True, alpha=0.3)

        (linea_vecino,) = eje_vecino.plot([], [], linewidth=2.5)
        frame.linea_vecino = linea_vecino

        camino_x, camino_y = recorrido_a_xy(recorrido_vecino)
        cuadros = len(camino_x)

        def init():
            linea_vecino.set_data([], [])
            eje_vecino.set_title(
                f"Vecino más cercano (inicio: {nombre_inicio})"
            )
            return (linea_vecino,)

        def actualizar(indice: int):
            linea_vecino.set_data(
                camino_x[: indice + 1],
                camino_y[: indice + 1],
            )
            eje_vecino.set_title(
                f"Vecino más cercano (inicio: {nombre_inicio})\n"
                f"Paso {indice+1}/{cuadros}"
            )
            return (linea_vecino,)

        from matplotlib.animation import FuncAnimation

        frame.animacion_vecino = FuncAnimation(
            figura,
            actualizar,
            init_func=init,
            frames=cuadros,
            interval=400,
            blit=False,
            repeat=False,
        )

        lienzo.draw_idle()

        if on_finish is not None:
            total_ms = cuadros * 400 + 100
            frame.after(total_ms, on_finish)

    frame.animar_exhaustivo = animar_exhaustivo
    frame.animar_vecino = animar_vecino

    preparar_ejes()

    return frame
