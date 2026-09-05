# 🚀 Batalla Espacial 2D

Un juego de disparos espaciales (*shoot 'em up*) hecho en Python con **Pygame**. Controla una nave, destruye oleadas de enemigos, recoge power-ups y enfréntate a un jefe final cada 5 oleadas.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green)
![Licencia](https://img.shields.io/badge/Licencia-MIT-lightgrey)

---

## 🎮 Características

- Nave controlable con disparo de láser.
- Oleadas de enemigos con dificultad creciente.
- **Jefe final** cada 5 oleadas, con barra de vida y patrón de disparo en abanico.
- **Power-ups**: vida extra, escudo temporal y disparo rápido.
- Efectos de sonido sintetizados (no requieren archivos de audio externos).
- Selección de dificultad: Fácil, Normal o Difícil.
- Pantallas de inicio y Game Over con opción de reiniciar.

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
