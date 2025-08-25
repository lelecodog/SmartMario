from code.Background import Background
from code.Coin import Coin
from code.Const import WIN_WIDTH, WIN_HEIGHT
from code.Enemy import Enemy
from code.PlayerEntity import PlayerEntity


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0), size=(WIN_WIDTH, WIN_HEIGHT), is_correct=False, value=None):
        default_size = size
        match entity_name:
            case 'world1_bg':
                list_bg = []
                for i in range(1, 4):
                    name = f'world1_bg0{i}'
                    # Define a altura personalizada
                    if name == 'world1_bg03':
                        y = -160  # valor negativo sobe a imagem
                    elif name == 'world1_bg02':
                        y = -130
                    else:
                        y = 0

                    # Tamanho personalizado apenas para world1_bg01
                    if name == 'world1_bg01':
                        size = (WIN_WIDTH, WIN_HEIGHT)
                    else:
                        size = default_size

                    list_bg.append(Background(name, (0, y), size))
                    list_bg.append(Background(name, (WIN_WIDTH, y), size))
                return list_bg
            case 'player':
                return PlayerEntity('player', (10, 750), (128, 158))
            case 'enemy':
                return Enemy('enemy', (1010, 750), (128, 158))
            case 'coin':
                return Coin('coin', value, is_correct, position, size)
            








