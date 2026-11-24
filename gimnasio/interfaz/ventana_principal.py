"""
ventana_principal.py
Ventana con todas las pestañas. Es el punto de unión entre la interfaz,
el modelo (Gimnasio) y la base de datos (RepositorioCSV).
"""

from tkinter import ttk

from config import TITULO_VENTANA, TAMANO_VENTANA
from interfaz.pestana_clientes import PestanaClientes
from interfaz.pestana_entrenadores import PestanaEntrenadores
from interfaz.pestana_clases import PestanaClases
from interfaz.pestana_inscripciones import PestanaInscripciones
from interfaz.pestana_pagos import PestanaPagos
from interfaz.pestana_reportes import PestanaReportes


class VentanaPrincipal:
    def __init__(self, master, gimnasio, repositorio):
        self.master = master
        self.gimnasio = gimnasio
        self.repositorio = repositorio

        self.master.title(f"{TITULO_VENTANA} - {gimnasio.nombre}")
        self.master.geometry(TAMANO_VENTANA)

        notebook = ttk.Notebook(master)
        notebook.pack(expand=True, fill="both", padx=8, pady=8)

        # Para agregar una pestaña nueva basta con crear su clase y ponerla aquí
        self.pestanas = []
        for texto, clase_pestana in [
            ("Clientes", PestanaClientes),
            ("Entrenadores", PestanaEntrenadores),
            ("Clases", PestanaClases),
            ("Inscripciones", PestanaInscripciones),
            ("Pagos", PestanaPagos),
            ("Reportes", PestanaReportes),
        ]:
            pestana = clase_pestana(notebook, self)
            notebook.add(pestana, text=texto)
            self.pestanas.append(pestana)

    def guardar_y_actualizar(self):
        # se llama después de cada cambio: guarda en CSV y refresca todas las pestañas
        self.repositorio.guardar(self.gimnasio)
        for pestana in self.pestanas:
            pestana.actualizar()
