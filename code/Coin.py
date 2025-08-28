import pygame as pg

from code.Const import ENTITY_SPEED
from code.Entity import Entity


class Coin(Entity):
    def __init__(self, name: str, value, is_correct, position, size):
        super().__init__(name, position)

        image = pg.image.load(f'asset/{name}.png').convert_alpha()
        resized_image = pg.transform.scale(image, size)

        self.value = value
        self.is_correct = is_correct
        self.surf = resized_image
        self.rect = self.surf.get_rect(topleft=position)

    def move(self):
        self.rect.x -= ENTITY_SPEED[self.name]
