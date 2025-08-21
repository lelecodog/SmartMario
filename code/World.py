import pygame as pg

from code.Entity import Entity
from code.EntityFactory import EntityFactory


class World:

    def __init__(self, window, name, player):
        self.window = window
        self.name = name
        self.player = player
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('world1_bg'))

    def run(self):
        running = True
        while running:
            self.window.fill((0, 0, 0))  # Limpa a tela

            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect)
                ent.move()
            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False


