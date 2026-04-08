import os
import sys

import pygame


CURRENT_DIR = os.path.dirname(__file__)
DOCS_DIR = os.path.dirname(CURRENT_DIR)
if DOCS_DIR not in sys.path:
    sys.path.insert(0, DOCS_DIR)

from public_mock_support import AZUL, COLOR_FONDO, FUENTE, FUENTE_MUY_PEQUENA, MockBottomBar, MockCamera, MockMusicManager, MockVoice, NEGRO, draw_cursor, init_display, load_image, log_action  # noqa: E402


class SistemaTTS:
    def __init__(self):
        self.voice = MockVoice()

    def decir_texto(self, texto):
        self.voice.decir_texto(texto)
        return True


class Inicio:
    def __init__(self, camara=None, gestor_musica=None, ID_sesion=1):
        self.screen = init_display("Public Mockup - Inicio")
        self.width, self.height = self.screen.get_size()
        self.ID_sesion = ID_sesion
        self.camara = camara or MockCamera(self.width, self.height)
        self.gestor_musica = gestor_musica or MockMusicManager()
        self.tts_sistema = SistemaTTS()
        self.control_clic = False
        self.iconos = {}
        self.cuadros = self.crear_cuadros()
        self.cargar_iconos()
        self.botones_comunicacion = self.crear_botones_comunicacion()
        self.barra_inferior = MockBottomBar(self.width, self.height, [
            {"label": "Instrucciones", "icon": self.iconos["instrucciones"]["imagen"], "action": "instrucciones"},
            {"label": "Configuración", "icon": self.iconos["configuracion"]["imagen"], "action": "configuracion"},
            {"label": "Salir", "icon": self.iconos["salir"]["imagen"], "action": "salir"},
            {"label": "Información", "icon": self.iconos["info"]["imagen"], "action": "informacion"},
            {"label": "Jugar", "icon": self.iconos["jugar"]["imagen"], "action": "jugar"},
            {"label": "Inicio", "icon": self.iconos["inicio"]["imagen"], "action": "inicio"},
        ])

    def cargar_iconos(self):
        iconos_info = [
            {"nombre": "instrucciones", "archivo": "menu/instrucciones.png", "texto": "Instrucciones"},
            {"nombre": "configuracion", "archivo": "menu/configuraciones.png", "texto": "Configuración"},
            {"nombre": "salir", "archivo": "menu/salida.png", "texto": "Salir"},
            {"nombre": "info", "archivo": "menu/informacion.png", "texto": "Información"},
            {"nombre": "jugar", "archivo": "menu/juegos.png", "texto": "Jugar"},
            {"nombre": "inicio", "archivo": "menu/inicio.png", "texto": "Inicio"},
            {"nombre": "hola", "archivo": "Inicio/hola.png", "texto": "HOLA"},
            {"nombre": "adios", "archivo": "Inicio/adios.png", "texto": "ADIÓS"},
            {"nombre": "gracias", "archivo": "Inicio/gracias.png", "texto": "GRACIAS"},
            {"nombre": "porfavor", "archivo": "Inicio/porfavor.png", "texto": "POR FAVOR"},
            {"nombre": "si", "archivo": "Inicio/si.png", "texto": "SÍ"},
            {"nombre": "no", "archivo": "Inicio/no.png", "texto": "NO"},
            {"nombre": "hambre", "archivo": "Inicio/hambre.png", "texto": "HAMBRE"},
            {"nombre": "incomodo", "archivo": "Inicio/incomodo.png", "texto": "INCÓMODO"},
            {"nombre": "bano", "archivo": "Inicio/bano.png", "texto": "BAÑO"},
            {"nombre": "sed", "archivo": "Inicio/sed.png", "texto": "SED"},
            {"nombre": "cansado", "archivo": "Inicio/cansado.png", "texto": "CANSADO"},
            {"nombre": "dolor", "archivo": "Inicio/dolor.png", "texto": "DOLOR"},
            {"nombre": "feliz", "archivo": "Inicio/feliz.png", "texto": "FELIZ"},
            {"nombre": "triste", "archivo": "Inicio/triste.png", "texto": "TRISTE"},
            {"nombre": "enojado", "archivo": "Inicio/enojado.png", "texto": "ENOJADO"},
            {"nombre": "miedo", "archivo": "Inicio/miedo.png", "texto": "MIEDO"},
            {"nombre": "nervioso", "archivo": "Inicio/nervioso.png", "texto": "NERVIOSO"},
            {"nombre": "calma", "archivo": "Inicio/calma.png", "texto": "CALMA"},
            {"nombre": "ayuda", "archivo": "Inicio/ayuda.png", "texto": "AYUDA"},
            {"nombre": "no-quiero", "archivo": "Inicio/noquiero.png", "texto": "NO QUIERO"},
            {"nombre": "mas", "archivo": "Inicio/mas.png", "texto": "MÁS"},
            {"nombre": "quiero", "archivo": "Inicio/quiero.png", "texto": "QUIERO"},
            {"nombre": "basta", "archivo": "Inicio/basta.png", "texto": "BASTA"},
            {"nombre": "espera", "archivo": "Inicio/espera.png", "texto": "ESPERA"},
            {"nombre": "mama", "archivo": "Inicio/mama.png", "texto": "MAMÁ"},
            {"nombre": "enfermera", "archivo": "Inicio/enfermera.png", "texto": "ENFERMERA"},
            {"nombre": "hermano", "archivo": "Inicio/hermano.png", "texto": "HERMANO"},
            {"nombre": "papa", "archivo": "Inicio/papa.png", "texto": "PAPÁ"},
            {"nombre": "maestra", "archivo": "Inicio/maestra.png", "texto": "MAESTRA"},
            {"nombre": "amigo", "archivo": "Inicio/amigo.png", "texto": "AMIGO"},
            {"nombre": "jugar-act", "archivo": "Inicio/jugar.png", "texto": "JUGAR"},
            {"nombre": "salir-act", "archivo": "Inicio/salir.png", "texto": "SALIR"},
            {"nombre": "musica", "archivo": "Inicio/musica.png", "texto": "MÚSICA"},
            {"nombre": "television", "archivo": "Inicio/television.png", "texto": "TELEVISIÓN"},
            {"nombre": "dormir", "archivo": "Inicio/dormir.png", "texto": "DORMIR"},
            {"nombre": "libro", "archivo": "Inicio/libro.png", "texto": "LIBRO"},
        ]
        size = int(min(self.width, self.height) * 0.1)
        for item in iconos_info:
            self.iconos[item["nombre"]] = {
                "imagen": load_image(item["archivo"], (size, size), label=item["texto"][:2]),
                "texto": item["texto"],
            }

    def crear_cuadros(self):
        margin_x = int(self.width * 0.02)
        margin_y = int(self.height * 0.02)
        columns = 3
        rows = 2
        box_w = (self.width - (columns + 1) * margin_x) // columns
        box_h = (self.height - (rows + 1) * margin_y) // rows
        colors = [
            (255, 200, 200),
            (200, 255, 200),
            (200, 200, 255),
            (255, 255, 200),
            (255, 200, 255),
            (200, 255, 255),
        ]
        titles = ["SOCIALES", "NECESIDADES", "EMOCIONES", "CONTROL", "PERSONAS", "ACTIVIDADES"]
        boxes = []
        for row in range(rows):
            for col in range(columns):
                index = row * columns + col
                boxes.append({
                    "rect": pygame.Rect(margin_x + col * (box_w + margin_x), margin_y + row * (box_h + margin_y), box_w, box_h),
                    "color": colors[index],
                    "titulo": titles[index],
                })
        return boxes

    def crear_botones_comunicacion(self):
        categorias = [
            ["hola", "adios", "gracias", "porfavor", "si", "no"],
            ["hambre", "incomodo", "bano", "sed", "cansado", "dolor"],
            ["feliz", "triste", "enojado", "miedo", "nervioso", "calma"],
            ["ayuda", "no-quiero", "mas", "quiero", "basta", "espera"],
            ["mama", "enfermera", "hermano", "papa", "maestra", "amigo"],
            ["jugar-act", "salir-act", "musica", "television", "dormir", "libro"],
        ]
        buttons = []
        for box, names in zip(self.cuadros, categorias):
            cell_w = box["rect"].width // 3
            cell_h = (box["rect"].height - 70) // 2
            for index, name in enumerate(names):
                row = index // 3
                col = index % 3
                icon_size = min(cell_w - 30, cell_h - 40)
                rect = pygame.Rect(box["rect"].x + col * cell_w + (cell_w - icon_size) // 2, box["rect"].y + 50 + row * cell_h, icon_size, icon_size)
                buttons.append({
                    "rect": rect,
                    "icono": name,
                    "texto": self.iconos[name]["texto"],
                    "texto_pos": (rect.centerx, rect.bottom + 18),
                })
        return buttons

    def dibujar_cuadro(self, cuadro):
        pygame.draw.rect(self.screen, cuadro["color"], cuadro["rect"], border_radius=20)
        pygame.draw.rect(self.screen, AZUL, cuadro["rect"], width=3, border_radius=20)
        title = FUENTE.render(cuadro["titulo"], True, NEGRO)
        self.screen.blit(title, title.get_rect(center=(cuadro["rect"].centerx, cuadro["rect"].y + 25)))

    def dibujar_boton_comunicacion(self, info, pos):
        rect = info["rect"]
        color = (200, 150, 100) if rect.collidepoint(pos) else (221, 162, 105)
        pygame.draw.rect(self.screen, color, rect, border_radius=15)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2, border_radius=15)
        icon_rect = self.iconos[info["icono"]]["imagen"].get_rect(center=rect.center)
        self.screen.blit(self.iconos[info["icono"]]["imagen"], icon_rect)
        text = FUENTE_MUY_PEQUENA.render(info["texto"], True, NEGRO)
        self.screen.blit(text, text.get_rect(center=info["texto_pos"]))

    def decir_texto(self, texto):
        self.tts_sistema.decir_texto(texto)

    def ejecutar(self):
        clock = pygame.time.Clock()
        while True:
            cursor_x, cursor_y, click = self.camara.obtener_posicion_y_clic()
            new_click = click and not self.control_clic
            self.control_clic = click
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "menu_principal"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "menu_principal"
            self.screen.fill(COLOR_FONDO)
            for cuadro in self.cuadros:
                self.dibujar_cuadro(cuadro)
            for button in self.botones_comunicacion:
                self.dibujar_boton_comunicacion(button, (cursor_x, cursor_y))
                if new_click and button["rect"].collidepoint((cursor_x, cursor_y)):
                    self.decir_texto(button["texto"])
            self.barra_inferior.actualizar_visibilidad((cursor_x, cursor_y))
            self.barra_inferior.dibujar(self.screen, (cursor_x, cursor_y))
            destino = self.barra_inferior.manejar_clic((cursor_x, cursor_y), new_click)
            if destino and destino != "inicio":
                log_action(f"inicio.navigate:{destino}")
            draw_cursor(self.screen, cursor_x, cursor_y)
            pygame.display.flip()
            clock.tick(30)


if __name__ == "__main__":
    Inicio().ejecutar()