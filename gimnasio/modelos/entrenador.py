"""
entrenador.py
Un Entrenador es un Usuario (herencia) que tiene una especialidad y dirige
clases grupales.
"""

from modelos.usuario import Usuario


class Entrenador(Usuario):
    def __init__(self, id_usuario: str, nombre: str, telefono: str, especialidad: str):
        super().__init__(id_usuario, nombre, telefono)
        self.especialidad = especialidad
        self.clases_asignadas = []

    def rol(self) -> str:
        return "Entrenador"

    def asignar_clase(self, clase):
        if clase not in self.clases_asignadas:
            self.clases_asignadas.append(clase)

    def quitar_clase(self, clase):
        if clase in self.clases_asignadas:
            self.clases_asignadas.remove(clase)
