class Player:
    def __init__(self, name):
        self.name = name
        self.team = []
        self.pc = []

    def add_pokemon(self, pokemon):
        if self.team < 6:
            self.team.append(pokemon)
        else:
            self.pc.append(pokemon)

    def team_is_alive(self):
        for pokemon in self.team:
            if pokemon.is_alive():
                return True
        return False
