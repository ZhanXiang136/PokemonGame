import json
import random

class Pokemon:
    def __int__(self, level=None, name=None):
        self.level = level or random.randint(0, 100)
        with open('/modules/pokemon.json', "r") as pokemon_file:
            pokemon_obj_list = json.load(pokemon_file)

            self.name = name or random.choice(list(pokemon_obj_list['pokemon']))
            pokemon_obj = pokemon_obj_list['pokemon'][self.name]
            self.id = pokemon_obj['id']
            self.types = pokemon_obj['types']
            self.base_stats = self._load_stats(pokemon_obj['stats'])
            self.current_stats = self.calculate_current_stats()
            self.hp = self.current_stats['hp']
            self.sprite_front = pokemon_obj['sprite_front']
            self.sprite_back = pokemon_obj['sprite_back']

    def calculate_current_stats(self):
        return {}

    def is_alive(self):
        return self.hp > 0

    def _load_stats(self, stats):
        stat_names = ['hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed']
        return_stats = {}
        for i in range(6):
            return_stats[stat_names[i]] = stats[i]
        return return_stats
