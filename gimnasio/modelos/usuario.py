"""
usuario.py
Clase padre de Cliente y Entrenador. Tiene lo que comparten todas las personas
registradas en el gimnasio.
"""


class Usuario:
    def __init__(self, id_usuario: str, nombre: str, telefono: str):
        self.id = id_usuario
        self.nombre = nombre
        self.telefono = telefono

    def rol(self) -> str:
        # cada clase hija sobrescribe este método (polimorfismo)
        return "Usuario"

    def __str__(self):
        # formato usado en los combobox de la interfaz: "id - nombre"
        return f"{self.id} - {self.nombre}"
