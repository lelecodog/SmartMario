import pygame as pg

from code.Const import ENTITY_SPEED
from code.Entity import Entity


class Coin(Entity):
    def __init__(self, name: str, value, is_correct, position, size):
        super().__init__(name, position)

        imagem = pg.image.load(f'asset/{name}.png').convert_alpha()
        # Redimensiona a imagem
        imagem_redimensionada = pg.transform.scale(imagem, size)

        self.value = value
        self.is_correct = is_correct
        self.surf = imagem_redimensionada
        self.rect = self.surf.get_rect(topleft=position)

    def move(self):
        self.rect.x -= ENTITY_SPEED[self.name]

