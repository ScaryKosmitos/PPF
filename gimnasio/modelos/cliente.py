"""
cliente.py
Un Cliente es un Usuario (herencia) que además tiene una membresía y una
lista de clases grupales en las que está inscrito.
"""

from modelos.usuario import Usuario
from modelos.membresia import Membresia


class Cliente(Usuario):
    def __init__(self, id_usuario: str, nombre: str, telefono: str, membresia: Membresia):
        super().__init__(id_usuario, nombre, telefono)
        self.membresia = membresia
        self.clases_inscritas = []

    def rol(self) -> str:
        return "Cliente"

    def cantidad_clases(self) -> int:
        return len(self.clases_inscritas)

    def esta_inscrito(self, clase) -> bool:
        return clase in self.clases_inscritas

    def inscribir(self, clase):
        if self.esta_inscrito(clase):
            raise ValueError(f"{self.nombre} ya está inscrito en {clase.nombre}.")
        # la membresía decide cuántas clases puede tomar (polimorfismo)
        if self.cantidad_clases() >= self.membresia.max_clases():
            raise ValueError(
                f"La membresía {self.membresia.tipo()} de {self.nombre} permite "
                f"máximo {self.membresia.max_clases()} clase(s)."
            )
        self.clases_inscritas.append(clase)

    def cancelar(self, clase):
        if not self.esta_inscrito(clase):
            raise ValueError(f"{self.nombre} no está inscrito en {clase.nombre}.")
        self.clases_inscritas.remove(clase)

    def cambiar_membresia(self, nueva: Membresia):
        if self.cantidad_clases() > nueva.max_clases():
            raise ValueError(
                f"{self.nombre} tiene {self.cantidad_clases()} clases y la membresía "
                f"{nueva.tipo()} permite máximo {nueva.max_clases()}. "
                "Primero debe cancelar algunas."
            )
        self.membresia = nueva
