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
from public_mock_support import FUENTE, MockCamera, MockMusicManager, NEGRO, SAVE_BG, draw_cursor, init_display, load_background, load_image, log_action  # noqa: E402


def ejecutar_puzzle_animales(camara=None, gestor_musica=None, id_sesion=1):
    screen = init_display("Public Mockup - Animalia")
    width, height = screen.get_size()
    camera = camara or MockCamera(width, height)
    music = gestor_musica or MockMusicManager()
    game = BaseGame(id_sesion, "Animalia")
    background = load_background(screen)
    clock = pygame.time.Clock()
    title = FUENTE.render("¡Ayuda a cada animal a llegar a su hábitat!", True, NEGRO)
    title_rect = pygame.Rect(width // 2 - (title.get_width() + 60) // 2, 30, title.get_width() + 60, 80)
    menu_button = pygame.Rect(50, height - 100, 70, 70)
    menu_icon = load_image("Botones/Home.png", (60, 60), label="Home")
    animals = [
        {"name": "tigre", "image": load_image("Animalia/animal_tigre.png", (width // 8, width // 8), label="Tigre")},
        {"name": "elefante", "image": load_image("Animalia/animal_elefante.png", (width // 8, width // 8), label="Elef.")},
        {"name": "orca", "image": load_image("Animalia/animal_orca.png", (width // 8, width // 8), label="Orca")},
        {"name": "canguro", "image": load_image("Animalia/animal_canguro.png", (width // 8, width // 8), label="Cang.")},
    ]
    habitats = [
        {"name": "jungla", "image": load_image("Animalia/habitat_jungla.jpg", (width // 5, height // 5), label="Jungla")},
        {"name": "sabana", "image": load_image("Animalia/habitat_sabana.jpg", (width // 5, height // 5), label="Sabana")},
        {"name": "oceano", "image": load_image("Animalia/habitat_oceano.jpg", (width // 5, height // 5), label="Océano")},
        {"name": "pradera", "image": load_image("Animalia/habitat_pradera.jpg", (width // 5, height // 5), label="Pradera")},
    ]
    random.shuffle(animals)
    draggable = []
    for index, animal in enumerate(animals):
        draggable.append({
            "name": animal["name"],
            "image": animal["image"],
            "rect": pygame.Rect(160 + index * 270, height // 3, width // 8, width // 8),
            "origin": (160 + index * 270, height // 3),
            "dragging": False,
        })
    habitat_rects = []
    for index, habitat in enumerate(habitats):
        rect = pygame.Rect(80 + index * 360, height - (height // 5) - 150, width // 5, height // 5)
        habitat_rects.append((habitat, rect))

    dragging = None
    click_state = False
    score = 0
    lives = 3
    while True:
        cursor_x, cursor_y, click = camera.obtener_posicion_y_clic()
        new_click = click and not click_state
        click_state = click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.actualizar_resultados(puntaje=score, aciertos=score // 10, errores=3 - lives)
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, SAVE_BG, title_rect, border_radius=15)
        screen.blit(title, title.get_rect(center=title_rect.center))
        for habitat, rect in habitat_rects:
            screen.blit(habitat["image"], rect)

        for animal in draggable:
            if animal["dragging"]:
                animal["rect"].center = (cursor_x, cursor_y)
            screen.blit(animal["image"], animal["rect"])
            if new_click and dragging is None and animal["rect"].collidepoint((cursor_x, cursor_y)):
                dragging = animal
                animal["dragging"] = True
                music.reproducir_sonido("mock-pick")

        if new_click and menu_button.collidepoint((cursor_x, cursor_y)):
            log_action("animalia.back")
            return

        if new_click and dragging is not None:
            dragging["dragging"] = False
            dropped = False
            for habitat, rect in habitat_rects:
                if rect.collidepoint((cursor_x, cursor_y)):
                    log_action(f"animalia.drop:{dragging['name']}->{habitat['name']}")
                    score += 10
                    dropped = True
                    music.reproducir_sonido("mock-drop")
                    break
            if not dropped:
                dragging["rect"].topleft = dragging["origin"]
                lives = max(0, lives - 1)
            dragging = None

        for rect, text in [(pygame.Rect(width - 240, height - 140, 220, 60), f"Vidas: {lives}/3"), (pygame.Rect(width - 240, height - 70, 220, 60), f"Puntos: {score}")]:
            pygame.draw.rect(screen, SAVE_BG, rect, border_radius=15)
            label = FUENTE.render(text, True, NEGRO)
            screen.blit(label, label.get_rect(center=rect.center))
        screen.blit(menu_icon, menu_icon.get_rect(center=menu_button.center))
        draw_cursor(screen, cursor_x, cursor_y)
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    ejecutar_puzzle_animales()