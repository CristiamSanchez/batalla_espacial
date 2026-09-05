# 🌐 Batalla Espacial 2D — Versión Web (Pygbag)

Esta carpeta contiene la **misma versión del juego**, adaptada para compilarse a WebAssembly con [Pygbag](https://github.com/pygame-web/pygbag) y jugarse directamente desde el navegador (por ejemplo, alojado en **GitHub Pages**). Funciona igual en escritorio (`python main.py`) que en el navegador.

## 📱 Controles táctiles (para celular)

Además del teclado, esta versión dibuja controles en pantalla para jugar desde el celular:

- **D-pad** (abajo a la izquierda): mover la nave en las 4 direcciones.
- **Botón TIRO** (círculo rojo, abajo a la derecha): disparar.

Soportan **multi-touch real** (puedes mantener presionado el D-pad y el botón de disparo al mismo tiempo con dos dedos). También funcionan con el mouse, así puedes probarlos en tu computadora sin necesidad de un celular a la mano.

## 📦 Requisitos para compilar a web

```bash
pip install pygbag
```

## 🔧 Cómo probar el proyecto en la web (paso a paso)

Ajusta `~/Documents/VSCodeProjects/PyGame` por la ruta real de tu proyecto si es distinta.

```bash
# 1. Ve a la carpeta raíz de tu proyecto (donde vas a tener las carpetas PyGame/ y web/)
cd ~/Documents/VSCodeProjects/PyGame

# 2. Crea y activa un entorno virtual (evita el error "externally-managed-environment")
python3 -m venv venv
source venv/bin/activate        # en Windows: venv\Scripts\activate

# 3. Instala pygbag dentro del entorno virtual
pip install pygbag

# 4. Asegúrate de que exista la carpeta "web" con el main.py adentro
#    (descarga el main.py que te compartí y colócalo en una carpeta llamada "web"
#    dentro de tu proyecto, si todavía no la tienes)
mkdir -p web
# copia aquí manualmente el main.py descargado, o usa mv/cp si ya lo tienes en otro lado

# 5. Entra a esa carpeta y compila/ejecuta
cd web
pygbag main.py
```

Esto hace dos cosas:
1. Genera una carpeta `build/web/` con todo lo necesario (HTML, JS, el propio Python empaquetado en WASM).
2. Levanta un servidor local — la terminal te mostrará una dirección como `http://localhost:8000`. Ábrela en tu navegador (Chrome/Firefox) para probar el juego ahí mismo, incluyendo los controles táctiles si simulas un dispositivo móvil desde las herramientas de desarrollador del navegador (F12 → ícono de celular).

> La primera compilación puede tardar unos minutos porque descarga el runtime de Python para WASM. Para volver a probar más adelante, solo necesitas repetir `source venv/bin/activate` y `pygbag main.py` desde la carpeta `web/` — no hace falta recrear el entorno virtual cada vez.

## 🚀 Publicar en GitHub Pages (para jugarlo desde el link, sin instalar nada)

1. Compila el proyecto con `pygbag main.py` (o `pygbag --build main.py` para solo generar los archivos sin levantar servidor).
2. Copia el contenido de `build/web/` a la raíz de una rama `gh-pages` de tu repositorio (o a una carpeta `docs/` en `main`, si prefieres esa opción de GitHub Pages).
3. En GitHub: **Settings → Pages** → selecciona la rama (`gh-pages`) o carpeta (`/docs`) que contiene el `index.html` generado.
4. En unos minutos tu juego estará disponible en `https://TU_USUARIO.github.io/TU_REPOSITORIO/`, jugable desde cualquier navegador de escritorio o celular, sin que nadie tenga que instalar Python ni Pygame.

## ⚠️ Cosas a tener en cuenta

- **Sonido**: los efectos se generan con `numpy`. Numpy sí puede usarse en Pygbag, pero pesa bastante y hace más lenta la carga inicial en el navegador. Si notas que tarda mucho en cargar, una opción es quitar el `import numpy` para la versión web (el juego ya está preparado para funcionar sin sonido sin romperse).
- **Rendimiento**: los navegadores son más lentos que ejecutar Python nativo. Si notas lag en celulares de gama baja, se puede reducir el número de estrellas de fondo o la cantidad de enemigos por oleada.
- Esto no lo pude probar yo mismo de principio a fin (mi entorno de trabajo no tiene acceso a internet para instalar Pygbag ni un navegador para renderizarlo), así que compílalo y pruébalo en tu máquina antes de publicarlo, por si aparece algún detalle específico de tu sistema operativo o navegador.

## 📁 Estructura de esta carpeta

```
web/
└── main.py   # Versión async/await del juego, con controles táctiles, compatible con Pygbag y con "python main.py" normal
```
