"""
pestana_clases.py
Pestaña para registrar clases grupales y asignarles un entrenador.
"""

from tkinter import ttk, messagebox

from interfaz.componentes import (crear_campo, crear_combo, crear_boton, crear_tabla,
                                  llenar_tabla, limpiar_campos, obtener_clave)


class PestanaClases(ttk.Frame):
    def __init__(self, contenedor, app):
        super().__init__(contenedor)
        self.app = app
        self._construir()
        self.actualizar()

    def _construir(self):
        fila_formularios = ttk.Frame(self)
        fila_formularios.pack(fill="x", padx=10, pady=10)

        # Formulario para registrar
        formulario = ttk.LabelFrame(fila_formularios, text="Registrar Clase Grupal")
        formulario.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.ent_codigo = crear_campo(formulario, "Código:", 0, ancho=25)
        self.ent_nombre = crear_campo(formulario, "Nombre:", 1, ancho=25)
        self.ent_horario = crear_campo(formulario, "Horario (ej. Lunes 6:00 p. m.):", 2, ancho=25)
        self.ent_cupo = crear_campo(formulario, "Cupo:", 3, ancho=25)
        crear_boton(formulario, "Guardar Clase", 4, self._accion_guardar)

        # Formulario para asignar entrenador
        asignacion = ttk.LabelFrame(fila_formularios, text="Asignar Entrenador")
        asignacion.pack(side="left", fill="both", expand=True, padx=(5, 0))

        self.combo_clase = crear_combo(asignacion, "Clase:", 0, ancho=28)
        self.combo_entrenador = crear_combo(asignacion, "Entrenador:", 1, ancho=28)
        crear_boton(asignacion, "Asignar Entrenador", 2, self._accion_asignar)

        self.tabla = crear_tabla(self, "Listado de Clases", [
            ("codigo", "Código", 90),
            ("nombre", "Nombre", 180),
            ("horario", "Horario", 180),
            ("entrenador", "Entrenador", 180),
            ("ocupacion", "Inscritos / Cupo", 130),
        ])

    def _accion_guardar(self):
        try:
            cupo = int(self.ent_cupo.get().strip())
        except ValueError:
            messagebox.showerror("Error", "El cupo debe ser un número entero.")
            return

        try:
            self.app.gimnasio.registrar_clase(
                self.ent_codigo.get().strip(),
                self.ent_nombre.get().strip(),
                self.ent_horario.get().strip(),
                cupo,
            )
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        limpiar_campos(self.ent_codigo, self.ent_nombre, self.ent_horario, self.ent_cupo)
        self.app.guardar_y_actualizar()
        messagebox.showinfo("Éxito", "Clase registrada correctamente.")

    def _accion_asignar(self):
        clase_texto = self.combo_clase.get()
        entrenador_texto = self.combo_entrenador.get()
        if not (clase_texto and entrenador_texto):
            messagebox.showerror("Error", "Debe seleccionar clase y entrenador.")
            return

        try:
            self.app.gimnasio.asignar_entrenador(obtener_clave(clase_texto),
                                                 obtener_clave(entrenador_texto))
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        self.app.guardar_y_actualizar()
        messagebox.showinfo("Éxito", "Entrenador asignado correctamente.")

    def actualizar(self):
        gimnasio = self.app.gimnasio

        self.combo_clase["values"] = [str(c) for c in gimnasio.listar_clases()]
        self.combo_entrenador["values"] = [f"{e} ({e.especialidad})"
                                           for e in gimnasio.listar_entrenadores()]
        self.combo_clase.set("")
        self.combo_entrenador.set("")

        filas = [(c.codigo, c.nombre, c.horario, c.nombre_entrenador(),
                  f"{len(gimnasio.clientes_en(c))} / {c.cupo}")
                 for c in gimnasio.listar_clases()]
        llenar_tabla(self.tabla, filas)
