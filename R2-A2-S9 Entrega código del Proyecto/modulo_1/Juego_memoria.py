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
from public_mock_support import FUENTE, MockCamera, MockMusicManager, NEGRO, SAVE_BG, SAVE_BORDER, draw_cursor, init_display, load_background, load_image, log_action  # noqa: E402


def ejecutar_juego_memoria(camara=None, gestor_musica=None, id_sesion=1):
    screen = init_display("Public Mockup - Pares mágicos")
    width, height = screen.get_size()
    camera = camara or MockCamera(width, height)
    music = gestor_musica or MockMusicManager()
    game = BaseGame(id_sesion, "Pares mágicos")
    background = load_background(screen)
    clock = pygame.time.Clock()
    back_rect = pygame.Rect(width - 260, height - 100, 200, 50)
    back_icon = load_image("Botones/Home.png", (50, 50), label="Home")
    card_face = [load_image(f"Pares/tarjeta{i}.png", (186, 186), label=f"{i}") for i in range(1, 7)]
    card_back = load_image("Botones/vuelta.png", (186, 186), label="?")
    deck = card_face * 2
    random.shuffle(deck)
    cards = []
    flipped = []
    score = 0
    for row in range(4):
        for col in range(3):
            rect = pygame.Rect(500 + col * 206, 110 + row * 206, 186, 186)
            cards.append({"image": deck[row * 3 + col], "rect": rect, "visible": True})
    click_state = False

    while True:
        cursor_x, cursor_y, click = camera.obtener_posicion_y_clic()
        new_click = click and not click_state
        click_state = click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.actualizar_resultados(puntaje=score, aciertos=score, errores=max(0, len(flipped) - score))
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        screen.blit(background, (0, 0))
        for index, card in enumerate(cards):
            current_surface = card["image"] if card["visible"] or index in flipped else card_back
            screen.blit(current_surface, card["rect"])
            if new_click and card["rect"].collidepoint((cursor_x, cursor_y)):
                log_action(f"pares_magicos.flip:{index}")
                if index not in flipped:
                    flipped.append(index)
                    music.reproducir_sonido("mock-flip")
                if len(flipped) == 2:
                    score += 1
                    for selected in flipped:
                        cards[selected]["visible"] = True
                    flipped.clear()

        pygame.draw.rect(screen, SAVE_BORDER, back_rect, border_radius=10)
        pygame.draw.rect(screen, SAVE_BG, back_rect.inflate(-6, -6), border_radius=10)
        screen.blit(back_icon, back_icon.get_rect(center=back_rect.center))
        if new_click and back_rect.collidepoint((cursor_x, cursor_y)):
            log_action("pares_magicos.back")
            return
        score_surface = FUENTE.render(f"Puntaje: {score}", True, NEGRO)
        screen.blit(score_surface, (width - score_surface.get_width() - 60, 100))
        draw_cursor(screen, cursor_x, cursor_y)
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    ejecutar_juego_memoria()