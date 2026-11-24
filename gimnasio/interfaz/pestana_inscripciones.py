"""
pestana_inscripciones.py
Pestaña para inscribir clientes en clases grupales o cancelar la inscripción.
"""

from tkinter import ttk, messagebox

from interfaz.componentes import crear_combo, crear_tabla, llenar_tabla, obtener_clave


class PestanaInscripciones(ttk.Frame):
    def __init__(self, contenedor, app):
        super().__init__(contenedor)
        self.app = app
        self._construir()
        self.actualizar()

    def _construir(self):
        formulario = ttk.LabelFrame(self, text="Inscripción a Clases")
        formulario.pack(fill="x", padx=10, pady=10)

        self.combo_cliente = crear_combo(formulario, "Cliente:", 0)
        self.combo_clase = crear_combo(formulario, "Clase:", 1)

        # dos botones en la misma fila
        botones = ttk.Frame(formulario)
        botones.grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(botones, text="Inscribir", command=self._accion_inscribir).pack(side="left", padx=5)
        ttk.Button(botones, text="Cancelar Inscripción", command=self._accion_cancelar).pack(side="left", padx=5)

        self.tabla = crear_tabla(self, "Inscripciones registradas", [
            ("cliente", "Cliente", 200),
            ("membresia", "Membresía", 110),
            ("clase", "Clase", 180),
            ("horario", "Horario", 180),
            ("entrenador", "Entrenador", 180),
        ])

    def _leer_seleccion(self):
        # devuelve (id_cliente, codigo_clase) o None si falta algo
        cliente_texto = self.combo_cliente.get()
        clase_texto = self.combo_clase.get()
        if not (cliente_texto and clase_texto):
            messagebox.showerror("Error", "Debe seleccionar cliente y clase.")
            return None
        return obtener_clave(cliente_texto), obtener_clave(clase_texto)

    def _accion_inscribir(self):
        seleccion = self._leer_seleccion()
        if seleccion is None:
            return

        try:
            self.app.gimnasio.inscribir(seleccion[0], seleccion[1])
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        self.app.guardar_y_actualizar()
        messagebox.showinfo("Éxito", "Inscripción registrada correctamente.")

    def _accion_cancelar(self):
        seleccion = self._leer_seleccion()
        if seleccion is None:
            return

        try:
            self.app.gimnasio.cancelar_inscripcion(seleccion[0], seleccion[1])
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        self.app.guardar_y_actualizar()
        messagebox.showinfo("Éxito", "Inscripción cancelada correctamente.")

    def actualizar(self):
        gimnasio = self.app.gimnasio

        self.combo_cliente["values"] = [str(c) for c in gimnasio.listar_clientes()]
        self.combo_clase["values"] = [f"{c} ({gimnasio.cupos_disponibles(c)} cupos)"
                                      for c in gimnasio.listar_clases()]
        self.combo_cliente.set("")
        self.combo_clase.set("")

        filas = [(cliente.nombre, cliente.membresia.tipo(), clase.nombre, clase.horario,
                  clase.nombre_entrenador())
                 for cliente, clase in gimnasio.listar_inscripciones()]
        llenar_tabla(self.tabla, filas)
