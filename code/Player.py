import json
import os
from datetime import datetime


SCORE_FILE = "score.json"


def player_list():
    if not os.path.exists(SCORE_FILE):
        return []
    with open(SCORE_FILE, 'r') as f:
        data = json.load(f)
    return list(data.keys())


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
        return f"Player: {self.name} | Score: {self.score} | World unlocked: {self.unlocked_worlds}"

    def save(self, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open("score.json", "r") as f:
                all_data = json.load(f)
            if not isinstance(all_data, list):
                all_data = []
        except (FileNotFoundError, json.JSONDecodeError):
            all_data = []

        # Updates or adds the current player
        all_data.append({
            'name': self.name,
            'score': self.score,
            'unlocked_worlds': self.unlocked_worlds,
            'last_played': timestamp
        })

        # Save
        with open(SCORE_FILE, 'w') as f:
            json.dump(all_data, f, indent=4)

    @staticmethod
    def load(name):
        if not os.path.exists(SCORE_FILE):
            return None

        with open(SCORE_FILE, 'r') as f:
            all_data = json.load(f)

        if name not in all_data:
            return None

        data = all_data[name]
        player = Player(name)
        player.score = data['score']
        player.unlocked_worlds = data['unlocked_worlds']
        player.last_played = data.get('last_played', 'N/A')
        return player
