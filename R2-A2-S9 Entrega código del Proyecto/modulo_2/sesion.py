import os
import sys

import pygame


CURRENT_DIR = os.path.dirname(__file__)
DOCS_DIR = os.path.dirname(CURRENT_DIR)
if DOCS_DIR not in sys.path:
    sys.path.insert(0, DOCS_DIR)

from public_mock_support import BORDE_BOTON, COLOR_INPUT, COLOR_TEXTO, FONDO_BOTON, FUENTE, FUENTE_MUY_PEQUENA, FUENTE_PEQUENA, MockProfile, NEGRO, draw_button, get_font, init_display, load_image, log_action  # noqa: E402


screen = init_display("Public Mockup - Sesión")
ANCHO, ALTO = screen.get_size()
fuente = FUENTE
fuente_pequena = FUENTE_PEQUENA
fuente_muy_pequena = FUENTE_MUY_PEQUENA
ICONO_EDITAR = load_image("General/editar.png", (24, 24), label="E")
ICONO_BORRAR = load_image("General/borrar.png", (24, 24), label="B")
fondo = load_image("General/fondo.png", (ANCHO, ALTO), label="Fondo")


class Button:
    def __init__(self, texto, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto

    def draw(self, surf, hover=False):
        fill = (230, 160, 100) if hover else FONDO_BOTON
        draw_button(surf, self.rect, self.texto, fuente, fill, BORDE_BOTON)

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)


class ButtonImage:
    def __init__(self, imagen_path, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.imagen = load_image(imagen_path, (w, h), label="X")

    def draw(self, surf, hover=False):
        surf.blit(self.imagen, self.rect)
        if hover:
            overlay = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 60))
            surf.blit(overlay, self.rect)

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)


class InputBox:
    def __init__(self, x, y, w, h, texto="", placeholder="", max_caracteres=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto
        self.placeholder = placeholder
        self.max_caracteres = max_caracteres
        self.active = False
        self.cursor_visible = True
        self.cursor_counter = 0

    def manejar_evento(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.texto = self.texto[:-1]
            elif event.key == pygame.K_RETURN:
                return self.texto
            elif event.unicode and (self.max_caracteres is None or len(self.texto) < self.max_caracteres):
                self.texto += event.unicode
        return None

    def update(self):
        self.cursor_counter += 1
        if self.cursor_counter % 30 == 0:
            self.cursor_visible = not self.cursor_visible

    def draw(self, surf):
        panel = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        pygame.draw.rect(panel, (255, 255, 255, 240), (0, 0, self.rect.w, self.rect.h))
        surf.blit(panel, self.rect.topleft)
        text = self.texto or self.placeholder
        color = COLOR_TEXTO if self.texto else (150, 150, 150)
        text_surface = fuente.render(text, True, color)
        surf.blit(text_surface, (self.rect.x + 14, self.rect.y + (self.rect.h - text_surface.get_height()) // 2))
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 14 + text_surface.get_width()
            pygame.draw.line(surf, COLOR_TEXTO, (cursor_x, self.rect.y + 10), (cursor_x, self.rect.y + self.rect.h - 10), 2)
        pygame.draw.rect(surf, COLOR_INPUT, self.rect, 3)


MOCK_USERS = [
    MockProfile(1, "Luna", "2018-03-14"),
    MockProfile(2, "Mateo", "2017-08-22"),
    MockProfile(3, "Sofía", "2016-11-05"),
]


def compute_modal_info(lista):
    modal_w, modal_h = 600, 420
    mx, my = (ANCHO - modal_w) // 2, (ALTO - modal_h) // 2
    modal_rect = pygame.Rect(mx, my, modal_w, modal_h)
    close_rect = pygame.Rect(mx + modal_w - 50, my + 16, 30, 30)
    botones = []
    scroll_y = my + 70
    for user in lista:
        card_rect = pygame.Rect(mx + 30, scroll_y, modal_w - 60, 70)
        botones.append({
            "edit": pygame.Rect(card_rect.right - 95, card_rect.y + 12, 36, 36),
            "del": pygame.Rect(card_rect.right - 50, card_rect.y + 12, 36, 36),
            "user": user,
            "card": card_rect,
            "select_rect": pygame.Rect(card_rect.x, card_rect.y, card_rect.w - 100, card_rect.h),
        })
        scroll_y += 80
    return {"modal_rect": modal_rect, "close_rect": close_rect, "botones": botones, "mx": mx, "my": my, "modal_w": modal_w}


def draw_modal_from_info(info):
    overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    mx, my = info["mx"], info["my"]
    modal = pygame.Surface((info["modal_w"], info["modal_rect"].h), pygame.SRCALPHA)
    pygame.draw.rect(modal, (255, 255, 255, 250), (0, 0, info["modal_w"], info["modal_rect"].h), border_radius=15)
    pygame.draw.rect(modal, BORDE_BOTON, (0, 0, info["modal_w"], info["modal_rect"].h), 3, border_radius=15)
    title = fuente.render("Usuarios Registrados", True, COLOR_TEXTO)
    modal.blit(title, ((info["modal_w"] - title.get_width()) // 2, 20))
    subtitle = fuente_muy_pequena.render("Selecciona un perfil para jugar", True, (120, 120, 120))
    modal.blit(subtitle, ((info["modal_w"] - subtitle.get_width()) // 2, 55))
    screen.blit(modal, (mx, my))
    pygame.draw.circle(screen, (240, 240, 240), info["close_rect"].center, 15)
    pygame.draw.line(screen, (150, 150, 150), (info["close_rect"].x + 8, info["close_rect"].y + 8), (info["close_rect"].x + 22, info["close_rect"].y + 22), 3)
    pygame.draw.line(screen, (150, 150, 150), (info["close_rect"].x + 22, info["close_rect"].y + 8), (info["close_rect"].x + 8, info["close_rect"].y + 22), 3)
    mouse_pos = pygame.mouse.get_pos()
    for button in info["botones"]:
        hover = button["select_rect"].collidepoint(mouse_pos)
        fill = (235, 245, 255) if hover else (250, 250, 250)
        border = (100, 150, 255) if hover else (210, 210, 210)
        pygame.draw.rect(screen, fill, button["card"], border_radius=10)
        pygame.draw.rect(screen, border, button["card"], 2, border_radius=10)
        label = fuente_pequena.render(button["user"].nickname, True, COLOR_TEXTO)
        screen.blit(label, (button["card"].x + 20, button["card"].centery - label.get_height() // 2))
        pygame.draw.circle(screen, (240, 245, 255), button["edit"].center, 18)
        screen.blit(ICONO_EDITAR, ICONO_EDITAR.get_rect(center=button["edit"].center))
        pygame.draw.circle(screen, (255, 240, 240), button["del"].center, 18)
        screen.blit(ICONO_BORRAR, ICONO_BORRAR.get_rect(center=button["del"].center))


def login():
    panel_w, panel_h = int(ANCHO * 0.45), int(ALTO * 0.5)
    panel_x, panel_y = (ANCHO - panel_w) // 2, (ALTO - panel_h) // 2
    field_w, field_h = int(panel_w * 0.6), 56
    sx, sy = panel_x + (panel_w - field_w) // 2, panel_y + 100
    input_usuario = InputBox(sx, sy, field_w, field_h, "", "Usuario", 25)
    boton_login = Button("Iniciar sesión", sx, sy + field_h + 40, field_w, 56)
    boton_registro = Button("Crear Usuario", sx, sy + field_h + 120, field_w, 56)
    boton_ver = Button("Ver Usuarios", sx, sy + field_h + 200, field_w, 56)
    boton_salir = ButtonImage("Botones/cerrar-programa.png", sx + 200, sy + field_h + 315, 56, 56)
    mostrando_lista = False
    modal_info = None
    mensaje = ""
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            input_usuario.manejar_evento(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if mostrando_lista and modal_info:
                    if modal_info["close_rect"].collidepoint(pos):
                        mostrando_lista = False
                        modal_info = None
                        continue
                    for item in modal_info["botones"]:
                        if item["edit"].collidepoint(pos):
                            log_action(f"sesion.edit:{item['user'].nickname}")
                        elif item["del"].collidepoint(pos):
                            log_action(f"sesion.delete:{item['user'].nickname}")
                        elif item["select_rect"].collidepoint(pos):
                            log_action(f"sesion.select:{item['user'].nickname}")
                            return {"id_sesion": item["user"].id_usuario, "nickname": item["user"].nickname}
                elif boton_login.collidepoint(pos):
                    nickname = input_usuario.texto.strip() or MOCK_USERS[0].nickname
                    log_action(f"sesion.login:{nickname}")
                    return {"id_sesion": 100 + len(nickname), "nickname": nickname}
                elif boton_registro.collidepoint(pos):
                    log_action("sesion.register")
                    mensaje = "Mock user created"
                elif boton_ver.collidepoint(pos):
                    mostrando_lista = True
                    modal_info = compute_modal_info(MOCK_USERS)
                elif boton_salir.collidepoint(pos):
                    return None
        input_usuario.update()
        screen.blit(fondo, (0, 0))
        shadow = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 40), (0, 0, panel_w, panel_h))
        screen.blit(shadow, (panel_x + 6, panel_y + 6))
        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        pygame.draw.rect(panel, (255, 255, 255, 230), (0, 0, panel_w, panel_h))
        pygame.draw.rect(panel, (230, 230, 230, 200), (0, 0, panel_w, panel_h), 3)
        screen.blit(panel, (panel_x, panel_y))
        title = fuente.render("INICIAR SESIÓN", True, COLOR_TEXTO)
        screen.blit(title, (panel_x + (panel_w - title.get_width()) // 2, panel_y + 30))
        input_usuario.draw(screen)
        boton_login.draw(screen, boton_login.rect.collidepoint(pygame.mouse.get_pos()))
        boton_registro.draw(screen, boton_registro.rect.collidepoint(pygame.mouse.get_pos()))
        boton_ver.draw(screen, boton_ver.rect.collidepoint(pygame.mouse.get_pos()))
        boton_salir.draw(screen, boton_salir.rect.collidepoint(pygame.mouse.get_pos()))
        if mensaje:
            msg = fuente.render(mensaje, True, COLOR_TEXTO)
            screen.blit(msg, (panel_x + (panel_w - msg.get_width()) // 2, panel_y + panel_h - 40))
        if mostrando_lista and modal_info:
            draw_modal_from_info(modal_info)
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    login()