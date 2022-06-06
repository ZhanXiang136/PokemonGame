from pokemon import Pokemon

class Player:
    def __init__(self, name, random_num_pokemon=3):
        self.name = name
        self.team = []
        self.pc = []

        if random_num_pokemon is not None:
            for i in range(random_num_pokemon):
                self.team.append(Pokemon((50, 275), level=50))

    def add_pokemon(self, pokemon):
        '''
        adds pokemon to player team
        :param pokemon: pokemon to be added
        :return: None
        '''
        if self.team < 6:
            self.team.append(pokemon)
        else:
            self.pc.append(pokemon)

    def team_is_alive(self):
        '''
        :return: if all pokemon in team is alive
        '''
        for pokemon in self.team:
            if pokemon.is_alive():
                return True
        return False
