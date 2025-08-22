import pygame as pg
import sys


from pygame import Surface, Rect
from pygame.font import Font

from code.Const import COLOR_WHITE, WIN_HEIGHT
from code.Entity import Entity
from code.EntityFactory import EntityFactory


class World:

    def __init__(self, window, name, player):
        self.window = window
        self.name = name
        self.player = player
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('world1_bg'))
        self.entity_list.append(EntityFactory.get_entity('Player'))
        self.timeout = 20000  # seconds

    def run(self):
        pg.mixer_music.load('./asset/world1.mp3')
        pg.mixer_music.play(-1)
        clock = pg.time.Clock()
        running = True
        while running:
            clock.tick(60)
            self.window.fill((0, 0, 0))  # Limpa a tela

            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect)
                # Se a entidade for o jogador, chama update()
                if hasattr(ent, "update"):
                    ent.update()
                else:
                    ent.move()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

            # Printed text
            self.world_text(20, f'{self.name} - Timeout: {self.timeout / 1000 :.1f}s', COLOR_WHITE, (10, 5))
            self.world_text(20, f'fps: {clock.get_fps() :.0f}', COLOR_WHITE, (10, WIN_HEIGHT - 35))
            self.world_text(20, f'entidades: {len(self.entity_list)}', COLOR_WHITE, (10, WIN_HEIGHT - 20))
            pg.display.flip()

    def world_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pg.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)
