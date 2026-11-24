"""
pestana_reportes.py
Pestaña que muestra qué clientes están al día con el pago de un mes
y cuánto se recaudó. Solo consulta datos, no modifica nada.
"""

from tkinter import ttk, messagebox

from modelos.pago import mes_actual, validar_mes
from interfaz.componentes import crear_campo, crear_tabla, llenar_tabla, formatear_pesos


class PestanaReportes(ttk.Frame):
    def __init__(self, contenedor, app):
        super().__init__(contenedor)
        self.app = app
        self.mes = mes_actual()  # mes que se está consultando
        self._construir()
        self.actualizar()

    def _construir(self):
        consulta = ttk.LabelFrame(self, text="Estado de pagos del mes")
        consulta.pack(fill="x", padx=10, pady=10)

        self.ent_mes = crear_campo(consulta, "Mes (AAAA-MM):", 0, ancho=15)
        self.ent_mes.insert(0, self.mes)
        ttk.Button(consulta, text="Consultar", command=self._accion_consultar).grid(
            row=0, column=2, padx=10, pady=5)

        self.lbl_resumen = ttk.Label(consulta, text="", font=("Arial", 11, "bold"))
        self.lbl_resumen.grid(row=1, column=0, columnspan=3, padx=5, pady=(0, 10), sticky="w")

        self.tabla = crear_tabla(self, "Clientes", [
            ("cliente", "Cliente", 220),
            ("telefono", "Teléfono", 120),
            ("membresia", "Membresía", 120),
            ("valor", "Mensualidad", 120),
            ("estado", "Estado", 120),
        ], alto=14)

    def _accion_consultar(self):
        mes = self.ent_mes.get().strip()
        try:
            validar_mes(mes)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        self.mes = mes
        self.actualizar()

    def actualizar(self):
        gimnasio = self.app.gimnasio
        clientes = gimnasio.listar_clientes()
        pendientes = gimnasio.clientes_pendientes(self.mes)

        self.lbl_resumen.config(
            text=f"Recaudado en {self.mes}: {formatear_pesos(gimnasio.total_recaudado(self.mes))}"
                 f"   ·   Al día: {len(clientes) - len(pendientes)}"
                 f"   ·   Pendientes: {len(pendientes)}"
        )

        filas = [(c.nombre, c.telefono, c.membresia.tipo(),
                  formatear_pesos(c.membresia.precio_mensual()),
                  gimnasio.estado_pago(c, self.mes))
                 for c in clientes]
        llenar_tabla(self.tabla, filas)
