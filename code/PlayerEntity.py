import pygame as pg

from code.Const import ENTITY_SPEED, WIN_HEIGHT, COLOR_RED, COLOR_WHITE
from code.Entity import Entity
from code.Player import Player


class PlayerEntity(Entity):

    def __init__(self, player: Player, name: str, position: tuple, size: tuple):
        super().__init__(name, position)

        image = pg.image.load(f'asset/{name}.png').convert_alpha()
        resized_image = pg.transform.scale(image, size)

        self.player = player
        self.surf = resized_image
        self.rect = self.surf.get_rect()
        self.rect.bottomleft = position
        self.fall = False
        self.fall_speed = 5
        self.is_jumping = False
        self.jump_speed = -18
        self.gravity = 0.8
        self.vertical_speed = 0
        self.hole_start = 540
        self.hole_end = 800
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
        if self.hole_start < self.rect.centerx < self.hole_end and self.rect.bottom >= self.chao_y:
            self.fall = True

    def update(self, screen):
        if self.fall:
            self.rect.y += self.fall_speed
            self.fall_speed += 1

            if self.rect.top > WIN_HEIGHT:
                self.die(screen)
                return "dead"
        else:
            self.move()
            # Applies vertical jump movement
            if self.is_jumping:
                self.rect.y += self.vertical_speed
                self.vertical_speed += self.gravity

                # Simulates landing
                if self.rect.bottom >= self.chao_y and self.vertical_speed > 0:
                    self.rect.bottom = self.chao_y
                    self.is_jumping = False
                    self.vertical_speed = 0
        return "alive"
