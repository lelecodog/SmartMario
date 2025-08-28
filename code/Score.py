import pygame as pg
import json

from code.Const import COLOR_BLACK, COLOR_YELLOW, COLOR_WHITE, COLOR_LIGHT_BLUE


def load_top_players():
    try:
        with open("score.json", "r") as f:
            data = json.load(f)
        # Order by crescent
        sorted_data = sorted(data, key=lambda x: x.get("score", 0), reverse=True)
        return sorted_data[:10]  # top 10
    except (FileNotFoundError, json.JSONDecodeError):
        return []


class Score:
    def __init__(self, window):
        self.window = window
        self.surf = pg.image.load('./asset/menu.jpg').convert()
        self.rect = self.surf.get_rect(left=0, top=0)

        # Dark overlay
        self.overlay = pg.Surface(self.surf.get_size())
        self.overlay.set_alpha(150)
        self.overlay.fill(COLOR_BLACK)

        self.players = load_top_players()
        self.title_font = pg.font.SysFont("Arial", 60)
        self.score_font = pg.font.SysFont("Arial", 40)
        self.back_rect = pg.Rect(50, 650, 200, 50)
        self.back_font = pg.font.SysFont("Arial", 40)

    def run(self):
        pg.mixer_music.load('./asset/menu.mp3')
        pg.mixer_music.play(-1)
        clock = pg.time.Clock()

        while True:
            self.window.blit(self.surf, self.rect)
            self.window.blit(self.overlay, self.rect)

            # Title
            title_text = self.title_font.render("TOP 10 SCORES", True, COLOR_YELLOW)
            title_rect = title_text.get_rect(center=(self.window.get_width() // 2, 80))
            self.window.blit(title_text, title_rect)

            # Players list
            for i, entry in enumerate(self.players):
                name = entry.get("name", "???")
                score = entry.get("score", 0)
                date = entry.get("last_played", "")
                text = f"{i + 1}. {name}  -  {score} pts  -  {date}"
                # intersperse color
                color = COLOR_WHITE if i % 2 == 0 else COLOR_LIGHT_BLUE
                text_surface = self.score_font.render(text, True, color)
                self.window.blit(text_surface, (350, 250 + i * 50))

            # Back button
            pg.draw.rect(self.window, COLOR_YELLOW, self.back_rect, 2)
            back_text = self.back_font.render("< BACK >", True, COLOR_YELLOW)
            self.window.blit(back_text, (self.back_rect.x + 10, self.back_rect.y + 5))

            pg.display.flip()

            # Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.back_rect.collidepoint(event.pos):
                        return  # return menu
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE or event.key == pg.K_RETURN:
                        return  # return menu

            clock.tick(30)
