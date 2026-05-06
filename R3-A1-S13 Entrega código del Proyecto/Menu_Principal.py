import os
import sys

import pygame


CURRENT_DIR = os.path.dirname(__file__)
DOCS_DIR = os.path.dirname(CURRENT_DIR)
if DOCS_DIR not in sys.path:
    sys.path.insert(0, DOCS_DIR)

try:
    from .Inicio import SistemaTTS  # noqa: E402
except ImportError:
    from Inicio import SistemaTTS  # noqa: E402
from public_mock_support import FUENTE, FONDO_PRINCIPAL, HOVER, MockCamera, MockMusicManager, draw_button, draw_cursor, init_display, load_image  # noqa: E402


class MenuPrincipal:
    def __init__(self, ID_sesion=1, camara=None):
        self.screen = init_display("Public Mockup - Menu principal")
        self.width, self.height = self.screen.get_size()
        self.camara = camara or MockCamera(self.width, self.height)
        self.gestor_musica = MockMusicManager()
        self.ID_sesion = ID_sesion
        self.voz = SistemaTTS()
        self.fondo = load_image(FONDO_PRINCIPAL, (self.width, self.height), label="Menu")
        self.opciones = [
            {"texto": "Inicio", "estado": "inicio", "voz": "Inicio"},
            {"texto": "Juegos", "estado": "juegos", "voz": "Juegos"},
            {"texto": "Instrucciones", "estado": "instrucciones", "voz": "Instrucciones"},
            {"texto": "Configuracion", "estado": "configuracion", "voz": "Configuracion"},
            {"texto": "Salir", "estado": "salir", "voz": "Salir"},
        ]
        self.control_clic = False

    def ejecutar(self):
        clock = pygame.time.Clock()
        while True:
            cursor_x, cursor_y, click = self.camara.obtener_posicion_y_clic()
            new_click = click and not self.control_clic
            self.control_clic = click
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "salir"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "salir"
            self.screen.blit(self.fondo, (0, 0))
            for index, opcion in enumerate(self.opciones):
                rect = pygame.Rect(self.width // 2 - int(self.width * 0.4) // 2, int(self.height * 0.3 + index * self.height * 0.12), int(self.width * 0.4), int(self.height * 0.08))
                fill = HOVER if rect.collidepoint((cursor_x, cursor_y)) else None
                draw_button(self.screen, rect, opcion["texto"], FUENTE, fill)
                if new_click and rect.collidepoint((cursor_x, cursor_y)):
                    self.voz.decir_texto(opcion["voz"])
                    return opcion["estado"]
            draw_cursor(self.screen, cursor_x, cursor_y)
            pygame.display.flip()
            clock.tick(30)


if __name__ == "__main__":
    MenuPrincipal().ejecutar()