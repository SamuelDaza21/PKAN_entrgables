import os
import random
import sys

import pygame


CURRENT_DIR = os.path.dirname(__file__)
DOCS_DIR = os.path.dirname(CURRENT_DIR)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)
if DOCS_DIR not in sys.path:
    sys.path.insert(0, DOCS_DIR)

from base_game import BaseGame  # noqa: E402
from public_mock_support import FUENTE_PEQUENA, MockCamera, MockMusicManager, NEGRO, draw_button, draw_cursor, init_display, load_background, load_image, log_action  # noqa: E402


def ejecutar_encuentra_y_aprende(camara=None, gestor_musica=None, id_sesion=1):
    screen = init_display("Public Mockup - Encuentra y aprende")
    width, height = screen.get_size()
    camera = camara or MockCamera(width, height)
    music = gestor_musica or MockMusicManager()
    game = BaseGame(id_sesion, "Encuentra y aprende")
    background = load_background(screen)
    clock = pygame.time.Clock()
    back_button = pygame.Rect(50, height - 80, 150, 50)
    round_number = 1
    score = 20
    lives = 3
    items = [
        {"nombre": "perro", "imagen": load_image("Encuentra-y-Aprende/perro.png", (150, 150), label="Perro")},
        {"nombre": "gato", "imagen": load_image("Encuentra-y-Aprende/gato.png", (150, 150), label="Gato")},
        {"nombre": "pez", "imagen": load_image("Encuentra-y-Aprende/pez.png", (150, 150), label="Pez")},
    ]
    target = random.choice(items)["nombre"]
    clicked = False

    while True:
        cursor_x, cursor_y, click = camera.obtener_posicion_y_clic()
        new_click = click and not clicked
        clicked = click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.actualizar_resultados(puntaje=score, aciertos=2, errores=1)
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        screen.blit(background, (0, 0))
        screen.blit(FUENTE_PEQUENA.render(f"Encuentra: {target}", True, NEGRO), (width // 2 - 120, 120))
        for index, item in enumerate(items):
            rect = pygame.Rect(200 + index * 300, 250, 200, 200)
            fill = (241, 182, 125) if rect.collidepoint((cursor_x, cursor_y)) else (221, 162, 105)
            pygame.draw.rect(screen, fill, rect, border_radius=20)
            pygame.draw.rect(screen, NEGRO, rect, 3, border_radius=20)
            screen.blit(item["imagen"], item["imagen"].get_rect(center=rect.center))
            if new_click and rect.collidepoint((cursor_x, cursor_y)):
                log_action(f"encuentra_y_aprende.select:{item['nombre']}")
                if item["nombre"] == target:
                    score += 10
                else:
                    lives = max(0, lives - 1)
                round_number += 1
                target = random.choice(items)["nombre"]
                music.reproducir_sonido("mock-select")

        for life_index in range(lives):
            pygame.draw.circle(screen, (255, 0, 0), (1450 + life_index * 55, 70), 15)
            pygame.draw.circle(screen, NEGRO, (1450 + life_index * 55, 70), 15, 2)

        panel = pygame.Rect(20, 20, 200, 120)
        pygame.draw.rect(screen, (221, 162, 105, 200), panel, border_radius=15)
        pygame.draw.rect(screen, NEGRO, panel, 2, border_radius=15)
        screen.blit(FUENTE_PEQUENA.render(f"Puntos: {score}", True, NEGRO), (40, 40))
        screen.blit(FUENTE_PEQUENA.render(f"Ronda: {round_number}", True, NEGRO), (40, 80))
        draw_button(screen, back_button, "Volver", FUENTE_PEQUENA)
        if new_click and back_button.collidepoint((cursor_x, cursor_y)):
            log_action("encuentra_y_aprende.back")
            return
        draw_cursor(screen, cursor_x, cursor_y)
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    ejecutar_encuentra_y_aprende()