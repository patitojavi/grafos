import tkinter as tk  # librería principal para interfaces gráficas
from tkinter import messagebox  # cuadros de diálogo para mostrar mensajes

from datos_viajante import coordenadas_ciudades  # datos base de las ciudades y sus posiciones 
from buscador_exhaustivo import resolver_exhaustivo_con_traza, MAX_CIUDADES_EXHAUSTIVO  # fuerza bruta y límite de ciudades
from vecino_cercano import resolver_vecino_con_traza  # heurística de vecino más cercano 
from interfaz_controles import crear_panel_controles  # panel con botones y combo
from interfaz_graficos import crear_panel_graficos  # panel para gráficos y animaciones

# ventana principal y manejo de interacción
def iniciar_interfaz(instancia):
    """
    crea y lanza la ventana principal del programa,
    conectando los paneles de controles y gráficos con la lógica del problema.
    """
    raiz = tk.Tk()  # ventana raíz de tkinter
    raiz.title("Problema del Viajante - Exhaustivo vs Vecino Cercano")  # título de la ventana
    raiz.geometry("1500x750")  # tamaño inicial de la ventana

    ciudades = instancia["ciudades"]  # lista de ciudades que forman la instancia del problema

    # estado compartido entre botones y gráficos
    estado = {
        "solucion_optima": None,    # almacena solución obtenida por búsqueda exhaustiva
        "solucion_vecino": None,     # almacena solución del vecino más cercano
        "traza_exhaustiva": None,      # pasos intermedios del método exhaustivo
        "longitudes_exhaustivas": None, # longitudes asociadas a cada paso de la traza
    }

    def ejecutar_exhaustivo():
        """
        controla la ejecución del método de búsqueda exhaustiva:
        - verifica el límite de ciudades
        - llama al resolutor
        - actualiza etiquetas y gráficos
        """
        total = len(ciudades)  # cantidad de ciudades actuales
        if total > MAX_CIUDADES_EXHAUSTIVO:
            # si hay demasiadas ciudades, se informa y se cancela la ejecución
            messagebox.showinfo(
                "Búsqueda exhaustiva",
                f"{total} ciudades.\n"
                f"el límite para fuerza bruta es {MAX_CIUDADES_EXHAUSTIVO}.\n"
                "reduce la cantidad de ciudades para ejecutar este método.",
            )
            return

        # referencias rápidas a los widgets del panel de controles
        btn = panel_controles.boton_exhaustivo          # botón de búsqueda exhaustiva
        lbl = panel_controles.etiqueta_tiempo_exhaustivo  # etiqueta de tiempo exhaustivo

        # deshabilita el botón durante el cálculo
        btn.state(["disabled"])
        lbl.config(text="tiempo exhaustivo: calculando...")

        try:
            # ejecuta el método exhaustivo con traza y longitudes
            solucion, traza, longitudes = resolver_exhaustivo_con_traza(instancia)
        except Exception as error:
            # si ocurre un error, se informa y se reactiva el botón
            messagebox.showerror("Error", f"fallo en búsqueda exhaustiva:\n{error}")
            btn.state(["!disabled"])
            return

        # guarda resultados en el estado compartido
        estado["solucion_optima"] = solucion
        estado["traza_exhaustiva"] = traza
        estado["longitudes_exhaustivas"] = longitudes

        # actualiza etiqueta con tiempo y longitud óptima
        lbl.config(
            text=(
                f"tiempo exhaustivo: {solucion['tiempo']:.4f} s "
                f"(l*={solucion['longitud']:.3f})"
            )
        )

        # lanza la animación del recorrido exhaustivo en el panel de gráficos
        panel_graficos.animar_exhaustivo(
            traza,
            longitudes,
            on_finish=lambda: btn.state(["!disabled"]),  # reactiva el botón al terminar
        )

    def ejecutar_vecino():
        """
        controla la ejecución del método de vecino más cercano:
        - toma la ciudad inicial seleccionada
        - llama al algoritmo heurístico
        - actualiza etiquetas, gráficos y el cálculo del gap si existe el óptimo
        """
        # referencias a controles del panel
        btn = panel_controles.boton_vecino
        lbl = panel_controles.etiqueta_tiempo_vecino
        lbl_gap = panel_controles.etiqueta_gap

        # deshabilita el botón durante el cálculo
        btn.state(["disabled"])
        lbl.config(text="tiempo vecino: calculando...")

        # obtiene la ciudad inicial elegida en el combo
        nombre_inicio = panel_controles.ciudad_inicial.get()
        # encuentra el índice correspondiente a esa ciudad
        indice_inicio = next(
            i
            for i, ciudad in enumerate(ciudades)
            if ciudad["nombre"] == nombre_inicio
        )

        try:
            # ejecuta el método vecino cercano con traza del recorrido
            solucion_vecino, recorrido_vecino = resolver_vecino_con_traza(
                instancia, indice_inicio
            )
        except Exception as error:
            # si algo falla, se muestra el error y se reactiva el botón
            messagebox.showerror("Error", f"fallo en vecino más cercano:\n{error}")
            btn.state(["!disabled"])
            return

        # guarda la solución heurística en el estado
        estado["solucion_vecino"] = solucion_vecino

        # actualiza la etiqueta con tiempo y longitud del vecino cercano
        lbl.config(
            text=(
                f"tiempo vecino: {solucion_vecino['tiempo']:.6f} s "
                f"(l={solucion_vecino['longitud']:.3f})"
            )
        )

        # lanza animación del recorrido heurístico en el panel de gráficos
        panel_graficos.animar_vecino(
            nombre_inicio,
            recorrido_vecino,
            on_finish=lambda: btn.state(["!disabled"]),  # reactiva el botón al terminar
        )

        # si existe solución óptima previa, calcula el gap
        if estado["solucion_optima"] is not None:
            mejor = estado["solucion_optima"]["longitud"]  # longitud óptima
            vecino = solucion_vecino["longitud"]           # longitud heurística
            gap = 100.0 * (vecino - mejor) / mejor        # cálculo del gap

            lbl_gap.config(
                text=(
                    f"gap de optimalidad: {gap:.2f}%  "
                    f"(l_vecino={vecino:.3f}, l*={mejor:.3f})"
                )
            )
        else:
            # si no existe óptimo, avisa que debe ejecutarse primero
            lbl_gap.config(
                text="gap de optimalidad: ejecuta primero la búsqueda exhaustiva."
            )

    # crea el panel de controles (botones, combo, etiquetas)
    panel_controles = crear_panel_controles(
        raiz,
        ciudades,
        on_ejecutar_exhaustivo=ejecutar_exhaustivo,
        on_ejecutar_vecino=ejecutar_vecino,
    )
    panel_controles.pack(side=tk.TOP, fill=tk.X)  # lo ubica arriba

    # crea el panel de gráficos (mapa y animaciones)
    panel_graficos = crear_panel_graficos(raiz, instancia)
    panel_graficos.pack(fill=tk.BOTH, expand=True)  # ocupa todo el espacio restante

    # inicia el loop principal de tkinter
    raiz.mainloop()
