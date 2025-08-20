import pygame as pg

from code.Const import COLOR_WHITE, COLOR_BLACK, COLOR_YELLOW


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
        self.title_font = pg.font.SysFont("Arial", 80)
        self.menu_font = pg.font.SysFont("Arial", 40)

        self.selected_option = 0
        self.options = ["NEW GAME", "SCORE", "EXIT"]

    def run(self):
        pg.mixer_music.load('./asset/menu.mp3')
        pg.mixer_music.play(-1)

        while True:
            self.window.blit(source=self.surf, dest=self.rect)

            # Apply dark overlay
            self.window.blit(self.overlay, self.rect)

            # Render title
            title_text = self.title_font.render("SMART  MARIO", True, COLOR_YELLOW)
            title_rect = title_text.get_rect(center=(self.window.get_rect().centerx, 100))
            self.window.blit(title_text, title_rect)

            # Render menu options with dynamic color
            for i, option in enumerate(self.options):
                color = COLOR_YELLOW if i == self.selected_option else COLOR_WHITE
                text = self.menu_font.render(option, True, color)
                text_rect = text.get_rect(center=(self.window.get_width() // 2, 400 + i * 100))
                self.window.blit(text, text_rect)

                # Detect if mouse is hovering over the text
                if text_rect.collidepoint(pg.mouse.get_pos()):
                    color = COLOR_YELLOW
                    self.selected_option = i  # Actualize option with mouse
                else:
                    color = COLOR_WHITE

            pg.display.flip()

            # Check for all events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()  # Close Window
                    quit()  # End Pygame

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % 3
                        pg.mixer.Sound('./asset/select-option.mp3').play()
                    elif event.key == pg.K_UP:
                        self.selected_option = (self.selected_option - 1) % 3
                        pg.mixer.Sound('./asset/select-option.mp3').play()
                    elif event.key == pg.K_RETURN:  # Enter
                        return self.options[self.selected_option]
