import json
import random
from image import Image
from move import Move
import math

class Pokemon:
    def __init__(self, pos, level=None, name=None):
        self.level = level or random.randint(0, 100)
        with open('modules/pokemon.json', "r") as pokemon_file:
            pokemon_obj_list = json.load(pokemon_file)

            while True: #loads a usable pokemon
                try: #sets up all the instance variable
                    self.name = name or random.choice(list(pokemon_obj_list['results']))
                    pokemon_obj = pokemon_obj_list['results'][self.name]
                    self.id = pokemon_obj['id']
                    self.types = pokemon_obj['types']
                    self.base_stats = self.load_stats(pokemon_obj['stats'])
                    self.current_stats = self.calculate_current_stats()
                    self.hp = self.current_stats['hp']
                    self.sprite_front = Image(pos, url=pokemon_obj['sprite_front'])
                    self.sprite_back = Image(pos, url=pokemon_obj['sprite_back'])

                    self.moves = []
                    for i in range(4): #makes sure the pokemon doesn't have the same move
                        while True:
                            move = pokemon_obj['moves'][random.randint(0, len(pokemon_obj['moves'])-1)]
                            for move_ in self.moves:
                                if move_.name == move:
                                    break
                            self.moves.append(Move(move))
                            break
                    break
                except:
                    pass

    def calculate_current_stats(self):
        '''
        HP = floor(0.01 x (2 x Base + IV + floor(0.25 x EV)) x Level) + Level + 10
        Other Stats = (floor(0.01 x (2 x Base + IV + floor(0.25 x EV)) x Level) + 5) x Nature.
        IV=31
        IV=1
        Nature=1
        :return:
        '''
        return_dict = {}
        for key in self.base_stats:
            if key == 'hp':
                return_dict[key] = math.floor(0.01 * (2 * self.base_stats[key] + 31 + math.floor(0.25 * 1)) * self.level) + self.level + 10
            else:
                return_dict[key] = math.floor(0.01 * (2 * self.base_stats[key] + 31 + math.floor(0.25 * 1)) * self.level) + 5
        return return_dict

    def take_damage(self, damage):
        '''
        pokemon take damage
        :param damage: damage to be taken
        :return: pokemon is alive
        '''
        self.hp -= int(damage)
        if self.is_alive() == False:
            self.hp = 0
            return False
        return True

    def is_alive(self):
        '''
        :return: if pokemon is alive
        '''
        return self.hp > 0

    def load_stats(self, stats):
        '''
        scale stats based on base stats
        :param stats: base stats
        :return: current stats
        '''
        stat_names = ['hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed']
        return_stats = {}
        for i in range(6):
            return_stats[stat_names[i]] = stats[i]
        return return_stats

    def info(self):
        '''
        :return: information about the pokemon
        '''
        return [self.name.capitalize(), self.level, [self.hp, self.current_stats['hp']], self.types]