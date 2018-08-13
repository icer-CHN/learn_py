class GameStats():
    '''跟踪游戏的统计信息'''

    def __init__(self, settings):
        self.settings = settings
        self.game_active = False
        self.reset_stats()
        self.high_score = 0

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
