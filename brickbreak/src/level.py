import json
import os

# Legend
#   _ = empty space,
#   w = white brick
#   b = blue brick

class LevelManager():
    def __init__(self, filename):
        self.levels = {}

        data = open(os.getcwd() + filename, 'r').read()
        self.levels = json.loads(data)

    def get_level_layout(self, level):
        print(level)
        level_str = str(level)
        if level_str in self.levels:
            return self.levels[level_str]
