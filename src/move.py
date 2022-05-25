class Move(object):
    def __init__(self, name, accuracy, power, damage_class, type_, pp):
        self.name = name
        self.accuracy = accuracy
        self.power = power
        self.damage_class = damage_class
        self.type = type_
        self.pp = pp
        self.current_pp = self.pp

    def use_move(self):
        if self.current_pp != 0:
            self.current_pp -= 1
            return True
        return False

    def restore_pp(self):
        self.current_pp = self.pp