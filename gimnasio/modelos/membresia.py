"""
membresia.py
Cada cliente tiene una membresía. Hay tres tipos y cada uno tiene un precio
mensual y un número máximo de clases grupales diferente.

Para agregar un tipo nuevo de membresía:
    1. Crear una clase que herede de Membresia y sobrescriba sus tres métodos.
    2. Agregarla al diccionario TIPOS_MEMBRESIA al final de este archivo.
"""


class Membresia:
    # Estos tres métodos los define cada tipo de membresía (clases hijas)
    def tipo(self) -> str:
        raise NotImplementedError("Cada membresía debe definir tipo().")

    def precio_mensual(self) -> int:
        raise NotImplementedError("Cada membresía debe definir precio_mensual().")

    def max_clases(self) -> int:
        raise NotImplementedError("Cada membresía debe definir max_clases().")

    def __str__(self):
        return self.tipo()


class Basica(Membresia):
    def tipo(self) -> str:
        return "Básica"

    def precio_mensual(self) -> int:
        return 60000

    def max_clases(self) -> int:
        return 1


class Estandar(Membresia):
    def tipo(self) -> str:
        return "Estándar"

    def precio_mensual(self) -> int:
        return 90000

    def max_clases(self) -> int:
        return 3


class Premium(Membresia):
    def tipo(self) -> str:
        return "Premium"

    def precio_mensual(self) -> int:
        return 120000

    def max_clases(self) -> int:
        return 5


# Relaciona el texto del tipo con su clase. Lo usan la interfaz (para llenar
# el combobox) y la base de datos (para saber qué clase crear al cargar).
TIPOS_MEMBRESIA = {
    "Básica": Basica,
    "Estándar": Estandar,
    "Premium": Premium,
}


def crear_membresia(tipo: str) -> Membresia:
    if tipo not in TIPOS_MEMBRESIA:
        raise ValueError(f"Tipo de membresía no válido: {tipo}")
    clase = TIPOS_MEMBRESIA[tipo]
    return clase()
