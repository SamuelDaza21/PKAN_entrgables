import os
import sys
from dataclasses import dataclass

import pygame


DOCS_DIR = os.path.dirname(__file__)
REPO_ROOT = os.path.dirname(DOCS_DIR)
SRC_DIR = os.path.join(REPO_ROOT, "src")
ASSETS_DIR = os.path.join(SRC_DIR, "assets")
IMAGES = os.path.join(ASSETS_DIR, "imagenes")
FONTS = os.path.join(ASSETS_DIR, "fuentes")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
TEXTO = BLANCO
COLOR_FONDO = (135, 206, 235)
COLOR_FONDO_B = (204, 130, 76)
COLOR_BORDE = (221, 162, 105)
FONDO_BOTON = COLOR_FONDO_B
BORDE_BOTON = COLOR_BORDE
AZUL = (100, 149, 237)
BARRA = (100, 200, 100)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
HOVER = COLOR_BORDE
COLOR_TEXTO = NEGRO
COLOR_INPUT = (80, 50, 30)
SAVE_BG = FONDO_BOTON
SAVE_BORDER = BORDE_BOTON
FONDO_PRINCIPAL = os.path.join(IMAGES, "General", "fondo.png")
FONT_PATH = os.path.join(FONTS, "Karina.ttf")
ACTION_MESSAGE = "Action triggered"


def init_display(title):
    pygame.init()
    pygame.font.init()
    screen = pygame.display.get_surface()
    if screen is None:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption(title)
    return screen


def get_font(size=30):
    try:
        return pygame.font.Font(FONT_PATH, size)
    except Exception:
        return pygame.font.Font(None, size)


FUENTE = get_font(30)
FUENTE_PEQUENA = get_font(20)
FUENTE_MUY_PEQUENA = get_font(16)


def log_action(label):
    print(f"{ACTION_MESSAGE}: {label}")


def resolve_image_path(asset_path):
    normalized = asset_path.replace("\\", "/").lstrip("/")
    if os.path.isabs(asset_path):
        return asset_path
    if normalized.lower().startswith("assets/"):
        normalized = normalized.split("/", 1)[1]
    if normalized.lower().startswith("imagenes/"):
        normalized = normalized.split("/", 1)[1]
    return os.path.join(IMAGES, *normalized.split("/"))


def load_image(asset_path, size=None, fill_color=COLOR_FONDO_B, label=None):
    try:
        surface = pygame.image.load(resolve_image_path(asset_path)).convert_alpha()
        if size:
            surface = pygame.transform.scale(surface, size)
        return surface
    except Exception:
        width, height = size or (120, 120)
        placeholder = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(placeholder, fill_color, (0, 0, width, height), border_radius=18)
        pygame.draw.rect(placeholder, NEGRO, (0, 0, width, height), 2, border_radius=18)
        if label:
            text = get_font(max(14, min(28, width // 6))).render(label, True, NEGRO)
            text_rect = text.get_rect(center=(width // 2, height // 2))
            placeholder.blit(text, text_rect)
        return placeholder


def load_background(screen):
    width, height = screen.get_size()
    return load_image(FONDO_PRINCIPAL, (width, height), fill_color=COLOR_FONDO)


def draw_button(surface, rect, text, font=None, fill=None, border=None, text_color=NEGRO, border_radius=15):
    font = font or FUENTE
    fill = fill or FONDO_BOTON
    border = border or BORDE_BOTON
    pygame.draw.rect(surface, fill, rect, border_radius=border_radius)
    pygame.draw.rect(surface, border, rect, 3, border_radius=border_radius)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)
    return rect


def draw_outlined_text(surface, text, font, text_color, outline_color, center):
    base = font.render(text, True, text_color)
    x = center[0] - base.get_width() // 2
    y = center[1]
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        outline = font.render(text, True, outline_color)
        surface.blit(outline, (x + dx, y + dy))
    surface.blit(base, (x, y))


def draw_cursor(surface, x, y):
    pygame.draw.circle(surface, ROJO, (int(x), int(y)), 10, 2)
    pygame.draw.line(surface, ROJO, (int(x) - 14, int(y)), (int(x) + 14, int(y)), 2)
    pygame.draw.line(surface, ROJO, (int(x), int(y) - 14), (int(x), int(y) + 14), 2)
    return x, y


def draw_slider(surface, rect, value):
    pygame.draw.rect(surface, (200, 200, 200), rect, border_radius=5)
    fill_rect = pygame.Rect(rect.x, rect.y, int(rect.width * value), rect.height)
    pygame.draw.rect(surface, BARRA, fill_rect, border_radius=5)
    pygame.draw.rect(surface, COLOR_BORDE, rect, 2, border_radius=5)
    text = FUENTE.render(f"{int(value * 100)}%", True, NEGRO)
    surface.blit(text, text.get_rect(center=rect.center))


@dataclass
class MockProfile:
    id_usuario: int
    nickname: str
    fecha_nacimiento: str


class MockCamera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.calibrado = True
        self.pausado = False
        self.cursor_x = width // 2
        self.cursor_y = height // 2
        self.inactividad = 0
        self.ear_suavizado = 0.321
        self.sensibilidadO = 1.0

    def obtener_posicion_y_clic(self):
        x, y = pygame.mouse.get_pos()
        self.cursor_x, self.cursor_y = x, y
        return x, y, bool(pygame.mouse.get_pressed()[0])

    def calibrar(self):
        log_action("camera.calibrate")
        self.calibrado = True

    def reanudar_cursor(self):
        self.pausado = False

    def pausar_cursor(self):
        self.pausado = True

    def cambiar_modo(self):
        log_action("camera.toggle_mode")


class MockMusicManager:
    def __init__(self):
        self.volumen_musica = 0.65
        self.volumen_efectos = 0.8
        self.cancion_actual = "Mock Theme"
        self.canciones = {
            "Mock Theme": "mock_theme.mp3",
            "Soft Loop": "soft_loop.mp3",
            "Bright Intro": "bright_intro.mp3",
        }

    def iniciar_musica(self):
        log_action(f"music.play:{self.cancion_actual}")

    def cambiar_cancion(self, nombre):
        self.cancion_actual = nombre
        log_action(f"music.change:{nombre}")

    def reproducir_sonido(self, nombre):
        log_action(f"sound:{nombre}")

    def establecer_volumen_musica(self, valor):
        self.volumen_musica = max(0.0, min(1.0, valor))

    def establecer_volumen_efectos(self, valor):
        self.volumen_efectos = max(0.0, min(1.0, valor))


class MockVoice:
    def decir_texto(self, texto):
        log_action(f"voice:{texto}")


class MockBottomBar:
    def __init__(self, width, height, items):
        self.width = width
        self.height = height
        self.items = items
        self.visible = True
        self.altura = int(height * 0.18)
        self.rect = pygame.Rect(int(width * 0.1), height - self.altura - 20, int(width * 0.8), self.altura)
        self.buttons = []
        segment = self.rect.width // len(items)
        for index, item in enumerate(items):
            rect = pygame.Rect(self.rect.x + index * segment, self.rect.y, segment, self.rect.height)
            self.buttons.append({"rect": rect, **item, "scale": 1.0, "alpha": 0})

    def actualizar_visibilidad(self, pos):
        self.visible = pos[1] > self.height - self.altura

    def dibujar(self, surface, pos):
        if not self.visible:
            return
        bar = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(bar, (221, 162, 105, 220), (0, 0, self.rect.width, self.rect.height), border_radius=25)
        pygame.draw.rect(bar, (204, 130, 76, 220), (0, 0, self.rect.width, self.rect.height), 3, border_radius=25)
        surface.blit(bar, self.rect.topleft)
        for button in self.buttons:
            hover = button["rect"].collidepoint(pos)
            target_scale = 1.2 if hover else 1.0
            target_alpha = 255 if hover else 0
            button["scale"] += (target_scale - button["scale"]) * 0.18
            button["alpha"] += (target_alpha - button["alpha"]) * 0.25
            icon = button["icon"]
            icon_w = max(1, int(icon.get_width() * button["scale"]))
            icon_h = max(1, int(icon.get_height() * button["scale"]))
            icon_surface = pygame.transform.smoothscale(icon, (icon_w, icon_h))
            icon_rect = icon_surface.get_rect(center=(button["rect"].centerx, button["rect"].centery - (18 if hover else 0)))
            surface.blit(icon_surface, icon_rect)
            if button["alpha"] > 1:
                text = FUENTE_MUY_PEQUENA.render(button["label"], True, (50, 50, 50))
                text.set_alpha(int(button["alpha"]))
                text_rect = text.get_rect(center=(button["rect"].centerx, button["rect"].centery + 48))
                surface.blit(text, text_rect)

    def manejar_clic(self, pos, click):
        if not (self.visible and click):
            return None
        for button in self.buttons:
            if button["rect"].collidepoint(pos):
                log_action(button["action"])
                return button["action"]
        return None


def build_bottom_bar(width, height):
    size = int(min(width, height) * 0.1)
    items = [
        {"label": "Instrucciones", "icon": load_image("menu/instrucciones.png", (size, size), label="I"), "action": "instrucciones"},
        {"label": "Configuración", "icon": load_image("menu/configuraciones.png", (size, size), label="C"), "action": "configuracion"},
        {"label": "Salir", "icon": load_image("menu/salida.png", (size, size), label="S"), "action": "salir"},
        {"label": "Información", "icon": load_image("menu/informacion.png", (size, size), label="?"), "action": "informacion"},
        {"label": "Jugar", "icon": load_image("menu/juegos.png", (size, size), label="J"), "action": "jugar"},
        {"label": "Inicio", "icon": load_image("menu/inicio.png", (size, size), label="H"), "action": "inicio"},
    ]
    return MockBottomBar(width, height, items)