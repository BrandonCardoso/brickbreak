class GameState():
    TITLE = 0
    INGAME = 1
    PAUSED = 2
    GAMEOVER = 3
    CLEARED = 4

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
        self.enter_callbacks = {}
        self.exit_callbacks = {}

    def get_state(self):
        return self.state

    def set_state(self, to_state, from_state = None):
        self.on_exit(from_state if from_state else self.state)
        self.state = to_state
        self.on_enter(to_state)

    def _add_to_list(self, list, state, obj):
        if not state in list:
            list[state] = []

        if not obj in list[state]:
            list[state].append(obj)

    def _remove_from_list(self, list, state, obj):
        if state in list:
            if obj in list[state]:
                list[state].remove(obj)

    def add_relation(self, relation):
        self._add_to_list(self.relations, relation.initial_state, relation)

    def remove_relation(self, relation):
        self._remove_from_list(self.relations, relation.initial_state, relation)

    def add_enter_callback(self, state, callback):
        self._add_to_list(self.enter_callbacks, state, callback)

    def remove_enter_callback(self, state, callback):
        self._remove_from_list(self.enter_callbacks, state, callback)

    def add_exit_callback(self, state, callback):
        self._add_to_list(self.exit_callbacks, state, callback)

    def remove_exit_callback(self, state, callback):
        self._remove_from_list(self.exit_callbacks, state, callback)

    def on_enter(self, state):
        if state in self.enter_callbacks:
            for callback in self.enter_callbacks[state]:
                callback()

    def on_exit(self, state):
        if state in self.exit_callbacks:
            for callback in self.exit_callbacks[state]:
                callback()

    def handle_key(self, key, mod):
        current_state = self.get_state()
        for relation in self.relations[current_state]:
            if (not relation.key or key == relation.key) and (not relation.mod or mod == relation.mod):
                self.set_state(relation.end_state, relation.initial_state)
