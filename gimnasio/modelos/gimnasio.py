"""
gimnasio.py
Clase principal del sistema (el "cerebro"). Guarda las listas de usuarios,
clases grupales y pagos, y tiene todas las reglas del negocio.

Esta clase NO sabe nada de Tkinter ni de archivos CSV: solo trabaja con objetos.
Si algo no se puede hacer, lanza un ValueError con el mensaje para el usuario.
"""

from datetime import date

from modelos.cliente import Cliente
from modelos.entrenador import Entrenador
from modelos.membresia import crear_membresia
from modelos.clase_grupal import ClaseGrupal
from modelos.pago import Pago, validar_mes


class Gimnasio:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.usuarios = []   # clientes y entrenadores
        self.clases = []
        self.pagos = []

    # -----------------------------
    # Validaciones
    # -----------------------------
    def _validar_obligatorios(self, *campos):
        for campo in campos:
            if campo == "":
                raise ValueError("Todos los campos son obligatorios.")

    # -----------------------------
    # Búsquedas
    # -----------------------------
    def buscar_usuario(self, id_usuario: str):
        for usuario in self.usuarios:
            if usuario.id == id_usuario:
                return usuario
        return None

    def buscar_cliente(self, id_usuario: str) -> Cliente:
        usuario = self.buscar_usuario(id_usuario)
        if not isinstance(usuario, Cliente):
            raise ValueError("Cliente no encontrado.")
        return usuario

    def buscar_entrenador(self, id_usuario: str) -> Entrenador:
        usuario = self.buscar_usuario(id_usuario)
        if not isinstance(usuario, Entrenador):
            raise ValueError("Entrenador no encontrado.")
        return usuario

    def buscar_clase(self, codigo: str) -> ClaseGrupal:
        for clase in self.clases:
            if clase.codigo == codigo:
                return clase
        raise ValueError("Clase no encontrada.")

    # -----------------------------
    # Listados
    # -----------------------------
    def listar_clientes(self):
        return [u for u in self.usuarios if isinstance(u, Cliente)]

    def listar_entrenadores(self):
        return [u for u in self.usuarios if isinstance(u, Entrenador)]

    def listar_clases(self):
        return self.clases

    def listar_pagos(self):
        return self.pagos

    def listar_inscripciones(self):
        # devuelve parejas (cliente, clase)
        inscripciones = []
        for cliente in self.listar_clientes():
            for clase in cliente.clases_inscritas:
                inscripciones.append((cliente, clase))
        return inscripciones

    def clientes_en(self, clase: ClaseGrupal):
        return [c for c in self.listar_clientes() if c.esta_inscrito(clase)]

    def cupos_disponibles(self, clase: ClaseGrupal) -> int:
        return clase.cupo - len(self.clientes_en(clase))

    # -----------------------------
    # Registros
    # -----------------------------
    def registrar_cliente(self, id_usuario: str, nombre: str, telefono: str,
                          tipo_membresia: str) -> Cliente:
        self._validar_obligatorios(id_usuario, nombre, telefono, tipo_membresia)
        if self.buscar_usuario(id_usuario) is not None:
            raise ValueError(f"Ya existe un usuario con id {id_usuario}.")

        cliente = Cliente(id_usuario, nombre, telefono, crear_membresia(tipo_membresia))
        self.usuarios.append(cliente)
        return cliente

    def registrar_entrenador(self, id_usuario: str, nombre: str, telefono: str,
                             especialidad: str) -> Entrenador:
        self._validar_obligatorios(id_usuario, nombre, telefono, especialidad)
        if self.buscar_usuario(id_usuario) is not None:
            raise ValueError(f"Ya existe un usuario con id {id_usuario}.")

        entrenador = Entrenador(id_usuario, nombre, telefono, especialidad)
        self.usuarios.append(entrenador)
        return entrenador

    def registrar_clase(self, codigo: str, nombre: str, horario: str, cupo: int) -> ClaseGrupal:
        self._validar_obligatorios(codigo, nombre, horario)
        if any(c.codigo == codigo for c in self.clases):
            raise ValueError(f"Ya existe una clase con código {codigo}.")

        clase = ClaseGrupal(codigo, nombre, horario, cupo)
        self.clases.append(clase)
        return clase

    # -----------------------------
    # Operaciones
    # -----------------------------
    def asignar_entrenador(self, codigo_clase: str, id_entrenador: str):
        clase = self.buscar_clase(codigo_clase)
        entrenador = self.buscar_entrenador(id_entrenador)
        if clase.entrenador is entrenador:
            raise ValueError(f"{entrenador.nombre} ya dirige {clase.nombre}.")

        # si la clase tenía otro entrenador, se le quita
        if clase.entrenador is not None:
            clase.entrenador.quitar_clase(clase)
        entrenador.asignar_clase(clase)
        clase.entrenador = entrenador

    def inscribir(self, id_cliente: str, codigo_clase: str):
        cliente = self.buscar_cliente(id_cliente)
        clase = self.buscar_clase(codigo_clase)
        if not cliente.esta_inscrito(clase) and self.cupos_disponibles(clase) <= 0:
            raise ValueError(f"La clase {clase.nombre} ya no tiene cupos.")
        # el cliente revisa lo que permite su membresía
        cliente.inscribir(clase)

    def cancelar_inscripcion(self, id_cliente: str, codigo_clase: str):
        cliente = self.buscar_cliente(id_cliente)
        clase = self.buscar_clase(codigo_clase)
        cliente.cancelar(clase)

    def cambiar_membresia(self, id_cliente: str, tipo_membresia: str):
        cliente = self.buscar_cliente(id_cliente)
        nueva = crear_membresia(tipo_membresia)
        if nueva.tipo() == cliente.membresia.tipo():
            raise ValueError(f"{cliente.nombre} ya tiene la membresía {nueva.tipo()}.")
        cliente.cambiar_membresia(nueva)

    def registrar_pago(self, id_cliente: str, mes: str, valor: int = None, fecha: str = None) -> Pago:
        # valor y fecha solo se pasan al cargar desde el CSV; desde la ventana
        # se usan el precio de la membresía y la fecha de hoy
        cliente = self.buscar_cliente(id_cliente)
        validar_mes(mes)
        if self.pago_del_mes(cliente, mes) is not None:
            raise ValueError(f"{cliente.nombre} ya pagó el mes {mes}.")

        if valor is None:
            valor = cliente.membresia.precio_mensual()
        if fecha is None:
            fecha = date.today().isoformat()

        pago = Pago(cliente, mes, valor, fecha)
        self.pagos.append(pago)
        return pago

    # -----------------------------
    # Reportes
    # -----------------------------
    def pago_del_mes(self, cliente: Cliente, mes: str):
        for pago in self.pagos:
            if pago.cliente is cliente and pago.mes == mes:
                return pago
        return None

    def estado_pago(self, cliente: Cliente, mes: str) -> str:
        if self.pago_del_mes(cliente, mes) is None:
            return "Pendiente"
        return "Al día"

    def clientes_pendientes(self, mes: str):
        return [c for c in self.listar_clientes() if self.pago_del_mes(c, mes) is None]

    def total_recaudado(self, mes: str) -> int:
        return sum(p.valor for p in self.pagos if p.mes == mes)
