import tkinter as tk
from tkinter import ttk, StringVar

# Panel ligero de controles para ejecutar los metodos

def crear_panel_controles(
    master,
    ciudades,
    on_ejecutar_exhaustivo,
    on_ejecutar_vecino,
):
    frame = ttk.Frame(master, padding=8)
    frame.ciudades = ciudades

    controles_izquierda = ttk.Frame(frame)
    controles_izquierda.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

    boton_exhaustivo = ttk.Button(
        controles_izquierda,
        text="Ejecutar búsqueda exhaustiva",
        command=on_ejecutar_exhaustivo,
    )
    boton_exhaustivo.pack(side=tk.TOP, pady=(0, 4))

    etiqueta_tiempo_exhaustivo = ttk.Label(
        controles_izquierda,
        text="Tiempo exhaustivo: --",
    )
    etiqueta_tiempo_exhaustivo.pack(side=tk.TOP)

    controles_derecha = ttk.Frame(frame)
    controles_derecha.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 0))

    fila_superior_vecino = ttk.Frame(controles_derecha)
    fila_superior_vecino.pack(side=tk.TOP, pady=(0, 2))

    ttk.Label(fila_superior_vecino, text="Ciudad inicial:").pack(side=tk.LEFT)

    ciudad_inicial = StringVar(value=ciudades[0]["nombre"])
    combo_inicio = ttk.Combobox(
        fila_superior_vecino,
        textvariable=ciudad_inicial,
        values=[c["nombre"] for c in ciudades],
        state="readonly",
        width=24,
    )
    combo_inicio.pack(side=tk.LEFT, padx=4)

    boton_vecino = ttk.Button(
        fila_superior_vecino,
        text="Ejecutar vecino más cercano",
        command=on_ejecutar_vecino,
    )
    boton_vecino.pack(side=tk.LEFT)

    etiqueta_tiempo_vecino = ttk.Label(
        controles_derecha,
        text="Tiempo vecino: --",
    )
    etiqueta_tiempo_vecino.pack(side=tk.TOP, pady=(2, 0))

    etiqueta_gap = ttk.Label(
        controles_derecha,
        text="Gap de optimalidad: --",
    )
    etiqueta_gap.pack(side=tk.TOP, pady=(2, 0))

    # Guardar referencias para acceso externo
    frame.boton_exhaustivo = boton_exhaustivo
    frame.etiqueta_tiempo_exhaustivo = etiqueta_tiempo_exhaustivo
    frame.ciudad_inicial = ciudad_inicial
    frame.combo_inicio = combo_inicio
    frame.boton_vecino = boton_vecino
    frame.etiqueta_tiempo_vecino = etiqueta_tiempo_vecino
    frame.etiqueta_gap = etiqueta_gap

    return frame
