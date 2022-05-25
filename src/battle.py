class Battle:
    def __init__(self, player, cpu):
        self.player = player
        self.cpu = cpu

    def battle(self):
        while self.player.team_is_alive() and self.cpu.team_is_alive():
            pass


    def calculate_damage(self):
        #((((2*level)/5 + 2) * Power * A/D)/50 + 2) * Type * Crit(6.25& deals 1.5x) * random(85,100)
        pass
