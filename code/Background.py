import pygame as pg

from code.Entity import Entity
from code.Const import WIN_WIDTH, ENTITY_SPEED


class Background(Entity):

    def __init__(self, name: str, position: tuple, size: tuple):
        super().__init__(name, position)
        image = pg.image.load(f'asset/{name}.png').convert_alpha()
        resized_image = pg.transform.scale(image, size)
        self.surf = resized_image
        self.rect = self.surf.get_rect(topleft=position)

    def move(self):
        self.rect.centerx -= ENTITY_SPEED[self.name]
        if self.rect.right <= 0:
            self.rect.left = WIN_WIDTH
