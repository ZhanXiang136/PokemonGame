import json

class Move(object):
    def __init__(self, move_name):
        with open('modules/move.json', "r") as pokemon_file:
            move_obj_list = json.load(pokemon_file)
            move = move_obj_list['results'][move_name]
            self.name = move['name']
            self.accuracy = move['accuracy']
            self.power = move['power']
            self.damage_class = move['damage_class']
            self.type = move['type']
            self.pp = move['pp']
            self.current_pp = self.pp

    def use_move(self):
        if self.current_pp != 0:
            self.current_pp -= 1
            return True
        return False

    def restore_pp(self):
        self.current_pp = self.pp
