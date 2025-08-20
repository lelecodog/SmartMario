from code.Entity import Entity


class Level:

    def __init__(self, window, name, player):
        self.window = window
        self.name = name
        self.player = player
        self.entity_list: list[Entity] = []

    def run(self):
        pass
