"""
========================================================
  BATALLA ESPACIAL - Juego 2D con Pygame (Edición Extendida)
========================================================
Un juego de disparos espaciales donde el jugador controla
una nave, dispara láseres, recoge power-ups, se enfrenta a
oleadas de enemigos y a un JEFE FINAL cada cierto número
de oleadas, con dificultad ajustable.

Controles:
    Flechas          -> Mover la nave
    Barra espaciadora -> Disparar láser
    ENTER            -> Confirmar / Iniciar / Reiniciar
    ESC              -> Salir del juego

Requisitos:
    pip install pygame numpy
    (numpy es opcional: solo se usa para generar los sonidos
     sintetizados; si no está instalado, el juego funciona
     igual mas sin efectos de sonido)
========================================================
"""

import pygame
import random
import sys
import asyncio

# Numpy es opcional: se usa únicamente para sintetizar sonidos.
# Si no está disponible, el juego sigue funcionando sin audio.
try:
    import numpy as np
    NUMPY_DISPONIBLE = True
except ImportError:
    NUMPY_DISPONIBLE = False

# ---------------------------------------------------------
# INICIALIZACIÓN GENERAL DE PYGAME
# ---------------------------------------------------------
pygame.init()

SONIDOS_ACTIVOS = False
try:
    pygame.mixer.init()
    SONIDOS_ACTIVOS = NUMPY_DISPONIBLE
except pygame.error:
    # Puede fallar si no hay dispositivo de audio disponible (ej. algunos servidores)
    SONIDOS_ACTIVOS = False

# Dimensiones de la ventana
ANCHO = 700
ALTO = 700
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Batalla Espacial 2D - Edición Extendida")

reloj = pygame.time.Clock()
FPS = 60

# ---------------------------------------------------------
# COLORES (usamos formas geométricas, no assets externos)
# ---------------------------------------------------------
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (150, 150, 150)
VERDE = (0, 255, 100)
ROJO = (255, 60, 60)
AZUL = (60, 160, 255)
AMARILLO = (255, 230, 80)
MORADO = (180, 80, 255)
NARANJA = (255, 150, 40)
CIAN = (80, 230, 230)

# ---------------------------------------------------------
# FUENTES DE TEXTO
# ---------------------------------------------------------
fuente_grande = pygame.font.SysFont("arial", 60, bold=True)
fuente_mediana = pygame.font.SysFont("arial", 36, bold=True)
fuente_pequena = pygame.font.SysFont("arial", 24)
fuente_muy_pequena = pygame.font.SysFont("arial", 18)


# ===========================================================
# GENERACIÓN DE SONIDOS SINTETIZADOS (sin archivos externos)
# ===========================================================
def generar_tono(frecuencia, duracion_ms, volumen=0.3, tipo="seno"):
    """Genera un pygame.Sound sintetizado con una onda simple.
    Esto evita depender de archivos de audio externos."""
    if not SONIDOS_ACTIVOS:
        return None

    frecuencia_muestreo = 44100
    n_muestras = int(frecuencia_muestreo * duracion_ms / 1000)
    t = np.linspace(0, duracion_ms / 1000, n_muestras, False)

    if tipo == "seno":
        onda = np.sin(2 * np.pi * frecuencia * t)
    elif tipo == "ruido":
        onda = np.random.uniform(-1, 1, n_muestras)
    else:
        onda = np.sin(2 * np.pi * frecuencia * t)

    # Aplicamos un pequeño desvanecimiento (fade out) para evitar "clicks"
    desvanecimiento = np.linspace(1, 0, n_muestras)
    onda = onda * desvanecimiento

    amplitud_max = 2 ** 15 - 1
    muestras = (onda * amplitud_max * volumen).astype(np.int16)
    estereo = np.column_stack((muestras, muestras))
    estereo = np.ascontiguousarray(estereo)

    return pygame.sndarray.make_sound(estereo)


# Creamos los efectos de sonido una sola vez al iniciar el juego
if SONIDOS_ACTIVOS:
    try:
        sonido_disparo = generar_tono(880, 90, 0.15, "seno")
        sonido_explosion = generar_tono(120, 220, 0.25, "ruido")
        sonido_powerup = generar_tono(660, 180, 0.2, "seno")
        sonido_dano = generar_tono(200, 200, 0.25, "seno")
        sonido_jefe_disparo = generar_tono(300, 120, 0.2, "seno")
    except Exception:
        SONIDOS_ACTIVOS = False


def reproducir(sonido):
    """Reproduce un efecto de sonido si el audio está disponible."""
    if SONIDOS_ACTIVOS and sonido is not None:
        sonido.play()


# ---------------------------------------------------------
# FONDO ESTRELLADO (simple efecto visual con puntos)
# ---------------------------------------------------------
estrellas = []
for _ in range(80):
    x = random.randint(0, ANCHO)
    y = random.randint(0, ALTO)
    velocidad = random.uniform(1, 3)
    radio = random.choice([1, 1, 2])
    estrellas.append([x, y, velocidad, radio])


def dibujar_fondo():
    """Dibuja el fondo negro con estrellas que se mueven hacia abajo."""
    pantalla.fill(NEGRO)
    for estrella in estrellas:
        estrella[1] += estrella[2]  # mover hacia abajo
        if estrella[1] > ALTO:
            estrella[1] = 0
            estrella[0] = random.randint(0, ANCHO)
        pygame.draw.circle(pantalla, BLANCO, (int(estrella[0]), int(estrella[1])), estrella[3])


# ===========================================================
# CONTROLES TÁCTILES (para jugar desde el celular en el navegador)
# ===========================================================
# Se dibuja un D-pad (arriba/abajo/izquierda/derecha) en la esquina inferior
# izquierda y un botón de disparo circular en la esquina inferior derecha.
# Funcionan tanto con toques reales (FINGERDOWN/FINGERUP) como con el mouse
# (MOUSEBUTTONDOWN/UP), para poder probarlos también desde una computadora.

TAMANO_BOTON_DPAD = 55
CENTRO_DPAD = (100, ALTO - 110)
CENTRO_DISPARO = (ANCHO - 90, ALTO - 100)
RADIO_DISPARO = 48


def crear_controles_tactiles():
    """Crea los rectángulos del D-pad. El botón de disparo es circular
    y se maneja aparte (con CENTRO_DISPARO y RADIO_DISPARO)."""
    cx, cy = CENTRO_DPAD
    t = TAMANO_BOTON_DPAD
    botones = {
        "arriba": pygame.Rect(0, 0, t, t),
        "abajo": pygame.Rect(0, 0, t, t),
        "izquierda": pygame.Rect(0, 0, t, t),
        "derecha": pygame.Rect(0, 0, t, t),
    }
    botones["arriba"].center = (cx, cy - t)
    botones["abajo"].center = (cx, cy + t)
    botones["izquierda"].center = (cx - t, cy)
    botones["derecha"].center = (cx + t, cy)
    return botones


def punto_en_circulo(punto, centro, radio):
    dx = punto[0] - centro[0]
    dy = punto[1] - centro[1]
    return (dx * dx + dy * dy) <= (radio * radio)


def detectar_boton_tactil(posicion, botones):
    """Devuelve el nombre del botón tocado en esa posición, o None."""
    for nombre, rect in botones.items():
        if rect.collidepoint(posicion):
            return nombre
    if punto_en_circulo(posicion, CENTRO_DISPARO, RADIO_DISPARO):
        return "disparo"
    return None


def obtener_posicion_tactil(evento):
    """Devuelve la posición lógica de un toque o clic, si corresponde."""
    if evento.type == pygame.FINGERDOWN:
        return (evento.x * ANCHO, evento.y * ALTO)
    if evento.type == pygame.MOUSEBUTTONDOWN:
        return evento.pos
    return None


def dibujar_controles_tactiles(superficie, botones, activos):
    """Dibuja el D-pad y el botón de disparo semitransparentes sobre la pantalla.
    Los botones presionados se resaltan con más opacidad para dar feedback visual."""
    # --- D-pad ---
    flechas = {
        "arriba": [(0, -14), (-12, 8), (12, 8)],
        "abajo": [(0, 14), (-12, -8), (12, -8)],
        "izquierda": [(-14, 0), (8, -12), (8, 12)],
        "derecha": [(14, 0), (-8, -12), (-8, 12)],
    }
    for nombre, rect in botones.items():
        presionado = nombre in activos
        superficie_boton = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        alfa = 200 if presionado else 90
        color_fondo = AZUL if presionado else GRIS
        pygame.draw.circle(superficie_boton, (*color_fondo, alfa),
                            (rect.width // 2, rect.height // 2), rect.width // 2)
        superficie.blit(superficie_boton, rect.topleft)

        # Flecha indicando la dirección del botón
        cx, cy = rect.center
        puntos = [(cx + dx, cy + dy) for dx, dy in flechas[nombre]]
        pygame.draw.polygon(superficie, BLANCO, puntos)

    # --- Botón de disparo ---
    presionado = "disparo" in activos
    superficie_disparo = pygame.Surface((RADIO_DISPARO * 2, RADIO_DISPARO * 2), pygame.SRCALPHA)
    alfa = 210 if presionado else 100
    color = ROJO if presionado else (200, 80, 80)
    pygame.draw.circle(superficie_disparo, (*color, alfa), (RADIO_DISPARO, RADIO_DISPARO), RADIO_DISPARO)
    superficie.blit(superficie_disparo, (CENTRO_DISPARO[0] - RADIO_DISPARO, CENTRO_DISPARO[1] - RADIO_DISPARO))
    etiqueta = fuente_muy_pequena.render("TIRO", True, BLANCO)
    superficie.blit(etiqueta, etiqueta.get_rect(center=CENTRO_DISPARO))


def procesar_evento_tactil(evento, botones, presiones):
    """Actualiza el diccionario 'presiones' (id de toque/mouse -> nombre de botón)
    según los eventos de dedo (móvil) o de mouse (escritorio/pruebas).
    Se usa un id distinto por cada dedo para soportar multi-touch real
    (por ejemplo, moverse con el D-pad mientras se dispara al mismo tiempo)."""
    if evento.type == pygame.FINGERDOWN:
        # Las coordenadas de FINGERDOWN vienen normalizadas (0.0 a 1.0)
        posicion = (evento.x * ANCHO, evento.y * ALTO)
        boton = detectar_boton_tactil(posicion, botones)
        if boton:
            presiones[evento.finger_id] = boton
    elif evento.type == pygame.FINGERUP:
        presiones.pop(evento.finger_id, None)
    elif evento.type == pygame.MOUSEBUTTONDOWN:
        boton = detectar_boton_tactil(evento.pos, botones)
        if boton:
            presiones["mouse"] = boton
    elif evento.type == pygame.MOUSEBUTTONUP:
        presiones.pop("mouse", None)


# ---------------------------------------------------------
# CONFIGURACIÓN DE DIFICULTAD
# ---------------------------------------------------------
DIFICULTADES = {
    "Fácil":   {"mult_velocidad": 0.7, "mult_cantidad": 0.8, "vidas": 4, "mult_disparo_enemigo": 1.4},
    "Normal":  {"mult_velocidad": 1.0, "mult_cantidad": 1.0, "vidas": 3, "mult_disparo_enemigo": 1.0},
    "Difícil": {"mult_velocidad": 1.4, "mult_cantidad": 1.3, "vidas": 2, "mult_disparo_enemigo": 0.7},
}


# ===========================================================
# CLASE: NAVE DEL JUGADOR
# ===========================================================
class Jugador(pygame.sprite.Sprite):
    def __init__(self, vidas_iniciales):
        super().__init__()
        ancho_nave, alto_nave = 50, 40
        self.image_base = pygame.Surface((ancho_nave, alto_nave), pygame.SRCALPHA)

        # Dibujamos la nave como un triángulo (forma geométrica simple)
        puntos = [
            (ancho_nave // 2, 0),
            (0, alto_nave),
            (ancho_nave, alto_nave)
        ]
        pygame.draw.polygon(self.image_base, VERDE, puntos)
        pygame.draw.circle(self.image_base, AZUL, (ancho_nave // 2, alto_nave - 12), 6)

        self.image = self.image_base.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 20

        self.velocidad = 6
        self.vidas = vidas_iniciales
        self.vidas_maximas = 5

        # Invencibilidad temporal tras recibir daño
        self.invencible = False
        self.tiempo_invencible = 0

        # Power-up: escudo (invencibilidad prolongada, se muestra distinto)
        self.escudo_activo = False
        self.tiempo_escudo = 0

        # Power-up: disparo rápido
        self.disparo_rapido = False
        self.tiempo_disparo_rapido = 0
        self.cooldown_normal = 300
        self.cooldown_rapido = 130

    def update(self, izquierda, derecha, arriba, abajo):
        """Mueve la nave según las entradas activas (teclado O botones táctiles),
        sin salir de la pantalla. Cada parámetro es un booleano ya combinado
        en el bucle principal (True si la tecla o el botón correspondiente
        está presionado)."""
        if izquierda and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if derecha and self.rect.right < ANCHO:
            self.rect.x += self.velocidad
        if arriba and self.rect.top > 0:
            self.rect.y -= self.velocidad
        if abajo and self.rect.bottom < ALTO:
            self.rect.y += self.velocidad

        # Contador de invencibilidad por daño reciente
        if self.invencible:
            self.tiempo_invencible -= 1
            if self.tiempo_invencible <= 0:
                self.invencible = False

        # Contador del power-up de escudo
        if self.escudo_activo:
            self.tiempo_escudo -= 1
            if self.tiempo_escudo <= 0:
                self.escudo_activo = False

        # Contador del power-up de disparo rápido
        if self.disparo_rapido:
            self.tiempo_disparo_rapido -= 1
            if self.tiempo_disparo_rapido <= 0:
                self.disparo_rapido = False

        # Efecto visual: parpadeo si es invencible, tono azulado si tiene escudo
        self.image = self.image_base.copy()
        if self.escudo_activo:
            pygame.draw.circle(self.image, CIAN, (self.rect.width // 2, self.rect.height // 2),
                                self.rect.width // 2 + 4, 3)
        if self.invencible and (self.tiempo_invencible // 5) % 2 == 0:
            self.image.set_alpha(120)
        else:
            self.image.set_alpha(255)

    def es_inmune(self):
        """La nave no recibe daño si está invencible o con escudo activo."""
        return self.invencible or self.escudo_activo

    def recibir_dano(self):
        """Resta una vida y activa la invencibilidad temporal. Devuelve True si murió."""
        if self.es_inmune():
            return False
        self.vidas -= 1
        self.invencible = True
        self.tiempo_invencible = 90  # ~1.5 segundos a 60 FPS
        reproducir(sonido_dano if SONIDOS_ACTIVOS else None)
        return self.vidas <= 0

    def obtener_cooldown_disparo(self):
        return self.cooldown_rapido if self.disparo_rapido else self.cooldown_normal

    def aplicar_powerup(self, tipo):
        """Aplica el efecto correspondiente según el tipo de power-up recogido."""
        if tipo == "vida":
            self.vidas = min(self.vidas + 1, self.vidas_maximas)
        elif tipo == "escudo":
            self.escudo_activo = True
            self.tiempo_escudo = 300  # 5 segundos aprox.
        elif tipo == "rapido":
            self.disparo_rapido = True
            self.tiempo_disparo_rapido = 420  # 7 segundos aprox.


# ===========================================================
# CLASE: LÁSER DEL JUGADOR
# ===========================================================
class LaserJugador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(AMARILLO)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = -10

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.bottom < 0:
            self.kill()


# ===========================================================
# CLASE: LÁSER ENEMIGO
# ===========================================================
class LaserEnemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad_x=0):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad_y = 6
        self.velocidad_x = velocidad_x

    def update(self):
        self.rect.y += self.velocidad_y
        self.rect.x += self.velocidad_x
        if self.rect.top > ALTO:
            self.kill()


# ===========================================================
# CLASE: POWER-UP
# ===========================================================
class PowerUp(pygame.sprite.Sprite):
    """Objeto que cae de un enemigo destruido. Tipos: vida, escudo, rapido."""
    COLORES = {"vida": VERDE, "escudo": CIAN, "rapido": AMARILLO}
    ETIQUETAS = {"vida": "+1", "escudo": "S", "rapido": "R"}

    def __init__(self, x, y, tipo):
        super().__init__()
        self.tipo = tipo
        tamano = 26
        self.image = pygame.Surface((tamano, tamano), pygame.SRCALPHA)
        color = self.COLORES[tipo]
        pygame.draw.rect(self.image, color, (0, 0, tamano, tamano), border_radius=6)
        pygame.draw.rect(self.image, BLANCO, (0, 0, tamano, tamano), width=2, border_radius=6)

        etiqueta = fuente_muy_pequena.render(self.ETIQUETAS[tipo], True, NEGRO)
        self.image.blit(etiqueta, etiqueta.get_rect(center=(tamano // 2, tamano // 2)))

        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = 3

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.top > ALTO:
            self.kill()


# ===========================================================
# CLASE: ENEMIGO NORMAL
# ===========================================================
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad_base, mult_disparo_enemigo):
        super().__init__()
        ancho_enemigo, alto_enemigo = 40, 30
        self.image = pygame.Surface((ancho_enemigo, alto_enemigo), pygame.SRCALPHA)

        puntos = [
            (0, 0),
            (ancho_enemigo, 0),
            (ancho_enemigo // 2, alto_enemigo)
        ]
        pygame.draw.polygon(self.image, MORADO, puntos)
        pygame.draw.circle(self.image, ROJO, (ancho_enemigo // 2, 10), 5)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocidad_x = velocidad_base * random.choice([-1, 1])
        self.velocidad_y = velocidad_base
        self.cooldown_disparo = int(random.randint(60, 200) * mult_disparo_enemigo)
        self.mult_disparo_enemigo = mult_disparo_enemigo

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y * 0.3

        if self.rect.left <= 0 or self.rect.right >= ANCHO:
            self.velocidad_x *= -1

        self.cooldown_disparo -= 1

    def puede_disparar(self):
        if self.cooldown_disparo <= 0:
            self.cooldown_disparo = int(random.randint(90, 220) * self.mult_disparo_enemigo)
            return True
        return False


# ===========================================================
# CLASE: JEFE FINAL (aparece cada cierto número de oleadas)
# ===========================================================
class Jefe(pygame.sprite.Sprite):
    def __init__(self, numero_oleada, dificultad):
        super().__init__()
        ancho_jefe, alto_jefe = 160, 100
        self.image = pygame.Surface((ancho_jefe, alto_jefe), pygame.SRCALPHA)

        # Cuerpo principal del jefe: un gran trapecio con detalles
        puntos_cuerpo = [
            (30, 0), (ancho_jefe - 30, 0),
            (ancho_jefe, alto_jefe - 20), (0, alto_jefe - 20)
        ]
        pygame.draw.polygon(self.image, NARANJA, puntos_cuerpo)
        pygame.draw.polygon(self.image, ROJO, puntos_cuerpo, width=4)
        pygame.draw.circle(self.image, AMARILLO, (ancho_jefe // 2, alto_jefe // 2), 18)
        pygame.draw.circle(self.image, NEGRO, (ancho_jefe // 2, alto_jefe // 2), 8)

        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.top = 40

        # La vida del jefe escala con el número de oleada y la dificultad elegida
        self.vida_maxima = int((80 + numero_oleada * 12) * dificultad["mult_cantidad"])
        self.vida = self.vida_maxima

        self.velocidad_x = 3 * dificultad["mult_velocidad"]
        self.direccion = 1
        self.cooldown_disparo = 60
        self.mult_disparo_enemigo = dificultad["mult_disparo_enemigo"]

        # Fase de entrada: el jefe baja desde arriba antes de empezar a atacar
        self.entrando = True

    def update(self):
        if self.entrando:
            self.rect.y += 2
            if self.rect.top >= 40:
                self.entrando = False
            return

        self.rect.x += int(self.velocidad_x * self.direccion)
        if self.rect.left <= 0 or self.rect.right >= ANCHO:
            self.direccion *= -1

        self.cooldown_disparo -= 1

    def puede_disparar(self):
        if not self.entrando and self.cooldown_disparo <= 0:
            self.cooldown_disparo = int(70 * self.mult_disparo_enemigo)
            return True
        return False

    def disparar(self):
        """El jefe dispara un abanico de 3 láseres."""
        lasers = []
        base_x, base_y = self.rect.centerx, self.rect.bottom
        for velocidad_x in (-3, 0, 3):
            lasers.append(LaserEnemigo(base_x, base_y, velocidad_x))
        return lasers

    def recibir_impacto(self, dano=1):
        """Devuelve True si el jefe fue derrotado."""
        self.vida -= dano
        return self.vida <= 0

    def dibujar_barra_vida(self, superficie):
        ancho_barra = 300
        alto_barra = 18
        x = ANCHO // 2 - ancho_barra // 2
        y = 15
        proporcion = max(self.vida, 0) / self.vida_maxima
        pygame.draw.rect(superficie, GRIS, (x, y, ancho_barra, alto_barra), border_radius=4)
        pygame.draw.rect(superficie, ROJO, (x, y, int(ancho_barra * proporcion), alto_barra), border_radius=4)
        pygame.draw.rect(superficie, BLANCO, (x, y, ancho_barra, alto_barra), width=2, border_radius=4)
        etiqueta = fuente_muy_pequena.render("JEFE", True, BLANCO)
        superficie.blit(etiqueta, (x + ancho_barra // 2 - etiqueta.get_width() // 2, y - 20))


# ===========================================================
# PANTALLA: SELECCIÓN DE DIFICULTAD
# ===========================================================
async def pantalla_seleccion_dificultad():
    """Permite elegir la dificultad con las flechas izquierda/derecha y ENTER."""
    opciones = list(DIFICULTADES.keys())
    indice = 1  # Empieza en "Normal"

    esperando = True
    while esperando:
        dibujar_fondo()

        titulo = fuente_mediana.render("Selecciona la dificultad", True, BLANCO)
        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 220))

        for i, nombre in enumerate(opciones):
            color = AMARILLO if i == indice else GRIS
            texto = fuente_mediana.render(nombre, True, color)
            y = 300 + i * 55
            pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, y))
            if i == indice:
                pygame.draw.polygon(pantalla, AMARILLO, [
                    (ANCHO // 2 - texto.get_width() // 2 - 25, y + 15),
                    (ANCHO // 2 - texto.get_width() // 2 - 10, y + 5),
                    (ANCHO // 2 - texto.get_width() // 2 - 10, y + 25),
                ])

        instrucciones = fuente_pequena.render("← → para elegir, ENTER para confirmar", True, GRIS)
        pantalla.blit(instrucciones, (ANCHO // 2 - instrucciones.get_width() // 2, 520))

        pygame.display.flip()
        await asyncio.sleep(0)  # Cede control al navegador (requerido por Pygbag)
        reloj.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            posicion_tactil = obtener_posicion_tactil(evento)
            if posicion_tactil is not None:
                x, y = posicion_tactil
                if 240 <= y <= 500:
                    if x < ANCHO // 3:
                        indice = (indice - 1) % len(opciones)
                    elif x > ANCHO * 2 // 3:
                        indice = (indice + 1) % len(opciones)
                    else:
                        esperando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    indice = (indice - 1) % len(opciones)
                elif evento.key == pygame.K_RIGHT:
                    indice = (indice + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    esperando = False
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    return DIFICULTADES[opciones[indice]]


# ===========================================================
# FUNCIONES DE PANTALLAS (INICIO Y GAME OVER)
# ===========================================================
async def pantalla_inicio():
    esperando = True
    while esperando:
        dibujar_fondo()

        titulo = fuente_grande.render("BATALLA ESPACIAL", True, VERDE)
        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 130))

        instrucciones = [
            "Flechas: mover la nave",
            "ESPACIO: disparar",
            "Recoge power-ups: vida, escudo y disparo rápido",
            "Cuidado con el JEFE cada 5 oleadas",
            "",
            "Presiona ENTER para continuar"
        ]
        y_texto = 280
        for linea in instrucciones:
            texto = fuente_pequena.render(linea, True, BLANCO)
            pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, y_texto))
            y_texto += 35

        pygame.display.flip()
        await asyncio.sleep(0)  # Cede control al navegador (requerido por Pygbag)
        reloj.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if obtener_posicion_tactil(evento) is not None:
                esperando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    esperando = False
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


async def pantalla_game_over(puntuacion):
    esperando = True
    while esperando:
        dibujar_fondo()

        titulo = fuente_grande.render("GAME OVER", True, ROJO)
        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 200))

        texto_puntuacion = fuente_mediana.render(f"Puntuación final: {puntuacion}", True, BLANCO)
        pantalla.blit(texto_puntuacion, (ANCHO // 2 - texto_puntuacion.get_width() // 2, 300))

        texto_reinicio = fuente_pequena.render("Presiona ENTER para reiniciar o ESC para salir", True, GRIS)
        pantalla.blit(texto_reinicio, (ANCHO // 2 - texto_reinicio.get_width() // 2, 380))

        pygame.display.flip()
        await asyncio.sleep(0)  # Cede control al navegador (requerido por Pygbag)
        reloj.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if obtener_posicion_tactil(evento) is not None:
                esperando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    esperando = False
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


# ===========================================================
# FUNCIÓN PARA CREAR UNA NUEVA OLEADA DE ENEMIGOS NORMALES
# ===========================================================
def crear_oleada(numero_oleada, dificultad):
    grupo_enemigos = pygame.sprite.Group()

    filas = min(2 + numero_oleada // 2, 5)
    columnas = min(5 + numero_oleada // 3, 9)
    velocidad_base = (1 + numero_oleada * 0.3) * dificultad["mult_velocidad"]

    espacio_x = ANCHO // (columnas + 1)
    espacio_y = 50

    for fila in range(filas):
        for columna in range(columnas):
            x = espacio_x * (columna + 1) - 20
            y = 50 + fila * espacio_y
            enemigo = Enemigo(x, y, velocidad_base, dificultad["mult_disparo_enemigo"])
            grupo_enemigos.add(enemigo)

    return grupo_enemigos


# ===========================================================
# FUNCIÓN PRINCIPAL DEL JUEGO (BUCLE DE JUGABILIDAD)
# ===========================================================
async def jugar(dificultad):
    jugador = Jugador(dificultad["vidas"])
    grupo_jugador = pygame.sprite.GroupSingle(jugador)

    lasers_jugador = pygame.sprite.Group()
    lasers_enemigos = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    numero_oleada = 1
    ES_OLEADA_JEFE = 5  # cada 5 oleadas aparece un jefe

    grupo_enemigos = pygame.sprite.Group()
    grupo_jefe = pygame.sprite.GroupSingle()

    def iniciar_oleada(n):
        if n % ES_OLEADA_JEFE == 0:
            grupo_jefe.add(Jefe(n, dificultad))
        else:
            nonlocal grupo_enemigos
            grupo_enemigos = crear_oleada(n, dificultad)

    iniciar_oleada(numero_oleada)

    puntuacion = 0
    tiempo_ultimo_disparo = 0

    # Controles táctiles (para jugar desde el celular en el navegador)
    botones_tactiles = crear_controles_tactiles()
    presiones_tactiles = {}  # id de dedo/mouse -> nombre de botón activo

    jugando = True
    while jugando:
        reloj.tick(FPS)
        tiempo_actual = pygame.time.get_ticks()

        # ------------------ EVENTOS ------------------
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            procesar_evento_tactil(evento, botones_tactiles, presiones_tactiles)

        teclas = pygame.key.get_pressed()
        botones_activos = set(presiones_tactiles.values())

        # Cada entrada combina teclado FÍSICO (si hay) con botones táctiles (si hay)
        mover_izquierda = teclas[pygame.K_LEFT] or "izquierda" in botones_activos
        mover_derecha = teclas[pygame.K_RIGHT] or "derecha" in botones_activos
        mover_arriba = teclas[pygame.K_UP] or "arriba" in botones_activos
        mover_abajo = teclas[pygame.K_DOWN] or "abajo" in botones_activos
        disparar = teclas[pygame.K_SPACE] or "disparo" in botones_activos

        if disparar and tiempo_actual - tiempo_ultimo_disparo > jugador.obtener_cooldown_disparo():
            lasers_jugador.add(LaserJugador(jugador.rect.centerx, jugador.rect.top))
            tiempo_ultimo_disparo = tiempo_actual
            reproducir(sonido_disparo if SONIDOS_ACTIVOS else None)

        # ------------------ ACTUALIZACIÓN ------------------
        grupo_jugador.update(mover_izquierda, mover_derecha, mover_arriba, mover_abajo)
        lasers_jugador.update()
        lasers_enemigos.update()
        powerups.update()
        grupo_enemigos.update()
        grupo_jefe.update()

        for enemigo in grupo_enemigos:
            if enemigo.puede_disparar():
                lasers_enemigos.add(LaserEnemigo(enemigo.rect.centerx, enemigo.rect.bottom))

        jefe = grupo_jefe.sprite
        if jefe is not None and jefe.puede_disparar():
            for laser in jefe.disparar():
                lasers_enemigos.add(laser)
            reproducir(sonido_jefe_disparo if SONIDOS_ACTIVOS else None)

        # Enemigos normales que llegan al fondo de la pantalla
        for enemigo in list(grupo_enemigos):
            if enemigo.rect.bottom >= ALTO:
                enemigo.kill()
                if jugador.recibir_dano():
                    return puntuacion

        # ------------------ COLISIONES ------------------

        # Láser del jugador contra enemigos normales
        colisiones = pygame.sprite.groupcollide(lasers_jugador, grupo_enemigos, True, True)
        for lista_destruidos in colisiones.values():
            for _ in lista_destruidos:
                puntuacion += 10
                reproducir(sonido_explosion if SONIDOS_ACTIVOS else None)
                # Probabilidad de soltar un power-up al morir
                if random.random() < 0.18:
                    tipo = random.choice(["vida", "escudo", "rapido"])
                    ex, ey = _.rect.center
                    powerups.add(PowerUp(ex, ey, tipo))

        # Láser del jugador contra el jefe
        if jefe is not None:
            impactos = pygame.sprite.spritecollide(jefe, lasers_jugador, True)
            for _ in impactos:
                if jefe.recibir_impacto(1):
                    puntuacion += 200  # bonus grande por derrotar al jefe
                    grupo_jefe.empty()
                    reproducir(sonido_explosion if SONIDOS_ACTIVOS else None)
                    # El jefe siempre deja un power-up al ser derrotado
                    powerups.add(PowerUp(jefe.rect.centerx, jefe.rect.centery,
                                          random.choice(["vida", "escudo", "rapido"])))
                    break
                else:
                    reproducir(sonido_disparo if SONIDOS_ACTIVOS else None)

        # Enemigo normal contra la nave (colisión directa)
        colision_directa = pygame.sprite.spritecollide(jugador, grupo_enemigos, False)
        if colision_directa:
            for enemigo in colision_directa:
                enemigo.kill()
            if jugador.recibir_dano():
                return puntuacion

        # Jefe contra la nave (colisión directa, el jefe no muere por esto)
        if jefe is not None and jugador.rect.colliderect(jefe.rect):
            if jugador.recibir_dano():
                return puntuacion

        # Láser enemigo contra la nave
        impactos_laser = pygame.sprite.spritecollide(jugador, lasers_enemigos, True)
        if impactos_laser and not jugador.es_inmune():
            if jugador.recibir_dano():
                return puntuacion

        # Power-ups recogidos por el jugador
        powerups_recogidos = pygame.sprite.spritecollide(jugador, powerups, True)
        for powerup in powerups_recogidos:
            jugador.aplicar_powerup(powerup.tipo)
            reproducir(sonido_powerup if SONIDOS_ACTIVOS else None)

        # Si se eliminó toda la oleada (o al jefe), pasar a la siguiente
        if len(grupo_enemigos) == 0 and jefe is None:
            numero_oleada += 1
            iniciar_oleada(numero_oleada)

        # ------------------ DIBUJADO ------------------
        dibujar_fondo()

        grupo_jugador.draw(pantalla)
        lasers_jugador.draw(pantalla)
        lasers_enemigos.draw(pantalla)
        grupo_enemigos.draw(pantalla)
        powerups.draw(pantalla)
        grupo_jefe.draw(pantalla)

        if jefe is not None:
            jefe.dibujar_barra_vida(pantalla)

        # HUD
        texto_puntuacion = fuente_pequena.render(f"Puntuación: {puntuacion}", True, BLANCO)
        pantalla.blit(texto_puntuacion, (10, 10))

        texto_vidas = fuente_pequena.render(f"Vidas: {jugador.vidas}", True, BLANCO)
        pantalla.blit(texto_vidas, (10, 40))

        texto_oleada = fuente_pequena.render(f"Oleada: {numero_oleada}", True, BLANCO)
        pantalla.blit(texto_oleada, (ANCHO - texto_oleada.get_width() - 10, 10))

        # Indicadores de power-ups activos
        estado_y = 70
        if jugador.escudo_activo:
            texto = fuente_muy_pequena.render("Escudo activo", True, CIAN)
            pantalla.blit(texto, (10, estado_y))
            estado_y += 22
        if jugador.disparo_rapido:
            texto = fuente_muy_pequena.render("Disparo rápido", True, AMARILLO)
            pantalla.blit(texto, (10, estado_y))

        # Controles táctiles (D-pad + botón de disparo) para jugar desde el celular
        dibujar_controles_tactiles(pantalla, botones_tactiles, botones_activos)

        pygame.display.flip()
        await asyncio.sleep(0)  # Cede control al navegador (requerido por Pygbag)


# ===========================================================
# BUCLE PRINCIPAL DEL PROGRAMA
# ===========================================================
async def main():
    while True:
        await pantalla_inicio()
        dificultad = await pantalla_seleccion_dificultad()
        puntuacion_final = await jugar(dificultad)
        await pantalla_game_over(puntuacion_final)


if __name__ == "__main__":
    asyncio.run(main())
