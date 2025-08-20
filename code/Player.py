import json


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.unlocked_levels = ['level1']  # Start with first level unlocked

    def add_score(self, points):
        self.score += points

    def unlock_level(self, level_name):
        if level_name not in self.unlocked_levels:
            self.unlocked_levels.append(level_name)

    def __str__(self):
        return f"Jogador: {self.name} | Score: {self.score} | Níveis desbloqueados: {self.unlocked_levels}"

    def save(self):
        data = {
            'name': self.name,
            'score': self.score,
            'unlocked_levels': self.unlocked_levels
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
                player.unlocked_levels = data['unlocked_levels']
                return player
        except FileNotFoundError:
            return None

