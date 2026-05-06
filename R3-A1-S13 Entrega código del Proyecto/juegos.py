import os
import sys

import pygame


CURRENT_DIR = os.path.dirname(__file__)
DOCS_DIR = os.path.dirname(CURRENT_DIR)
if DOCS_DIR not in sys.path:
    sys.path.insert(0, DOCS_DIR)

from public_mock_support import BLANCO, FUENTE, HOVER, MockBottomBar, MockCamera, MockMusicManager, NEGRO, SAVE_BG, SAVE_BORDER, draw_cursor, draw_outlined_text, init_display, load_image, log_action  # noqa: E402


class MenuJuegos:
    def __init__(self, camara=None, gestor_musica=None, ID_sesion=1):
        self.screen = init_display("Public Mockup - Juegos")
        self.width, self.height = self.screen.get_size()
        self.camara = camara or MockCamera(self.width, self.height)
        self.gestor_musica = gestor_musica or MockMusicManager()
        self.ID_sesion = ID_sesion
        self.fondo = load_image("General/fondo.png", (self.width, self.height), label="Juegos")
        self.juegos = [
            {"nombre": "Pares mágicos", "imagen": "Juegos/pares_magicos.jpg", "accion": "pares_magicos"},
            {"nombre": "Animalia", "imagen": "Juegos/animalia.jpg", "accion": "animalia"},
            {"nombre": "Mate-reto", "imagen": "Juegos/mate-reto.jpg", "accion": "mate_reto"},
            {"nombre": "Encuentra y aprende", "imagen": "Juegos/encuentra.jpg", "accion": "encuentra"},
            {"nombre": "Caza letras", "imagen": "Juegos/caza_letras.jpg", "accion": "caza_letras"},
        ]
        self.start_index = 0
        self.vista_count = 3
        self.tamano = (290, 280)
        for juego in self.juegos:
            juego["surface"] = load_image(juego["imagen"], self.tamano, label=juego["nombre"][:6])
        size = int(min(self.width, self.height) * 0.1)
        self.barra = MockBottomBar(self.width, self.height, [
            {"label": "Instrucciones", "icon": load_image("menu/instrucciones.png", (size, size), label="I"), "action": "instrucciones"},
            {"label": "Configuración", "icon": load_image("menu/configuraciones.png", (size, size), label="C"), "action": "configuracion"},
            {"label": "Salir", "icon": load_image("menu/salida.png", (size, size), label="S"), "action": "salir"},
            {"label": "Información", "icon": load_image("menu/informacion.png", (size, size), label="?"), "action": "informacion"},
            {"label": "Jugar", "icon": load_image("menu/juegos.png", (size, size), label="J"), "action": "jugar"},
            {"label": "Inicio", "icon": load_image("menu/inicio.png", (size, size), label="H"), "action": "inicio"},
        ])

    def dibujar(self, cursor_x, cursor_y):
        self.screen.blit(self.fondo, (0, 0))
        separation = int(self.width * 0.05)
        total_visible = min(self.vista_count, len(self.juegos))
        width_cards = total_visible * self.tamano[0] + (total_visible - 1) * separation
        start_x = (self.width - width_cards) // 2
        y_cards = int(self.height * 0.25)
        center_y = y_cards + self.tamano[1] // 2
        self.left_rect = pygame.Rect(start_x - 100, center_y - 40, 60, 80)
        self.right_rect = pygame.Rect(start_x + width_cards + 40, center_y - 40, 60, 80)
        for rect, direction in [(self.left_rect, "left"), (self.right_rect, "right")]:
            fill = HOVER if rect.collidepoint((cursor_x, cursor_y)) else SAVE_BG
            pygame.draw.rect(self.screen, fill, rect, border_radius=15)
            if direction == "left":
                points = [(rect.centerx + 10, rect.centery - 20), (rect.centerx - 10, rect.centery), (rect.centerx + 10, rect.centery + 20)]
            else:
                points = [(rect.centerx - 10, rect.centery - 20), (rect.centerx + 10, rect.centery), (rect.centerx - 10, rect.centery + 20)]
            pygame.draw.polygon(self.screen, BLANCO, points)
        self.card_rects = []
        for offset in range(total_visible):
            index = (self.start_index + offset) % len(self.juegos)
            rect = pygame.Rect(start_x + offset * (self.tamano[0] + separation), y_cards, *self.tamano)
            self.card_rects.append((rect, index))
            juego = self.juegos[index]
            if rect.collidepoint((cursor_x, cursor_y)):
                hover = pygame.transform.scale(juego["surface"], (int(self.tamano[0] * 1.1), int(self.tamano[1] * 1.1)))
                hover_rect = hover.get_rect(center=rect.center)
                self.screen.blit(hover, hover_rect)
                pygame.draw.rect(self.screen, BLANCO, hover_rect, 12)
                draw_outlined_text(self.screen, juego["nombre"], FUENTE, SAVE_BG, NEGRO, (rect.centerx, rect.bottom + 40))
            else:
                self.screen.blit(juego["surface"], rect)
                pygame.draw.rect(self.screen, SAVE_BORDER, rect, 12)
                draw_outlined_text(self.screen, juego["nombre"], FUENTE, BLANCO, HOVER, (rect.centerx, rect.bottom + 30))

    def manejar_interaccion(self, cursor_x, cursor_y, click):
        if self.left_rect.collidepoint((cursor_x, cursor_y)) and click:
            self.start_index = (self.start_index - 1) % len(self.juegos)
            return None
        if self.right_rect.collidepoint((cursor_x, cursor_y)) and click:
            self.start_index = (self.start_index + 1) % len(self.juegos)
            return None
        for rect, index in self.card_rects:
            if rect.collidepoint((cursor_x, cursor_y)) and click:
                log_action(f"menu_juegos.launch:{self.juegos[index]['accion']}")
                return self.juegos[index]["accion"]
        return None

    def ejecutar(self):
        clock = pygame.time.Clock()
        click_state = False
        while True:
            cursor_x, cursor_y, click = self.camara.obtener_posicion_y_clic()
            new_click = click and not click_state
            click_state = click
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "menu_principal"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "menu_principal"
            self.dibujar(cursor_x, cursor_y)
            launch = self.manejar_interaccion(cursor_x, cursor_y, new_click)
            if launch:
                log_action(f"menu_juegos.mock_launch:{launch}")
            self.barra.actualizar_visibilidad((cursor_x, cursor_y))
            self.barra.dibujar(self.screen, (cursor_x, cursor_y))
            destino = self.barra.manejar_clic((cursor_x, cursor_y), new_click)
            if destino:
                return destino
            draw_cursor(self.screen, cursor_x, cursor_y)
            pygame.display.flip()
            clock.tick(30)


if __name__ == "__main__":
    MenuJuegos().ejecutar()