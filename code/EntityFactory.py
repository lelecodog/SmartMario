from code.Background import Background
from code.Coin import Coin
from code.Const import WIN_WIDTH, WIN_HEIGHT
from code.Enemy import Enemy
from code.PlayerEntity import PlayerEntity


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0), size=(WIN_WIDTH, WIN_HEIGHT), is_correct=False,
                   value=None, player=None):
        default_size = size
        match entity_name:
            case 'world1_bg':
                list_bg = []
                for i in range(1, 4):
                    name = f'world1_bg0{i}'
                    # Set custom height
                    if name == 'world1_bg03':
                        y = -160
                    elif name == 'world1_bg02':
                        y = -130
                    else:
                        y = 0

                    if name == 'world1_bg01':
                        size = (WIN_WIDTH, WIN_HEIGHT)
                    else:
                        size = default_size

                    list_bg.append(Background(name, (0, y), size))
                    list_bg.append(Background(name, (WIN_WIDTH, y), size))
                return list_bg
            case 'player':
                if player is None:
                    raise ValueError("The 'player' parameter is required to create PlayerEntity.")
                return PlayerEntity(player, 'player', (100, 750), (128, 158))
            case 'enemy':
                return Enemy('enemy', (1160, 753), (128, 158))
            case 'coin':
                return Coin('coin', value, is_correct, position, size)
            case _:
                raise ValueError(f"Unknown entity: {entity_name}")
