import json


class GameStats():
    '''跟踪游戏的统计信息'''

    def __init__(self, settings):
        self.settings = settings
        self.game_active = False
        self.reset_stats()
        self.high_score = self.load_high_score()

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def load_high_score(self):
        filename = 'high_score.json'
        try:
            with open(filename) as f:
                score = json.load(f)
        except FileNotFoundError:
            return 0
        else:
            if score:
                return score
            else:
                return 0
