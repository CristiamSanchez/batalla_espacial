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
```

## 🕹️ Controles

| Tecla                | Acción                              |
|-----------------------|--------------------------------------|
| ⬅️ ➡️ ⬆️ ⬇️ (flechas) | Mover la nave                        |
| `ESPACIO`             | Disparar láser                       |
| `ENTER`               | Confirmar / iniciar / reiniciar      |
| `ESC`                 | Salir del juego                      |

### Desde un celular

En GitHub Pages no necesitas abrir un teclado virtual. Toca la pantalla de
inicio para continuar; en la selección de dificultad toca el lado izquierdo o
derecho para cambiar y el centro para confirmar. Durante la partida usa el
D-pad de la esquina inferior izquierda para mover la nave y el botón `TIRO` de
la esquina inferior derecha para disparar. En `GAME OVER`, toca la pantalla
para reiniciar.

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

Sí. La carpeta `web/` contiene la versión adaptada con
[Pygbag](https://github.com/pygame-web/pygbag), que compila el juego a
WebAssembly. La carpeta `docs/` contiene los archivos que se publican en
GitHub Pages.

El archivo `main.py` no se puede abrir directamente desde el navegador del
celular: necesita Python y Pygame instalados. Para jugar en el celular, usa la
versión publicada en GitHub Pages. Para ejecutarlo localmente en Android
necesitarías una aplicación compatible con Python y Pygame, como Pydroid 3,
además de instalar las dependencias del proyecto.

## 🛠️ Posibles mejoras futuras

- Diferentes patrones de ataque del jefe según su vida restante.
- Tabla de puntuaciones más altas (high scores) guardada en archivo local.
- Más tipos de enemigos y power-ups.

## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT. Eres libre de usarlo, modificarlo y compartirlo.
