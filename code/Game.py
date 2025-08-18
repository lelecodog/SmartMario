import pygame as pg

from code.Menu import Menu


class Game:
    def __init__(self):
        # setup
        pg.init()
        self.window = pg.display.set_mode(size=(1200, 850))

    def run(self, ):
        while True:
            menu = Menu(self.window)
            menu.run()
            pass

            # Check for all events
            #for event in pg.event.get():
               # if event.type == pg.QUIT:
                   # pg.quit()  # Close Window
                   # quit()  # End Pygame
