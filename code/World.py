import pygame as pg

from datetime import datetime
from pygame import Surface, Rect
from pygame.font import Font

from code.Coin import Coin
from code.Const import COLOR_WHITE, WIN_WIDTH, COLOR_RED, COLOR_BLACK
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.Player import Player
from code.QuestionFactory import QuestionFactory
from code.Const import LEVEL_SETTINGS


def generate_questions_for_level(level_index):
    level = LEVEL_SETTINGS[level_index]
    return [
        QuestionFactory.generate_question(level["min"], level["max"], level["operations"])
        for _ in range(3)
    ]


def get_draw_priority(ent: Entity):
    if ent.name.startswith("world1_bg"):
        return 0  # background: drawn first
    elif ent.name == "coin":
        return 1  # coins: on the background
    elif ent.name == "enemy":
        return 2  # enemy
    else:
        return 3  # player, HUD, etc.


class World:

    def __init__(self, window, name, player: Player):
        self.pending_question_data = None
        self.next_coin_spawn_time = None
        self.game_over = False
        self.window = window
        self.name = name
        self.player = player
        self.entity_list: list[Entity] = []
        # Introductions
        self.show_intro = True
        self.intro_start_time = pg.time.get_ticks()
        self.intro_duration = 7000
        # entities
        self.entity_list.extend(EntityFactory.get_entity('world1_bg'))
        self.player_entity = EntityFactory.get_entity('player', player=player)
        self.entity_list.append(self.player_entity)
        self.entity_list.append(EntityFactory.get_entity('enemy'))
        # Levels
        self.current_level_index = 0
        self.current_question_index = 0
        self.questions_started = False
        self.questions = generate_questions_for_level(self.current_level_index)
        self.question_text = ""
        # Sounds
        self.right_sound = pg.mixer.Sound('./asset/right.mp3')
        self.wrong_sound = pg.mixer.Sound('./asset/wrong.mp3')
        # Time question
        self.next_question_timer = None
        self.game_ended = False

    def run(self):
        pg.mixer_music.load('./asset/world1.mp3')
        pg.mixer_music.play(-1)
        clock = pg.time.Clock()
        running = True
        while running:
            if self.game_ended:
                return
            clock.tick(60)
            self.window.fill((0, 0, 0))

            # Check if it's time to flip the coins
            if hasattr(self, "next_coin_spawn_time") and self.next_coin_spawn_time:
                if (
                        isinstance(self.next_coin_spawn_time, int) and
                        isinstance(self.pending_question_data, dict) and
                        pg.time.get_ticks() >= self.next_coin_spawn_time
                ):
                    self.spawn_coins_for_question(self.pending_question_data)
                    self.next_coin_spawn_time = None
                    self.pending_question_data = None

            sorted_entities = sorted(self.entity_list, key=get_draw_priority)
            for ent in sorted_entities:
                self.window.blit(ent.surf, ent.rect)

                if ent.name == "coin":
                    self.draw_coin_value(ent)

                if hasattr(ent, "update"):
                    status = ent.update(self.window)
                    if status == "dead":
                        return
                else:
                    ent.move()

            if not self.game_over and self.player.score <= 0:
                self.player_entity.die(self.window)
                return

            self.check_coin_collision()
            self.remove_offscreen_entities()

            # Checks if it is time to load the next question
            if self.next_question_timer:
                if pg.time.get_ticks() - self.next_question_timer >= 1000:
                    self.next_question_timer = None
                    self.load_next_question()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

            if self.current_level_index >= len(LEVEL_SETTINGS):
                return
            level_name = LEVEL_SETTINGS[self.current_level_index]["name"]
            self.world_text(50, f'{level_name}', COLOR_RED, (WIN_WIDTH // 2 - 110, 300))

            # Printed text

            self.world_text(80, f'Question: {self.question_text}', COLOR_WHITE, (190, 360))
            self.world_text(60, f"Score: {self.player.score}", COLOR_BLACK, (WIN_WIDTH // 2 - 120, 250))

            if self.show_intro:
                elapsed = pg.time.get_ticks() - self.intro_start_time
                if elapsed >= self.intro_duration:
                    self.show_intro = False

                    if not self.questions_started:
                        self.questions_started = True
                        self.load_next_question()
                else:
                    self.draw_intro_window()

            pg.display.flip()

    def world_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pg.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)

    def draw_intro_window(self):
        x = self.player_entity.rect.centerx - 150
        y = self.player_entity.rect.top - 150
        width = 400
        height = 120

        # Background box
        intro_rect = pg.Rect(x, y, width, height)
        pg.draw.rect(self.window, (0, 0, 0), intro_rect)
        pg.draw.rect(self.window, (255, 255, 255), intro_rect, 2)

        font = pg.font.SysFont("Lucida Sans Typewriter", 30)
        lines = [
            "Bem-vindo ao desafio!",
            "Pegue a moeda com a resposta certa.",
            "Evite as erradas ou perca pontos!",
            "Aperte Space para pular ",
            "setas para mover"
        ]
        for i, line in enumerate(lines):
            text_surf = font.render(line, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(x + width // 2, y + 20 + i * 20))
            self.window.blit(text_surf, text_rect)

    def draw_coin_value(self, coin):
        font = pg.font.SysFont("Lucida Sans Typewriter", 36)
        value_text = font.render(str(coin.value), True, (0, 0, 0))
        text_rect = value_text.get_rect(center=coin.rect.center)
        self.window.blit(value_text, text_rect)

    def check_coin_collision(self):
        removed_coins = False
        for entidade in self.entity_list[:]:
            if isinstance(entidade, Coin) and self.player_entity.rect.colliderect(entidade.rect):
                level_bonus = self.current_level_index + 1

                if entidade.is_correct:
                    self.right_sound.play()
                    self.player.add_score(level_bonus)
                else:
                    self.wrong_sound.play()
                    self.player.add_score(-level_bonus)

                self.entity_list.remove(entidade)
                removed_coins = True

        # heck if there are still coins
        if removed_coins and not any(isinstance(e, Coin) for e in self.entity_list):
            self.question_text = ""  # remove question
            if self.next_question_timer is None:
                self.next_question_timer = pg.time.get_ticks()

    # Remove coins that go off the screen
    def remove_offscreen_entities(self):
        removed_coins = False
        for e in self.entity_list[:]:
            if e.rect.right < 0:
                self.entity_list.remove(e)
                removed_coins = True

        if removed_coins and not any(isinstance(e, Coin) for e in self.entity_list):
            self.question_text = ""
            if self.next_question_timer is None:
                self.next_question_timer = pg.time.get_ticks()

    def spawn_coins_for_question(self, question_data: dict):
        self.question_text = question_data["question"]

        for i, value in enumerate(question_data["options"]):
            is_correct = value == question_data["correct"]
            position = (1130 + i * 700, 670)
            coin = EntityFactory.get_entity(
                'coin',
                position=position,
                size=(60, 60),
                value=value,
                is_correct=is_correct
            )
            self.entity_list.append(coin)

    def load_next_question(self):
        if self.current_question_index >= len(self.questions):
            self.current_level_index += 1
            self.current_question_index = 0

            if self.current_level_index >= len(LEVEL_SETTINGS):
                self.end_game()
                return

            self.questions = generate_questions_for_level(self.current_level_index)

        self.pending_question_data = self.questions[self.current_question_index]
        self.question_text = self.pending_question_data["question"]
        self.next_coin_spawn_time = pg.time.get_ticks() + 1000

        self.questions_started = True
        self.current_question_index += 1

    def end_game(self):
        self.game_ended = True
        self.player_entity.show_victory_screen(self.window)
        self.player.save(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        pg.time.set_timer(pg.USEREVENT + 1, 5000)
