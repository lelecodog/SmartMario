from code.Background import Background
from code.Const import WIN_WIDTH
from code.PlayerEntity import PlayerEntity


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0), size=(128, 158)):
        match entity_name:
            case 'world1_bg':
                list_bg = []
                for i in range(1, 4):
                    name = f'world1_bg0{i}'
                    # Define a altura personalizada
                    if name == 'world1_bg03':
                        y = -180  # valor negativo sobe a imagem
                    elif name == 'world1_bg02':
                        y = -150
                    else:
                        y = 0
                    list_bg.append(Background(name, (0, y)))
                    list_bg.append(Background(name, (WIN_WIDTH, y)))
                return list_bg
            case 'Player':
                return PlayerEntity('Player', (10, 650), (128, 158))

