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
from public_mock_support import BLANCO, BARRA, COLOR_BORDE, COLOR_FONDO_B, FUENTE, MockCamera, MockMusicManager, NEGRO, draw_button, draw_cursor, draw_slider, init_display, load_image, log_action  # noqa: E402


class Configuracion:
    def __init__(self, camara_existente=None, gestor_musica=None, ID_Sesion=1):
        self.screen = init_display("Public Mockup - Configuración")
        self.width, self.height = self.screen.get_size()
        self.camara = camara_existente or MockCamera(self.width, self.height)
        self.gestor_musica = gestor_musica or MockMusicManager()
        self.ID_Sesion = ID_Sesion
        self.voz = SistemaTTS()
        self.fondo = load_image("General/Configuracion.png", (self.width, self.height), label="Configuración")

    def dibujar_boton(self, rect, texto, color_fondo=COLOR_FONDO_B, color_borde=COLOR_BORDE):
        return draw_button(self.screen, rect, texto, FUENTE, color_fondo, color_borde)

    def barra_volumen(self, rect, valor, cursor_x, cursor_y, clic):
        if rect.collidepoint((cursor_x, cursor_y)) and clic:
            valor = max(0.0, min(1.0, (cursor_x - rect.x) / rect.width))
        draw_slider(self.screen, rect, valor)
        return valor

    def ejecutar_configuracion(self):
        clock = pygame.time.Clock()
        boton_volver = pygame.Rect(self.width // 2 - 150, 660, 300, 50)
        barra_musica = pygame.Rect(self.width // 2 - 150, 250, 300, 30)
        barra_efectos = pygame.Rect(self.width // 2 - 150, 320, 300, 30)
        boton_menu = pygame.Rect(self.width // 2 - 150, 390, 300, 50)
        control_clic = False
        menu_abierto = False
        while True:
            cursor_x, cursor_y, click = self.camara.obtener_posicion_y_clic()
            new_click = click and not control_clic
            control_clic = click
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "menu_principal"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "menu_principal"
            self.screen.blit(self.fondo, (0, 0))
            self.dibujar_boton(boton_volver, "Volver")
            self.screen.blit(FUENTE.render("VOLUMEN MÚSICA", True, NEGRO), (self.width // 2 - 120, 220))
            self.screen.blit(FUENTE.render("VOLUMEN EFECTOS", True, NEGRO), (self.width // 2 - 125, 290))
            self.gestor_musica.volumen_musica = self.barra_volumen(barra_musica, self.gestor_musica.volumen_musica, cursor_x, cursor_y, click)
            self.gestor_musica.volumen_efectos = self.barra_volumen(barra_efectos, self.gestor_musica.volumen_efectos, cursor_x, cursor_y, click)
            texto_musica = f"Música: {self.gestor_musica.cancion_actual}"
            self.dibujar_boton(boton_menu, texto_musica)
            if new_click and boton_volver.collidepoint((cursor_x, cursor_y)):
                self.voz.decir_texto("Volver")
                return "menu_principal"
            if new_click and boton_menu.collidepoint((cursor_x, cursor_y)):
                menu_abierto = not menu_abierto
            if menu_abierto:
                alto = 40
                for index, nombre in enumerate(self.gestor_musica.canciones.keys()):
                    option = pygame.Rect(boton_menu.x, boton_menu.y + (index + 1) * alto, boton_menu.width, alto)
                    fill = (180, 220, 255) if nombre == self.gestor_musica.cancion_actual else COLOR_FONDO_B
                    pygame.draw.rect(self.screen, fill, option, border_radius=5)
                    pygame.draw.rect(self.screen, COLOR_BORDE, option, 1, border_radius=5)
                    label = FUENTE.render(nombre, True, NEGRO)
                    self.screen.blit(label, label.get_rect(center=option.center))
                    if new_click and option.collidepoint((cursor_x, cursor_y)):
                        self.gestor_musica.cambiar_cancion(nombre)
                        menu_abierto = False
            self.screen.blit(FUENTE.render(f"EAR: {self.camara.ear_suavizado:.3f}", True, BLANCO), (10, 10))
            self.screen.blit(FUENTE.render(f"Sensibilidad: {self.camara.sensibilidadO:.2f}", True, BLANCO), (10, 60))
            draw_cursor(self.screen, cursor_x, cursor_y)
            pygame.display.flip()
            clock.tick(30)


if __name__ == "__main__":
    Configuracion().ejecutar_configuracion()