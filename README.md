# Batalla Espacial 2D

Juego de disparos espacial desarrollado con Python y Pygame.

## Formas de jugar

### Desde GitHub Pages

Abre:

https://cristiamsanchez.github.io/batalla_espacial/

La versión web funciona en computadores y navegadores móviles.

### En computador

Requisitos:

- Python 3.9 o superior
- Pygame
- NumPy opcional para los sonidos

Instalación:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python batalla_espacial.py

## 🕹️ Controles

| Tecla                | Acción                              |
|-----------------------|--------------------------------------|
| ⬅️ ➡️ ⬆️ ⬇️ (flechas) | Mover la nave                        |
| `ESPACIO`             | Disparar láser                       |
| `ENTER`               | Confirmar / iniciar / reiniciar      |
| `ESC`                 | Salir del juego                      |

## 📦 Requisitos

- Python 3.9 o superior
- [Pygame](https://www.pygame.org/) 2.x
- [NumPy](https://numpy.org/) *(opcional, solo para los efectos de sonido)*

## 🔧 Instalación

1. Clona este repositorio:

   ```bash
   git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
   cd TU_REPOSITORIO/PyGame
   ```

2. (Recomendado) Crea un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate      # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## 🛠️ Solución al error "externally-managed-environment"

Si al hacer `pip install -r requirements.txt` te aparece:

```
error: externally-managed-environment
× This environment is externally managed
```

Es porque tu sistema (Debian/Ubuntu) protege el Python del sistema operativo para que no lo rompas instalando paquetes globalmente (PEP 668). La solución es usar un **entorno virtual**, que además es buena práctica en cualquier proyecto Python:

```bash
# Parado dentro de la carpeta del proyecto (donde está este README)
python3 -m venv venv
source venv/bin/activate        # en Windows: venv\Scripts\activate

# Ahora sí, dentro del entorno virtual:
pip install -r requirements.txt
python batalla_espacial.py
```

Sabrás que el entorno virtual está activo porque tu terminal mostrará `(venv)` al inicio de la línea. Cuando termines de jugar/trabajar, puedes salir con `deactivate`. La próxima vez solo necesitas repetir `source venv/bin/activate` (no hace falta volver a crear el entorno con `python3 -m venv venv`).

## ▶️ Ejecución

```bash
python batalla_espacial.py
```

Se abrirá una ventana con la pantalla de inicio. Presiona `ENTER` para continuar, elige la dificultad con las flechas `←` `→` y confirma con `ENTER` para empezar a jugar.

> **Nota:** si no tienes `numpy` instalado, el juego funciona igual pero sin efectos de sonido (lo detecta automáticamente, no da error).

## 📁 Estructura del proyecto

```
PyGame/
├── batalla_espacial.py   # Código completo del juego
├── requirements.txt      # Dependencias de Python
└── README.md             # Este archivo
```

## 🌐 ¿Se puede jugar desde el navegador?

Sí. Hay una versión adaptada con [Pygbag](https://github.com/pygame-web/pygbag) (compila el mismo código Python a WebAssembly) en la carpeta hermana `../web/`. Ahí encontrarás un `README.md` con los pasos para compilarla y publicarla en GitHub Pages.

## 🛠️ Posibles mejoras futuras

- Diferentes patrones de ataque del jefe según su vida restante.
- Tabla de puntuaciones más altas (high scores) guardada en archivo local.
- Más tipos de enemigos y power-ups.

## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT. Eres libre de usarlo, modificarlo y compartirlo.
