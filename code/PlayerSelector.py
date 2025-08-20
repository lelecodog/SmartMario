import pygame as pg
import os
import json
from code.Const import COLOR_WHITE, COLOR_BLACK, COLOR_YELLOW
from code.Level import Level
from code.Player import Player


def list_saved_players():
    try:
        return [f.replace('.json', '') for f in os.listdir('players') if f.endswith('.json')]
    except FileNotFoundError:
        return []


class PlayerSelector:
    def __init__(self, window):
        self.window = window
        self.surf = pg.image.load('./asset/menu.jpg')
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
        self.players = list_saved_players()
        self.selected_index = -1

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
            pg.draw.rect(self.window, COLOR_WHITE, self.input_box, 2)
            input_surface = self.input_font.render(self.input_text, True, COLOR_WHITE)
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
                    if self.input_active:
                        if event.key == pg.K_RETURN:
                            name = self.input_text.strip()
                            if name:
                                player = Player.load(name)
                                if not player:
                                    player = Player(name)
                                    print(f"Novo jogador '{name}' criado!")
                                return player
                        elif event.key == pg.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            self.input_text += event.unicode
                    else:
                        if event.key == pg.K_RETURN and self.selected_index >= 0:
                            name = self.players[self.selected_index]
                            player = Player.load(name)
                            return player

            clock.tick(30)




