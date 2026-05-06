import math
import os
import sys

import pygame


CURRENT_DIR = os.path.dirname(__file__)
DOCS_DIR = os.path.dirname(CURRENT_DIR)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)
if DOCS_DIR not in sys.path:
    sys.path.insert(0, DOCS_DIR)

from base_game import BaseGame  # noqa: E402
from public_mock_support import FUENTE, FUENTE_PEQUENA, MockCamera, MockMusicManager, NEGRO, draw_cursor, init_display, load_image, log_action  # noqa: E402
from question_manager import LABERINTO_QUESTIONS, QuestionPool  # noqa: E402
from question_ui import QuestionUIRenderer  # noqa: E402


def ejecutar_juego_laberinto(camara=None, gestor_musica=None, id_sesion=1):
    screen = init_display("Public Mockup - Mate-reto")
    width, height = screen.get_size()
    camera = camara or MockCamera(width, height)
    music = gestor_musica or MockMusicManager()
    game = BaseGame(id_sesion, "Laberinto")
    clock = pygame.time.Clock()
    background = load_image("Mate-Reto/laberinto1.png", (width, height), label="Laberinto")
    circle = load_image("Mate-Reto/circulo_laberinto.png", (30, 30), label="O")
    next_button = pygame.Rect(width - 260, height - 100, 200, 50)
    star = load_image("Mate-Reto/estrella.png", (40, 40), label="*")
    stars = [(width - 1032, height - 637), (width - 785, height - 465), (width - 600, height - 332)]
    current_center = [width - 860, height // 8]
    meta = pygame.Rect(width - 828, height - 205, 40, 40)
    question_pool = QuestionPool(LABERINTO_QUESTIONS)
    current_question = question_pool.get_next_question()
    renderer = QuestionUIRenderer(width, height, FUENTE, FUENTE_PEQUENA)
    answer_rects = []
    click_state = False
    score = 0

    while True:
        cursor_x, cursor_y, click = camera.obtener_posicion_y_clic()
        new_click = click and not click_state
        click_state = click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.actualizar_resultados(puntaje=score, aciertos=score // 10, errores=0)
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        dx = cursor_x - current_center[0]
        dy = cursor_y - current_center[1]
        distance = math.hypot(dx, dy)
        if distance > 3:
            current_center[0] += dx * 0.08
            current_center[1] += dy * 0.08

        screen.blit(background, (0, 0))
        for star_pos in stars:
            screen.blit(star, star_pos)
        pygame.draw.rect(screen, (90, 255, 90), meta, border_radius=10)
        screen.blit(circle, circle.get_rect(center=(int(current_center[0]), int(current_center[1]))))
        answer_rects = renderer.render_question_panel(screen, current_question)
        for rect, answer in answer_rects:
            if new_click and rect.collidepoint((cursor_x, cursor_y)):
                log_action(f"mate_reto.answer:{answer}")
                score += 10 if answer == current_question.correct_answer else 0
                music.reproducir_sonido("mock-answer")
                current_question = question_pool.get_next_question()
        pygame.draw.rect(screen, (221, 162, 105), next_button, border_radius=12)
        pygame.draw.rect(screen, NEGRO, next_button, 2, border_radius=12)
        next_text = FUENTE_PEQUENA.render("Siguiente", True, NEGRO)
        screen.blit(next_text, next_text.get_rect(center=next_button.center))
        if new_click and next_button.collidepoint((cursor_x, cursor_y)):
            log_action("mate_reto.next")
            current_question = question_pool.get_next_question()
        score_text = FUENTE.render(f"Puntaje: {score}", True, NEGRO)
        screen.blit(score_text, (40, height - 90))
        draw_cursor(screen, cursor_x, cursor_y)
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    ejecutar_juego_laberinto()