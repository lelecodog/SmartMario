import pygame as pg

from code.Const import COLOR_WHITE, COLOR_BLACK


class Menu:

    def __init__(self, window):
        self.window = window
        self.surf = pg.image.load('./asset/menu.jpg')
        self.rect = self.surf.get_rect(left=0, top=0)

        # create dark overlay
        self.overlay = pg.Surface(self.surf.get_size())
        self.overlay.set_alpha(150)  # Transparency
        self.overlay.fill(COLOR_BLACK)

        # Text font
        self.title_font = pg.font.SysFont("Arial", 75)
        self.menu_font = pg.font.SysFont("Arial", 50)

        # Text rendering
        self.title_text = self.title_font.render("SMART  MARIO", True, COLOR_WHITE)
        self.new_text = self.menu_font.render("NEW GAME", True, COLOR_WHITE)
        self.score_text = self.menu_font.render("SCORE", True, COLOR_WHITE)
        self.exit_text = self.menu_font.render("EXIT", True, COLOR_WHITE)

    def run(self):
        pg.mixer_music.load('./asset/menu.mp3')
        pg.mixer_music.play(-1)

        while True:
            self.window.blit(source=self.surf, dest=self.rect)

            # Apply dark overlay
            self.window.blit(self.overlay, self.rect)

            # Text positioning
            title_rect = self.title_text.get_rect(center=(self.window.get_rect().centerx, 100))
            new_rect = self.new_text.get_rect(center=(self.window.get_rect().centerx, 500))
            score_rect = self.score_text.get_rect(center=(self.window.get_rect().centerx, 600))
            exit_rect = self.exit_text.get_rect(center=(self.window.get_rect().centerx, 700))

            # Draw on screen
            self.window.blit(self.title_text, title_rect)
            self.window.blit(self.new_text, new_rect)
            self.window.blit(self.score_text, score_rect)
            self.window.blit(self.exit_text, exit_rect)

            pg.display.flip()

            # Check for all events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()  # Close Window
                    quit()  # End Pygame


