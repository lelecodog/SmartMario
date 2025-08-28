import pygame as pg

from code.Entity import Entity


class Enemy(Entity):
    def __init__(self, name: str, position: tuple, size: tuple):
        super().__init__(name, position)

        image = pg.image.load(f'asset/{name}.png').convert_alpha()
        resized_image = pg.transform.scale(image, size)

        self.surf = resized_image
        self.rect = self.surf.get_rect()
        self.rect.bottomleft = position

    def move(self):
        pass
