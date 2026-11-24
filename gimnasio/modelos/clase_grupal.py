"""
clase_grupal.py
Una ClaseGrupal (por ejemplo "Spinning", lunes 6:00 p. m.) tiene un cupo
máximo de clientes y un entrenador que la dirige.
"""


class ClaseGrupal:
    def __init__(self, codigo: str, nombre: str, horario: str, cupo: int):
        if cupo <= 0:
            raise ValueError("El cupo debe ser mayor que 0.")
        self.codigo = codigo
        self.nombre = nombre
        self.horario = horario
        self.cupo = cupo
        self.entrenador = None  # se asigna después con Gimnasio.asignar_entrenador()

    def nombre_entrenador(self) -> str:
        if self.entrenador is None:
            return "Sin asignar"
        return self.entrenador.nombre

    def __str__(self):
        # formato usado en los combobox de la interfaz: "codigo - nombre"
        return f"{self.codigo} - {self.nombre}"
