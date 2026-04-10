import os
import sys

import pygame


CURRENT_DIR = os.path.dirname(__file__)
DOCS_DIR = os.path.dirname(CURRENT_DIR)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)
if DOCS_DIR not in sys.path:
    sys.path.insert(0, DOCS_DIR)

from public_mock_support import BORDE_BOTON, BLANCO, COLOR_FONDO_B, NEGRO, load_image  # noqa: E402
from question_manager import QuestionType  # noqa: E402


class QuestionUIRenderer:
    def __init__(self, screen_width, screen_height, title_font, body_font):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title_font = title_font
        self.body_font = body_font
        self.answer_width = 180
        self.answer_height = 120
        self.answer_spacing = 20

    def _adjust_text(self, text, color, max_width, max_height):
        for size in range(28, 12, -2):
            font = pygame.font.Font(self.title_font.get_name() if hasattr(self.title_font, "get_name") else None, size)
            words = text.split()
            lines = []
            line = []
            for word in words:
                probe = " ".join(line + [word])
                if font.size(probe)[0] <= max_width - 10:
                    line.append(word)
                else:
                    lines.append(" ".join(line))
                    line = [word]
            if line:
                lines.append(" ".join(line))
            total_height = len(lines) * font.get_linesize()
            if total_height <= max_height - 10:
                surface = pygame.Surface((max_width, max_height), pygame.SRCALPHA)
                y_offset = (max_height - total_height) // 2
                for item in lines:
                    text_surface = font.render(item, True, color)
                    surface.blit(text_surface, ((max_width - text_surface.get_width()) // 2, y_offset))
                    y_offset += font.get_linesize()
                return surface
        fallback = pygame.Surface((max_width, max_height), pygame.SRCALPHA)
        text_surface = self.body_font.render(text[:18], True, color)
        fallback.blit(text_surface, text_surface.get_rect(center=(max_width // 2, max_height // 2)))
        return fallback

    def render_question_panel(self, screen, question):
        overlay = pygame.Surface((self.screen_width, 330), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        pygame.draw.rect(screen, BORDE_BOTON, (0, 0, self.screen_width, 330), 3)
        question_surface = self._adjust_text(question.question, BLANCO, self.screen_width - 60, 90)
        screen.blit(question_surface, (30, 20))
        if question.question_type == QuestionType.IMAGE_SEQUENCE and question.sequence:
            self._render_sequence(screen, question.sequence, 120)
        return self._render_answers(screen, question.get_shuffled_answers(), 190)

    def _render_sequence(self, screen, sequence, y_pos):
        x_pos = 60
        for element in sequence:
            if isinstance(element, str) and element.lower().endswith(".png"):
                image = load_image(element, (70, 70), label="IMG")
                screen.blit(image, (x_pos, y_pos))
            else:
                text = self.body_font.render(element, True, BLANCO)
                screen.blit(text, (x_pos + 8, y_pos + 26))
            x_pos += 100

    def _render_answers(self, screen, answers, y_pos):
        rects = []
        total_width = len(answers) * (self.answer_width + self.answer_spacing)
        start_x = max(30, (self.screen_width - total_width) // 2)
        for index, answer in enumerate(answers):
            rect = pygame.Rect(start_x + index * (self.answer_width + self.answer_spacing), y_pos, self.answer_width, self.answer_height)
            pygame.draw.rect(screen, COLOR_FONDO_B, rect, border_radius=10)
            pygame.draw.rect(screen, BORDE_BOTON, rect, 3, border_radius=10)
            if isinstance(answer, str) and answer.lower().endswith(".png"):
                image = load_image(answer, (self.answer_width - 10, self.answer_height - 10), label="IMG")
                screen.blit(image, image.get_rect(center=rect.center))
            else:
                text = self._adjust_text(answer, NEGRO, self.answer_width - 10, self.answer_height - 10)
                screen.blit(text, text.get_rect(center=rect.center))
            rects.append((rect, answer))
        return rects