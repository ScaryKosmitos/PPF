"""
componentes.py
Funciones de ayuda para construir la interfaz. Así cada pestaña no repite
el mismo código para crear etiquetas, campos y tablas.
"""

import tkinter as tk
from tkinter import ttk


def crear_campo(contenedor, texto: str, fila: int, ancho: int = 30) -> ttk.Entry:
    ttk.Label(contenedor, text=texto).grid(row=fila, column=0, padx=5, pady=5, sticky="e")
    entrada = ttk.Entry(contenedor, width=ancho)
    entrada.grid(row=fila, column=1, padx=5, pady=5, sticky="w")
    return entrada


def crear_combo(contenedor, texto: str, fila: int, ancho: int = 40) -> ttk.Combobox:
    ttk.Label(contenedor, text=texto).grid(row=fila, column=0, padx=5, pady=5, sticky="e")
    combo = ttk.Combobox(contenedor, state="readonly", width=ancho)
    combo.grid(row=fila, column=1, padx=5, pady=5, sticky="w")
    return combo


def crear_boton(contenedor, texto: str, fila: int, comando) -> ttk.Button:
    boton = ttk.Button(contenedor, text=texto, command=comando)
    boton.grid(row=fila, column=0, columnspan=2, pady=10)
    return boton


def crear_tabla(contenedor, titulo: str, columnas: list[tuple], alto: int = 10) -> ttk.Treeview:
    """columnas es una lista de tuplas (clave, encabezado, ancho)."""
    ttk.Label(contenedor, text=titulo, font=("Arial", 11, "bold")).pack(anchor="w", padx=10)

    claves = [columna[0] for columna in columnas]
    tabla = ttk.Treeview(contenedor, columns=claves, show="headings", height=alto)
    for clave, encabezado, ancho in columnas:
        tabla.heading(clave, text=encabezado)
        tabla.column(clave, width=ancho, anchor="w")
    tabla.pack(expand=True, fill="both", padx=10, pady=(0, 10))
    return tabla


def llenar_tabla(tabla: ttk.Treeview, filas: list[tuple]):
    for fila in tabla.get_children():
        tabla.delete(fila)
    for valores in filas:
        tabla.insert("", "end", values=valores)


def limpiar_campos(*entradas):
    for entrada in entradas:
        entrada.delete(0, tk.END)


def obtener_clave(texto_combo: str) -> str:
    # los combobox muestran "id - nombre"; esto devuelve solo el id
    return texto_combo.split(" - ")[0]


def formatear_pesos(valor: int) -> str:
    # 90000 -> "$90.000"
    return "$" + f"{valor:,}".replace(",", ".")
