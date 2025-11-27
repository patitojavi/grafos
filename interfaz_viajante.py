import tkinter as tk
from tkinter import messagebox

from datos_viajante import coordenadas_ciudades
from buscador_exhaustivo import resolver_exhaustivo_con_traza, MAX_CIUDADES_EXHAUSTIVO
from vecino_cercano import resolver_vecino_con_traza
from interfaz_controles import crear_panel_controles
from interfaz_graficos import crear_panel_graficos

# Ventana principal y manejo de interaccion

def iniciar_interfaz(instancia):
    raiz = tk.Tk()
    raiz.title("Problema del Viajante - Exhaustivo vs Vecino Cercano")
    raiz.geometry("1500x750")

    ciudades = instancia["ciudades"]

    # Estado compartido entre botones y graficos
    estado = {
        "solucion_optima": None,
        "solucion_vecino": None,
        "traza_exhaustiva": None,
        "longitudes_exhaustivas": None,
    }

    def ejecutar_exhaustivo():
        # Controla la corrida de fuerza bruta
        total = len(ciudades)
        if total > MAX_CIUDADES_EXHAUSTIVO:
            messagebox.showinfo(
                "Búsqueda exhaustiva",
                f"{total} ciudades.\n"
                f"El límite para fuerza bruta es {MAX_CIUDADES_EXHAUSTIVO}.\n"
                "Reduce la cantidad de ciudades para ejecutar este método.",
            )
            return

        btn = panel_controles.boton_exhaustivo
        lbl = panel_controles.etiqueta_tiempo_exhaustivo

        btn.state(["disabled"])
        lbl.config(text="Tiempo exhaustivo: calculando...")

        try:
            solucion, traza, longitudes = resolver_exhaustivo_con_traza(instancia)
        except Exception as error:
            messagebox.showerror("Error", f"Fallo en búsqueda exhaustiva:\n{error}")
            btn.state(["!disabled"])
            return

        estado["solucion_optima"] = solucion
        estado["traza_exhaustiva"] = traza
        estado["longitudes_exhaustivas"] = longitudes

        lbl.config(
            text=(
                f"Tiempo exhaustivo: {solucion['tiempo']:.4f} s "
                f"(L*={solucion['longitud']:.3f})"
            )
        )

        panel_graficos.animar_exhaustivo(
            traza,
            longitudes,
            on_finish=lambda: btn.state(["!disabled"]),
        )

    def ejecutar_vecino():
        # Corre vecino cercano y actualiza paneles
        btn = panel_controles.boton_vecino
        lbl = panel_controles.etiqueta_tiempo_vecino
        lbl_gap = panel_controles.etiqueta_gap

        btn.state(["disabled"])
        lbl.config(text="Tiempo vecino: calculando...")

        nombre_inicio = panel_controles.ciudad_inicial.get()
        indice_inicio = next(
            i
            for i, ciudad in enumerate(ciudades)
            if ciudad["nombre"] == nombre_inicio
        )

        try:
            solucion_vecino, recorrido_vecino = resolver_vecino_con_traza(
                instancia, indice_inicio
            )
        except Exception as error:
            messagebox.showerror("Error", f"Fallo en vecino más cercano:\n{error}")
            btn.state(["!disabled"])
            return

        estado["solucion_vecino"] = solucion_vecino

        lbl.config(
            text=(
                f"Tiempo vecino: {solucion_vecino['tiempo']:.6f} s "
                f"(L={solucion_vecino['longitud']:.3f})"
            )
        )

        panel_graficos.animar_vecino(
            nombre_inicio,
            recorrido_vecino,
            on_finish=lambda: btn.state(["!disabled"]),
        )

        if estado["solucion_optima"] is not None:
            mejor = estado["solucion_optima"]["longitud"]
            vecino = solucion_vecino["longitud"]
            gap = 100.0 * (vecino - mejor) / mejor
            lbl_gap.config(
                text=(
                    f"Gap de optimalidad: {gap:.2f}%  "
                    f"(L_vecino={vecino:.3f}, L*={mejor:.3f})"
                )
            )
        else:
            lbl_gap.config(
                text="Gap de optimalidad: ejecuta primero la búsqueda exhaustiva."
            )

    panel_controles = crear_panel_controles(
        raiz,
        ciudades,
        on_ejecutar_exhaustivo=ejecutar_exhaustivo,
        on_ejecutar_vecino=ejecutar_vecino,
    )
    panel_controles.pack(side=tk.TOP, fill=tk.X)

    panel_graficos = crear_panel_graficos(raiz, instancia)
    panel_graficos.pack(fill=tk.BOTH, expand=True)

    raiz.mainloop()
