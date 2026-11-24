"""
pestana_clientes.py
Pestaña para registrar clientes, cambiar su membresía y ver el listado.
"""

from tkinter import ttk, messagebox

from modelos.membresia import TIPOS_MEMBRESIA
from interfaz.componentes import (crear_campo, crear_combo, crear_boton, crear_tabla,
                                  llenar_tabla, limpiar_campos, obtener_clave, formatear_pesos)


class PestanaClientes(ttk.Frame):
    def __init__(self, contenedor, app):
        super().__init__(contenedor)
        self.app = app  # ventana principal: da acceso al gimnasio y a guardar
        self._construir()
        self.actualizar()

    def _construir(self):
        # los dos formularios van lado a lado para dejar espacio a la tabla
        fila_formularios = ttk.Frame(self)
        fila_formularios.pack(fill="x", padx=10, pady=10)

        # Formulario para registrar
        formulario = ttk.LabelFrame(fila_formularios, text="Registrar Cliente")
        formulario.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.ent_id = crear_campo(formulario, "Id:", 0, ancho=25)
        self.ent_nombre = crear_campo(formulario, "Nombre:", 1, ancho=25)
        self.ent_telefono = crear_campo(formulario, "Teléfono:", 2, ancho=25)
        self.combo_membresia = crear_combo(formulario, "Membresía:", 3, ancho=22)
        self.combo_membresia["values"] = self._textos_membresia()
        crear_boton(formulario, "Guardar Cliente", 4, self._accion_guardar)

        # Formulario para cambiar la membresía
        cambio = ttk.LabelFrame(fila_formularios, text="Cambiar Membresía")
        cambio.pack(side="left", fill="both", expand=True, padx=(5, 0))

        self.combo_cliente = crear_combo(cambio, "Cliente:", 0, ancho=28)
        self.combo_nueva = crear_combo(cambio, "Nueva membresía:", 1, ancho=28)
        self.combo_nueva["values"] = self._textos_membresia()
        crear_boton(cambio, "Cambiar Membresía", 2, self._accion_cambiar)

        self.tabla = crear_tabla(self, "Listado de Clientes", [
            ("id", "Id", 100),
            ("nombre", "Nombre", 200),
            ("telefono", "Teléfono", 120),
            ("membresia", "Membresía", 110),
            ("precio", "Mensualidad", 110),
            ("clases", "Clases / Máximo", 120),
        ])

    def _textos_membresia(self):
        # "Estándar - $90.000 - 3 clase(s)"; obtener_clave() devuelve "Estándar"
        textos = []
        for tipo, clase in TIPOS_MEMBRESIA.items():
            membresia = clase()
            textos.append(f"{tipo} - {formatear_pesos(membresia.precio_mensual())} - "
                          f"{membresia.max_clases()} clase(s)")
        return textos

    def _accion_guardar(self):
        try:
            self.app.gimnasio.registrar_cliente(
                self.ent_id.get().strip(),
                self.ent_nombre.get().strip(),
                self.ent_telefono.get().strip(),
                obtener_clave(self.combo_membresia.get()),
            )
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        limpiar_campos(self.ent_id, self.ent_nombre, self.ent_telefono)
        self.combo_membresia.set("")
        self.app.guardar_y_actualizar()
        messagebox.showinfo("Éxito", "Cliente registrado correctamente.")

    def _accion_cambiar(self):
        cliente_texto = self.combo_cliente.get()
        nueva_texto = self.combo_nueva.get()
        if not (cliente_texto and nueva_texto):
            messagebox.showerror("Error", "Debe seleccionar cliente y membresía.")
            return

        try:
            self.app.gimnasio.cambiar_membresia(obtener_clave(cliente_texto),
                                                obtener_clave(nueva_texto))
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        self.combo_nueva.set("")
        self.app.guardar_y_actualizar()
        messagebox.showinfo("Éxito", "Membresía cambiada correctamente.")

    def actualizar(self):
        clientes = self.app.gimnasio.listar_clientes()

        self.combo_cliente["values"] = [str(c) for c in clientes]
        self.combo_cliente.set("")

        filas = []
        for c in clientes:
            filas.append((c.id, c.nombre, c.telefono, c.membresia.tipo(),
                          formatear_pesos(c.membresia.precio_mensual()),
                          f"{c.cantidad_clases()} / {c.membresia.max_clases()}"))
        llenar_tabla(self.tabla, filas)
