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
from public_mock_support import FUENTE, MockCamera, MockMusicManager, NEGRO, draw_button, draw_cursor, init_display, load_background, load_image, log_action  # noqa: E402


def ejecutar_juego_ahorcado(camara=None, gestor_musica=None, id_sesion=1):
    screen = init_display("Public Mockup - Caza letras")
    width, height = screen.get_size()
    camera = camara or MockCamera(width, height)
    music = gestor_musica or MockMusicManager()
    game = BaseGame(id_sesion, "Caza letras")
    background = load_background(screen)
    clock = pygame.time.Clock()
    image_panel = pygame.Rect(50, 100, 300, 300)
    back_button = pygame.Rect(50, height - 80, 150, 50)
    word = "gato"
    shown = ["_", "_", "_", "_"]
    lives = 3
    score = 30
    rounds = 2
    target_image = load_image("Encuentra-y-Aprende/gato.png", (220, 220), label="Gato")
    letters = ["g", "a", "x", "o", "t", "z"]
    positions = [(500, 360), (650, 360), (800, 360), (500, 500), (650, 500), (800, 500)]
    click_state = False

    while True:
        cursor_x, cursor_y, click = camera.obtener_posicion_y_clic()
        new_click = click and not click_state
        click_state = click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.actualizar_resultados(puntaje=score, aciertos=4 - shown.count("_"), errores=3 - lives)
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, (204, 130, 76), image_panel, border_radius=20)
        pygame.draw.rect(screen, NEGRO, image_panel, 3, border_radius=20)
        screen.blit(target_image, target_image.get_rect(center=image_panel.center))
        for index, letter in enumerate(shown):
            x = 400 + index * 70
            rect = pygame.Rect(x, 150, 60, 60)
            pygame.draw.rect(screen, (204, 130, 76), rect, border_radius=10)
            pygame.draw.rect(screen, NEGRO, rect, 2, border_radius=10)
            if letter != "_":
                text = FUENTE.render(letter, True, NEGRO)
                screen.blit(text, text.get_rect(center=rect.center))

        for index, letter in enumerate(letters):
            x, y = positions[index]
            rect = pygame.Rect(x - 40, y - 40, 80, 80)
            fill = (224, 150, 96) if rect.collidepoint((cursor_x, cursor_y)) else (204, 130, 76)
            pygame.draw.rect(screen, fill, rect, border_radius=15)
            pygame.draw.rect(screen, NEGRO, rect, 3, border_radius=15)
            text = FUENTE.render(letter, True, NEGRO)
            screen.blit(text, text.get_rect(center=rect.center))
            if new_click and rect.collidepoint((cursor_x, cursor_y)):
                log_action(f"caza_letras.select:{letter}")
                if letter in word:
                    for pos, char in enumerate(word):
                        if char == letter:
                            shown[pos] = char
                    score += 5
                else:
                    lives = max(0, lives - 1)
                music.reproducir_sonido("mock-letter")

        for index in range(lives):
            screen.blit(load_image("General/globo.png", (60, 80), label="Vida"), (width - 220 - index * 70, 500))
        screen.blit(FUENTE.render("Cambio en: 9s", True, NEGRO), (width - 350, 150))
        screen.blit(FUENTE.render(f"Puntaje: {score}", True, NEGRO), (width - 350, 100))
        screen.blit(FUENTE.render(f"Rondas: {rounds}", True, NEGRO), (width - 350, 200))
        draw_button(screen, back_button, "Volver")
        if new_click and back_button.collidepoint((cursor_x, cursor_y)):
            log_action("caza_letras.back")
            return
        draw_cursor(screen, cursor_x, cursor_y)
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    ejecutar_juego_ahorcado()