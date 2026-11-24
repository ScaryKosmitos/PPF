# Sistema de Gestión de Gimnasio

Proyecto en Python con tres capas:

| Capa | Carpeta | Qué hace |
|------|---------|----------|
| Backend (POO) | `modelos/` | Clases del diagrama y reglas del negocio |
| Base de datos | `basedatos/` | Guarda y carga los objetos en archivos CSV |
| Frontend | `interfaz/` | Ventana Tkinter con pestañas |

## Cómo ejecutarlo

Desde la carpeta `gimnasio`:

```
cd ~/PPF/gimnasio
python main.py
```

Los datos se guardan solos en la carpeta `datos/` después de cada cambio.

## Estructura

```
gimnasio/
├── main.py                  # arranca el programa
├── config.py                # valores que se pueden cambiar (nombre del gimnasio...)
├── modelos/
│   ├── usuario.py           # Usuario (clase padre)
│   ├── cliente.py           # Cliente(Usuario)
│   ├── entrenador.py        # Entrenador(Usuario)
│   ├── membresia.py         # Membresia y sus tipos: Basica, Estandar, Premium
│   ├── clase_grupal.py      # ClaseGrupal
│   ├── pago.py              # Pago y funciones del mes (AAAA-MM)
│   └── gimnasio.py          # Gimnasio: listas y reglas del sistema
├── basedatos/
│   └── repositorio_csv.py   # RepositorioCSV: cargar() y guardar()
├── interfaz/
│   ├── componentes.py       # funciones para crear campos, combos y tablas
│   ├── ventana_principal.py # une todo y tiene guardar_y_actualizar()
│   └── pestana_*.py         # una pestaña por archivo
├── docs/                    # diagrama de clases (.dot, .png, .svg)
└── datos/                   # archivos CSV (se crean solos)
```

## Recorrido de una acción

Ejemplo: inscribir a un cliente en una clase.

1. `PestanaInscripciones` lee los combobox y llama a `gimnasio.inscribir(...)`.
2. `Gimnasio` revisa que la clase tenga cupo y le pide al `Cliente` que se inscriba.
   El cliente revisa cuántas clases le permite su membresía.
   Si algo está mal se lanza `ValueError` y la pestaña muestra el mensaje.
3. La pestaña llama a `app.guardar_y_actualizar()`, que guarda en CSV con
   `RepositorioCSV.guardar()` y refresca todas las pestañas.

## Reglas del sistema

- No se repiten ids de usuario ni códigos de clase.
- Cada membresía tiene un precio y un máximo de clases: Básica $60.000 (1), Estándar $90.000 (3), Premium $120.000 (5).
- Una clase no acepta más inscritos que su cupo.
- No se puede bajar a una membresía que permita menos clases de las que el cliente ya tiene.
- Cada cliente paga una vez por mes; el valor lo pone el sistema según su membresía.
- El reporte muestra quién está al día o pendiente en un mes y cuánto se recaudó.

## Conceptos de POO que se usan

- **Herencia:** `Cliente` y `Entrenador` heredan de `Usuario`; `Basica`, `Estandar` y `Premium` heredan de `Membresia`.
- **Polimorfismo:** `tipo()`, `precio_mensual()` y `max_clases()` dan un resultado distinto según la membresía; `Cliente.inscribir()` funciona igual para las tres.
- **Composición:** el `Gimnasio` contiene sus clases y pagos; cada `Cliente` tiene su propia `Membresia`.
- **Asociación:** `ClaseGrupal.entrenador`, `Cliente.clases_inscritas`, `Pago.cliente`.
- **Encapsulamiento de reglas:** la interfaz nunca modifica las listas directamente; siempre pasa por `Gimnasio`.

## Cómo hacer cambios comunes

- **Nuevo tipo de membresía:** crear la clase en `modelos/membresia.py` y agregarla a `TIPOS_MEMBRESIA`.
  Aparece sola en los combobox.
- **Cambiar precios o cantidad de clases:** editar los métodos de cada membresía en `modelos/membresia.py`.
- **Nueva pestaña:** crear `interfaz/pestana_nueva.py` con una clase que herede de `ttk.Frame`
  y tenga el método `actualizar()`, y agregarla a la lista de `ventana_principal.py`.
- **Nuevo atributo en una clase:** agregarlo en `modelos/`, en `CAMPOS_...` y en `cargar()`/`guardar()`
  de `repositorio_csv.py`, y en el formulario de su pestaña.
- **Actualizar el diagrama:** editar `docs/diagrama_clases.dot` y, desde `docs/`, ejecutar
  `dot -Tpng -Gdpi=200 diagrama_clases.dot -o diagrama_clases.png`.
