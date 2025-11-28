import tkinter as tk  # librería principal de interfaces gráficas
from tkinter import ttk, StringVar  # widgets estilizados y variable de texto

# Panel ligero de controles para ejecutar los métodos
def crear_panel_controles(
    master,  # contenedor padre donde se ubicará el panel
    ciudades,  # lista de ciudades disponibles para la interfaz
    on_ejecutar_exhaustivo,  # callback para botón de búsqueda exhaustiva
    on_ejecutar_vecino,  # callback para botón de vecino cercano
):
    frame = ttk.Frame(master, padding=8)  # marco contenedor con padding general
    frame.ciudades = ciudades  # guarda referencia a las ciudades en el frame

    controles_izquierda = ttk.Frame(frame)  # sección izquierda del panel (botón exhaustivo)
    controles_izquierda.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

    boton_exhaustivo = ttk.Button(
        controles_izquierda,  # se coloca en la columna izquierda
        text="Ejecutar búsqueda exhaustiva",  # texto visible del botón
        command=on_ejecutar_exhaustivo,  # función que se ejecuta al presionar
    )
    boton_exhaustivo.pack(side=tk.TOP, pady=(0, 4))  # acomoda con separación inferior

    etiqueta_tiempo_exhaustivo = ttk.Label(
        controles_izquierda,  # etiqueta bajo el botón exhaustivo
        text="Tiempo exhaustivo: --",  # valor inicial sin calcular
    )
    etiqueta_tiempo_exhaustivo.pack(side=tk.TOP)  # posiciona la etiqueta

    controles_derecha = ttk.Frame(frame)  # sección derecha del panel (vecino cercano)
    controles_derecha.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 0))

    fila_superior_vecino = ttk.Frame(controles_derecha)  # fila para combo y botón vecino
    fila_superior_vecino.pack(side=tk.TOP, pady=(0, 2))  # margen inferior pequeño

    ttk.Label(fila_superior_vecino, text="Ciudad inicial:").pack(side=tk.LEFT)  # texto del combo

    ciudad_inicial = StringVar(value=ciudades[0]["nombre"])  # variable enlazada al combo con primer valor por defecto

    combo_inicio = ttk.Combobox(
        fila_superior_vecino,
        textvariable=ciudad_inicial,  # conecta combo a la variable
        values=[c["nombre"] for c in ciudades],  # nombres de ciudades disponibles
        state="readonly",  # evita edición manual
        width=24,  # ancho visual del combo
    )
    combo_inicio.pack(side=tk.LEFT, padx=4)

    boton_vecino = ttk.Button(
        fila_superior_vecino,
        text="Ejecutar vecino más cercano",  # botón para el algoritmo heurístico
        command=on_ejecutar_vecino,  # callback asociado
    )
    boton_vecino.pack(side=tk.LEFT)  # lo ubica junto al combo

    etiqueta_tiempo_vecino = ttk.Label(
        controles_derecha,
        text="Tiempo vecino: --",  # tiempo del algoritmo heurístico
    )
    etiqueta_tiempo_vecino.pack(side=tk.TOP, pady=(2, 0))

    etiqueta_gap = ttk.Label(
        controles_derecha,
        text="Gap de optimalidad: --",  # diferencia entre heurística y óptimo
    )
    etiqueta_gap.pack(side=tk.TOP, pady=(2, 0))

    # Guardar referencias en el frame para acceder desde fuera
    frame.boton_exhaustivo = boton_exhaustivo  # botón exhaustivo
    frame.etiqueta_tiempo_exhaustivo = etiqueta_tiempo_exhaustivo  # etiqueta para mostrar tiempo exhaustivo
    frame.ciudad_inicial = ciudad_inicial  # variable de ciudad inicial seleccionada
    frame.combo_inicio = combo_inicio  # combobox de selección inicial
    frame.boton_vecino = boton_vecino  # botón de vecino cercano
    frame.etiqueta_tiempo_vecino = etiqueta_tiempo_vecino  # etiqueta tiempo heurístico
    frame.etiqueta_gap = etiqueta_gap  # etiqueta gap heurístico vs óptimo

    return frame  # retorna el panel completo para insertarlo en la interfaz
