from code.Background import Background
from code.Const import WIN_WIDTH


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0)):
        match entity_name:
            case 'world1_bg':
                list_bg = []
                for i in range(2):
                    list_bg.append(Background(f'world1_bg0{i+1}', (0, 0)))
                    list_bg.append(Background(f'world1_bg0{i + 1}', (WIN_WIDTH, 0)))
                return list_bg
            case _:
                print(f"[ERRO] Entidade '{entity_name}' não encontrada.")
                return []
