"""
pestana_pagos.py
Pestaña para registrar el pago de la mensualidad de un cliente.
El valor lo pone el sistema según la membresía del cliente.
"""

from tkinter import ttk, messagebox

from modelos.pago import mes_actual
from interfaz.componentes import (crear_campo, crear_combo, crear_boton, crear_tabla,
                                  llenar_tabla, limpiar_campos, obtener_clave, formatear_pesos)


class PestanaPagos(ttk.Frame):
    def __init__(self, contenedor, app):
        super().__init__(contenedor)
        self.app = app
        self._construir()
        self.actualizar()

    def _construir(self):
        formulario = ttk.LabelFrame(self, text="Registrar Pago de Mensualidad")
        formulario.pack(fill="x", padx=10, pady=10)

        self.combo_cliente = crear_combo(formulario, "Cliente:", 0)
        self.ent_mes = crear_campo(formulario, "Mes (AAAA-MM):", 1)
        self.ent_mes.insert(0, mes_actual())
        crear_boton(formulario, "Registrar Pago", 2, self._accion_pagar)

        self.tabla = crear_tabla(self, "Pagos registrados", [
            ("cliente", "Cliente", 220),
            ("membresia", "Membresía", 120),
            ("mes", "Mes", 100),
            ("valor", "Valor", 120),
            ("fecha", "Fecha de pago", 140),
        ])

    def _accion_pagar(self):
        cliente_texto = self.combo_cliente.get()
        if not cliente_texto:
            messagebox.showerror("Error", "Debe seleccionar un cliente.")
            return

        try:
            pago = self.app.gimnasio.registrar_pago(obtener_clave(cliente_texto),
                                                    self.ent_mes.get().strip())
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        limpiar_campos(self.ent_mes)
        self.ent_mes.insert(0, mes_actual())
        self.app.guardar_y_actualizar()
        messagebox.showinfo("Éxito", f"Pago de {formatear_pesos(pago.valor)} registrado "
                                     f"para {pago.cliente.nombre} ({pago.mes}).")

    def actualizar(self):
        gimnasio = self.app.gimnasio

        self.combo_cliente["values"] = [str(c) for c in gimnasio.listar_clientes()]
        self.combo_cliente.set("")

        filas = [(p.cliente.nombre, p.cliente.membresia.tipo(), p.mes,
                  formatear_pesos(p.valor), p.fecha)
                 for p in gimnasio.listar_pagos()]
        llenar_tabla(self.tabla, filas)
