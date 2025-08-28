import pygame as pg

from code.Const import WIN_WIDTH, WIN_HEIGHT
from code.Score import Score
from code.World import World
from code.Menu import Menu
from code.Player import Player
from code.PlayerSelector import PlayerSelector


def select_player():
    name = input("Enter the player's name: ")
    player = Player.load(name)
    if not player:
        player = Player(name)
    return player


class Game:
    def __init__(self):
        # setup
        pg.init()
        self.window = pg.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        self.options = ["NEW GAME", "SCORE", "EXIT"]

    def run(self, ):
        while True:
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return == self.options[0]:  # "NEW GAME"
                selector = PlayerSelector(self.window)
                player = selector.run()
                pg.mixer_music.stop()
                world = World(self.window, 'world1', player)
                world.run()

            elif menu_return == self.options[1]:  # "SCORE"
                score_screen = Score(self.window)
                score_screen.run()

            else:  # "EXIT"
                pg.quit()
                quit()
