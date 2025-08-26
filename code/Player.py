import json, os


def player_list():
    return [f[:-5] for f in os.listdir() if f.endswith('.json')]


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 10
        self.unlocked_worlds = ['world1']  # Start with first world unlocked

    def add_score(self, points):
        self.score += points

    def unlock_world(self, level_name):
        if level_name not in self.unlocked_worlds:
            self.unlocked_worlds.append(level_name)

    def __str__(self):
        return f"Jogador: {self.name} | Score: {self.score} | Níveis desbloqueados: {self.unlocked_worlds}"

    def save(self):
        data = {
            'name': self.name,
            'score': self.score,
            'unlocked_worlds': self.unlocked_worlds
        }
        with open(f'{self.name}.json', 'w') as f:
            json.dump(data, f)

    @staticmethod
    def load(name):
        try:
            with open(f'{name}.json', 'r') as f:
                data = json.load(f)
                player = Player(data['name'])
                player.score = data['score']
                player.unlocked_worlds = data['unlocked_worlds']
                return player
        except FileNotFoundError:
            return None

