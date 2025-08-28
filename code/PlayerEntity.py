import sys
import time
import pygame as pg

from code.Const import ENTITY_SPEED, WIN_HEIGHT, COLOR_RED, COLOR_WHITE
from code.Entity import Entity
from code.Player import Player


class PlayerEntity(Entity):

    def __init__(self, player: Player, name: str, position: tuple, size: tuple):
        super().__init__(name, position)

        imagem = pg.image.load(f'asset/{name}.png').convert_alpha()

        # Redimensiona a imagem
        imagem_redimensionada = pg.transform.scale(imagem, size)

        self.player = player
        self.surf = imagem_redimensionada
        self.rect = self.surf.get_rect()
        self.rect.bottomleft = position
        self.caindo_no_buraco = False
        self.velocidade_queda = 5
        self.is_jumping = False
        self.jump_speed = -18
        self.gravity = 0.8
        self.vertical_speed = 0
        self.buraco_inicio = 540
        self.buraco_fim = 800
        self.chao_y = 750
        self.jump_sound = pg.mixer.Sound('./asset/jump-up.mp3')
        self.game_over_sound = pg.mixer.Sound('./asset/game-over.mp3')
        self.win_sound = pg.mixer.Sound('./asset/win.mp3')
        self.space_pressed_last_frame = False

    def move(self):
        pressed_key = pg.key.get_pressed()
        click_key = pg.key.get_pressed()[pg.K_SPACE] and not self.space_pressed_last_frame
        if pressed_key[pg.K_RIGHT]:
            self.rect.x += ENTITY_SPEED[self.name]

        if pressed_key[pg.K_LEFT] and self.rect.left > 0:
            self.rect.x -= ENTITY_SPEED[self.name]
        self.check_fall()

        if click_key and not self.is_jumping:
            self.is_jumping = True
            self.jump_sound.play()
            self.vertical_speed = self.jump_speed
        self.space_pressed_last_frame = pressed_key[pg.K_SPACE]

    def die(self, screen):
        pg.mixer_music.stop()
        self.game_over_sound.play()

        screen.fill((0, 0, 0))

        font = pg.font.SysFont("Arial", 100)
        text = font.render("GAME OVER!", True, COLOR_RED)
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)

        pg.display.flip()

        pg.time.delay(5000)
        pg.mixer.stop()
        return

    def show_victory_screen(self, screen):
        pg.mixer_music.stop()
        self.win_sound.play()

        screen.fill((0, 0, 0))

        font = pg.font.SysFont("Arial", 60)
        small_font = pg.font.SysFont("Arial", 40)
        text = font.render("CONGRATULATIONS", True, COLOR_WHITE)
        score_text = small_font.render(f"YOUR SCORE: {self.player.score}", True, COLOR_WHITE)
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 200))
        screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 300))

        pg.display.flip()

        pg.time.delay(5000)
        pg.mixer.stop()
        return

    def check_fall(self):
        if self.buraco_inicio < self.rect.centerx < self.buraco_fim and self.rect.bottom >= self.chao_y:
            print("💀 O jogador caiu no buraco!")
            self.caindo_no_buraco = True  # ativa a queda

    def update(self, screen):
        if self.caindo_no_buraco:
            self.rect.y += self.velocidade_queda
            self.velocidade_queda += 1  # acelera a queda (gravidade)

            if self.rect.top > WIN_HEIGHT:  # saiu da tela
                self.die(screen)
                return "dead"
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
        return "alive"
