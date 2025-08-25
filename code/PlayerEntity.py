import sys

import pygame as pg

from code.Const import ENTITY_SPEED, WIN_HEIGHT
from code.Entity import Entity


class PlayerEntity(Entity):

    def __init__(self, name: str, position: tuple, size: tuple):
        super().__init__(name, position)

        imagem = pg.image.load(f'asset/{name}.png').convert_alpha()

        # Redimensiona a imagem
        imagem_redimensionada = pg.transform.scale(imagem, size)

        self.surf = imagem_redimensionada
        self.rect = self.surf.get_rect()
        self.rect.bottomleft = position
        self.caindo_no_buraco = False
        self.velocidade_queda = 5
        self.is_jumping = False
        self.jump_speed = -20
        self.gravity = 1
        self.vertical_speed = 0
        self.buraco_inicio = 540
        self.buraco_fim = 800
        self.chao_y = 750

    def move(self):
        pressed_key = pg.key.get_pressed()
        if pressed_key[pg.K_RIGHT]:
            self.rect.x += ENTITY_SPEED[self.name]
        self.check_fall()
        if pressed_key[pg.K_LEFT] and self.rect.left > 0:
            self.rect.x -= ENTITY_SPEED[self.name]
        if pressed_key[pg.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.vertical_speed = self.jump_speed

    def check_fall(self):
        if self.buraco_inicio < self.rect.centerx < self.buraco_fim and self.rect.bottom >= self.chao_y:
            print("💀 O jogador caiu no buraco!")
            self.caindo_no_buraco = True  # ativa a queda

    def morrer(self):
        # Aqui você pode definir o que acontece quando o jogador morre
        print("Game Over")
        pg.quit()
        sys.exit()

    def update(self):
        if self.caindo_no_buraco:
            self.rect.y += self.velocidade_queda
            self.velocidade_queda += 1  # acelera a queda (gravidade)

            if self.rect.top > WIN_HEIGHT:  # saiu da tela
                self.morrer()
        else:
            self.move()
            # Aplica movimento vertical do pulo
            if self.is_jumping:
                self.rect.y += self.vertical_speed
                self.vertical_speed += self.gravity

                # Simula aterrissagem (ajuste conforme seu chão)
                if self.rect.bottom >= self.chao_y and self.vertical_speed > 0:  # altura do chão
                    self.rect.bottom = self.chao_y
                    self.is_jumping = False
                    self.vertical_speed = 0

