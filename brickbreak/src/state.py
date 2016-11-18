class GameState():
    TITLE = 0
    INGAME = 1
    PAUSED = 2

class GameStateRelation():
    def __init__(self, name, initial_state, end_state, key = None, mod = None):
        self.name = name
        self.initial_state = initial_state
        self.end_state = end_state
        self.key = key
        self.mod = mod

class GameStateManager():
    def __init__(self, initial_state):
        self.state = initial_state
        self.relations = {}

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def add_relation(self, relation):
        if not relation.initial_state in self.relations:
            self.relations[relation.initial_state] = []

        if not relation in self.relations[relation.initial_state]:
           self.relations[relation.initial_state].append(relation)

    def remove_relation(self, relation):
        if relation.initial_state in self.relations:
            if relation in self.relations[relation.initial_state]:
                self.relations[relation.initial_state].remove(relation)

    def handle_key(self, key, mod):
        current_state = self.get_state()
        for relation in self.relations[current_state]:
            if (not relation.key or key == relation.key) and (not relation.mod or mod == relation.mod):
                self.set_state(relation.end_state)