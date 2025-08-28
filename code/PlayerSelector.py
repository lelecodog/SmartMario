import pygame as pg
import json
from code.Const import COLOR_WHITE, COLOR_BLACK, COLOR_YELLOW
from code.Player import Player


def list_saved_players():
    try:
        with open("score.json", "r") as f:
            data = json.load(f)
        return list(set(entry["name"] for entry in data))
    except (FileNotFoundError, json.JSONDecodeError):
        return []


class PlayerSelector:
    def __init__(self, window):
        self.window = window
        self.surf = pg.image.load('./asset/menu.jpg').convert()
        self.rect = self.surf.get_rect(left=0, top=0)

        # Dark overlay
        self.overlay = pg.Surface(self.surf.get_size())
        self.overlay.set_alpha(150)
        self.overlay.fill(COLOR_BLACK)

        # Font
        self.title_font = pg.font.SysFont("Arial", 70)
        self.menu_font = pg.font.SysFont("Arial", 40)
        self.input_font = pg.font.SysFont("Arial", 30)

        # Text
        self.input_box = pg.Rect(200, 150, 400, 40)
        self.input_text = ""
        self.input_active = False

        # Players list
        self.players = ["<ENTER NAME!>"] + list_saved_players()
        self.selected_index = 0
        self.input_active = True

    def run(self):
        pg.mixer_music.load('./asset/menu.mp3')
        pg.mixer_music.play(-1)
        clock = pg.time.Clock()

        while True:
            self.window.blit(self.surf, self.rect)
            self.window.blit(self.overlay, self.rect)

            # Títle
            title_text = self.title_font.render("SELECT PLAYER", True, COLOR_YELLOW)
            title_rect = title_text.get_rect(center=(self.window.get_rect().centerx, 80))
            self.window.blit(title_text, title_rect)

            # Text camp
            if self.selected_index == 0:
                border_color = COLOR_YELLOW
                cursor = "|" if pg.time.get_ticks() // 500 % 2 == 0 else ""  # flashes every 500ms
                input_surface = self.input_font.render(self.input_text + cursor, True, COLOR_WHITE)
            else:
                border_color = COLOR_WHITE
                input_surface = self.input_font.render(self.input_text, True, COLOR_WHITE)

            pg.draw.rect(self.window, border_color, self.input_box, 2)
            self.window.blit(input_surface, (self.input_box.x + 10, self.input_box.y + 5))

            # Player list
            for i, name in enumerate(self.players):
                color = COLOR_YELLOW if i == self.selected_index else COLOR_WHITE
                text = self.menu_font.render(name, True, color)
                text_rect = text.get_rect(topleft=(220, 220 + i * 50))
                self.window.blit(text, text_rect)

                # Mouse hover
                if text_rect.collidepoint(pg.mouse.get_pos()):
                    self.selected_index = i

            pg.display.flip()

            # Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(event.pos):
                        self.input_active = True
                    else:
                        self.input_active = False
                    # Click in salve player
                    for i, name in enumerate(self.players):
                        rect = pg.Rect(220, 220 + i * 50, 300, 40)
                        if rect.collidepoint(event.pos):
                            self.input_text = name
                            self.selected_index = i
                            pg.mixer.Sound('./asset/select-option.mp3').play()
                elif event.type == pg.KEYDOWN:
                    if self.selected_index == 0:
                        self.input_active = True
                        if event.key == pg.K_RETURN:
                            name = self.input_text.strip()
                            if name:
                                player = Player(name)
                                return player
                        elif event.key == pg.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        elif event.key == pg.K_DOWN:
                            if len(self.players) > 1:
                                self.selected_index = 1
                                self.input_active = False
                                self.input_text = self.players[self.selected_index]
                                pg.mixer.Sound('./asset/select-option.mp3').play()
                        else:
                            self.input_text += event.unicode
                    else:
                        self.input_active = False
                        if event.key == pg.K_UP:
                            self.selected_index -= 1
                            if self.selected_index < 0:
                                self.selected_index = 0
                            self.input_active = self.selected_index == 0
                            self.input_text = "" if self.input_active else self.players[self.selected_index]
                            pg.mixer.Sound('./asset/select-option.mp3').play()
                        elif event.key == pg.K_DOWN:
                            self.selected_index += 1
                            if self.selected_index >= len(self.players):
                                self.selected_index = len(self.players) - 1
                            self.input_active = self.selected_index == 0
                            self.input_text = "" if self.input_active else self.players[self.selected_index]
                            pg.mixer.Sound('./asset/select-option.mp3').play()
                        elif event.key == pg.K_RETURN:
                            name = self.players[self.selected_index]
                            player = Player(name)
                            return player

            clock.tick(30)
