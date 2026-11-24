"""
repositorio_csv.py
Base de datos del sistema usando archivos CSV (uno por "tabla").

    clientes.csv        id, nombre, telefono, membresia
    entrenadores.csv    id, nombre, telefono, especialidad
    clases.csv          codigo, nombre, horario, cupo, id_entrenador
    inscripciones.csv   id_cliente, codigo_clase
    pagos.csv           id_cliente, mes, valor, fecha

Los objetos se relacionan en memoria, pero en el CSV solo se guarda el id
o el código del objeto relacionado (igual que una llave foránea).
"""

import csv
import os

from modelos.gimnasio import Gimnasio


class RepositorioCSV:
    CAMPOS_CLIENTES = ["id", "nombre", "telefono", "membresia"]
    CAMPOS_ENTRENADORES = ["id", "nombre", "telefono", "especialidad"]
    CAMPOS_CLASES = ["codigo", "nombre", "horario", "cupo", "id_entrenador"]
    CAMPOS_INSCRIPCIONES = ["id_cliente", "codigo_clase"]
    CAMPOS_PAGOS = ["id_cliente", "mes", "valor", "fecha"]

    def __init__(self, carpeta: str):
        self.carpeta = carpeta
        os.makedirs(self.carpeta, exist_ok=True)

    # -----------------------------
    # Lectura y escritura genéricas
    # -----------------------------
    def _ruta(self, nombre_archivo: str) -> str:
        return os.path.join(self.carpeta, nombre_archivo)

    def _leer(self, nombre_archivo: str) -> list[dict]:
        ruta = self._ruta(nombre_archivo)
        if not os.path.exists(ruta):
            return []
        with open(ruta, newline="", encoding="utf-8") as archivo:
            return list(csv.DictReader(archivo))

    def _escribir(self, nombre_archivo: str, campos: list[str], filas: list[dict]):
        with open(self._ruta(nombre_archivo), "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(filas)

    # -----------------------------
    # Cargar: CSV -> objetos
    # -----------------------------
    def cargar(self, nombre_gimnasio: str) -> Gimnasio:
        gimnasio = Gimnasio(nombre_gimnasio)

        # Se usan los mismos métodos del Gimnasio, así los datos cargados
        # pasan por las mismas validaciones que los que se crean en la ventana.
        # El orden importa: primero lo que no depende de nada.
        for fila in self._leer("clientes.csv"):
            gimnasio.registrar_cliente(fila["id"], fila["nombre"], fila["telefono"], fila["membresia"])

        for fila in self._leer("entrenadores.csv"):
            gimnasio.registrar_entrenador(fila["id"], fila["nombre"], fila["telefono"], fila["especialidad"])

        for fila in self._leer("clases.csv"):
            gimnasio.registrar_clase(fila["codigo"], fila["nombre"], fila["horario"], int(fila["cupo"]))
            if fila["id_entrenador"]:
                gimnasio.asignar_entrenador(fila["codigo"], fila["id_entrenador"])

        for fila in self._leer("inscripciones.csv"):
            gimnasio.inscribir(fila["id_cliente"], fila["codigo_clase"])

        for fila in self._leer("pagos.csv"):
            gimnasio.registrar_pago(fila["id_cliente"], fila["mes"], int(fila["valor"]), fila["fecha"])

        return gimnasio

    # -----------------------------
    # Guardar: objetos -> CSV
    # -----------------------------
    def guardar(self, gimnasio: Gimnasio):
        clientes = [{"id": c.id, "nombre": c.nombre, "telefono": c.telefono,
                     "membresia": c.membresia.tipo()}
                    for c in gimnasio.listar_clientes()]
        self._escribir("clientes.csv", self.CAMPOS_CLIENTES, clientes)

        entrenadores = [{"id": e.id, "nombre": e.nombre, "telefono": e.telefono,
                         "especialidad": e.especialidad}
                        for e in gimnasio.listar_entrenadores()]
        self._escribir("entrenadores.csv", self.CAMPOS_ENTRENADORES, entrenadores)

        clases = [{"codigo": c.codigo, "nombre": c.nombre, "horario": c.horario, "cupo": c.cupo,
                   "id_entrenador": c.entrenador.id if c.entrenador else ""}
                  for c in gimnasio.listar_clases()]
        self._escribir("clases.csv", self.CAMPOS_CLASES, clases)

        inscripciones = [{"id_cliente": cliente.id, "codigo_clase": clase.codigo}
                         for cliente, clase in gimnasio.listar_inscripciones()]
        self._escribir("inscripciones.csv", self.CAMPOS_INSCRIPCIONES, inscripciones)

        pagos = [{"id_cliente": p.cliente.id, "mes": p.mes, "valor": p.valor, "fecha": p.fecha}
                 for p in gimnasio.listar_pagos()]
        self._escribir("pagos.csv", self.CAMPOS_PAGOS, pagos)
