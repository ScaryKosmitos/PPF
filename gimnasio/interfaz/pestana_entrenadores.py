"""
pestana_entrenadores.py
Pestaña para registrar entrenadores y ver el listado.
"""

from tkinter import ttk, messagebox

from interfaz.componentes import crear_campo, crear_boton, crear_tabla, llenar_tabla, limpiar_campos


class PestanaEntrenadores(ttk.Frame):
    def __init__(self, contenedor, app):
        super().__init__(contenedor)
        self.app = app
        self._construir()
        self.actualizar()

    def _construir(self):
        formulario = ttk.LabelFrame(self, text="Registrar Entrenador")
        formulario.pack(fill="x", padx=10, pady=10)

        self.ent_id = crear_campo(formulario, "Id:", 0)
        self.ent_nombre = crear_campo(formulario, "Nombre:", 1)
        self.ent_telefono = crear_campo(formulario, "Teléfono:", 2)
        self.ent_especialidad = crear_campo(formulario, "Especialidad:", 3)
        crear_boton(formulario, "Guardar Entrenador", 4, self._accion_guardar)

        self.tabla = crear_tabla(self, "Listado de Entrenadores", [
            ("id", "Id", 100),
            ("nombre", "Nombre", 200),
            ("telefono", "Teléfono", 120),
            ("especialidad", "Especialidad", 150),
            ("clases", "Clases que dirige", 280),
        ])

    def _accion_guardar(self):
        try:
            self.app.gimnasio.registrar_entrenador(
                self.ent_id.get().strip(),
                self.ent_nombre.get().strip(),
                self.ent_telefono.get().strip(),
                self.ent_especialidad.get().strip(),
            )
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        limpiar_campos(self.ent_id, self.ent_nombre, self.ent_telefono, self.ent_especialidad)
        self.app.guardar_y_actualizar()
        messagebox.showinfo("Éxito", "Entrenador registrado correctamente.")

    def actualizar(self):
        filas = []
        for e in self.app.gimnasio.listar_entrenadores():
            clases = ", ".join(c.nombre for c in e.clases_asignadas)
            filas.append((e.id, e.nombre, e.telefono, e.especialidad, clases))
        llenar_tabla(self.tabla, filas)
