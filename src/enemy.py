from pokemon import Pokemon

class Enemy:
    def __init__(self, name, random_num_pokemon=3):
        self.name = name
        self.team = []
        self.pc = []

        if random_num_pokemon is not None:
            for i in range(random_num_pokemon):
                self.team.append(Pokemon((450, 100), level=50))

    def team_is_alive(self):
        for pokemon in self.team:
            if pokemon.is_alive():
                return True
        return False
