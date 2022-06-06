from button import ViewButton
import json
import random
import pygame
import time
from image import Image

class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

        self.player_pokemon = player.team[0]
        self.enemy_pokemon = enemy.team[0]

        self.info = {
            'attacker': None,
            'defender': None,
            'hit': None,
            'move': None,
            'damage': None,
            'type': None,
            'critical': None
        }

        self.text = []
        self.text_index = 0

    def animate(self, moving_pokemon, displays, faint=False):
        '''
        animating pokemon movement and display texts
        :param moving_pokemon: pokemon that is animaitng
        :param displays: displays to be displayed
        :param faint: faint animation
        :return: None
        '''
        pygame.init()
        screen = pygame.display.set_mode((960, 640))
        screen.fill((255, 255, 255))
        clock = pygame.time.Clock()
        in_animation = True

        if moving_pokemon == self.player_pokemon and not faint: #checks which direction the animation should go
            go_up = True
            go_down = False
        elif moving_pokemon == self.enemy_pokemon and not faint:
            go_up = False
            go_down = True
        else:
            go_up = False
            go_down = False

        while True:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

            if in_animation:
                if moving_pokemon == self.player_pokemon:
                    if go_up:
                        self.player_pokemon.sprite_back.update_pos("up")
                        if self.player_pokemon.sprite_back.pos[0] > self.enemy_pokemon.sprite_back.pos[0] or self.player_pokemon.sprite_back.pos[1] < self.enemy_pokemon.sprite_back.pos[1]:
                            go_up = False
                            go_down = True
                    elif go_down:
                        self.player_pokemon.sprite_back.update_pos("down")
                        if self.player_pokemon.sprite_back.pos[0] == self.player_pokemon.sprite_front.pos[0] or self.player_pokemon.sprite_back.pos[1] == self.player_pokemon.sprite_front.pos[1]:
                            in_animation = False
                    else:
                        self.player_pokemon.sprite_back.update_pos("faint")
                        if self.player_pokemon.sprite_back.pos[1] > self.player_pokemon.sprite_front.pos[1] + 200:
                            in_animation = False
                else:
                    if go_up:
                        self.enemy_pokemon.sprite_front.update_pos("up")
                        if self.enemy_pokemon.sprite_front.pos[0] == self.enemy_pokemon.sprite_back.pos[0] or self.enemy_pokemon.sprite_back.pos[1] == self.enemy_pokemon.sprite_front.pos[1]:
                            in_animation = False

                    elif go_down:
                        self.enemy_pokemon.sprite_front.update_pos("down")
                        if self.enemy_pokemon.sprite_front.pos[0] < self.player_pokemon.sprite_front.pos[0] or self.enemy_pokemon.sprite_front.pos[1] > self.player_pokemon.sprite_front.pos[1]:
                            go_up = True
                            go_down = False
                    else:
                        self.enemy_pokemon.sprite_front.update_pos("faint")
                        if self.enemy_pokemon.sprite_front.pos[1] > self.enemy_pokemon.sprite_back.pos[1]+200:
                            in_animation = False
            else:
                try:
                    displays['print-last-image'] = [Image((0, 455), file_path='images/text_box.png', scale=(700, 185))]
                    displays['print-last-text'] = [ViewButton((0, 455), (700, 185), self.text[self.text_index], 25, 'clear', (50, 25))]
                    self.redraw_window(screen, displays)
                    time.sleep(2.5)
                    self.text_index += 1
                    displays.pop('print-last-image', None)
                    displays.pop('print-last-text', None)
                except Exception as e:
                    self.text = []
                    self.text_index = 0
                    displays.pop('print-last-image', None)
                    displays.pop('print-last-text', None)
                    break
            self.redraw_window(screen, displays)

    def redraw_window(self, screen, active_displays):
        '''
        updates the window
        :param screen: screen to be displayed on
        :param active_displays: displays to be displayed
        :return: None
        '''
        screen.fill((255,255,255))
        for key, displays in active_displays.items():
            for display in displays:
                display.draw(screen)
        pygame.display.update()

    def organize_info(self):
        '''
        adds text to be printed to self.text
        :return: None
        '''
        self.text.clear()

        self.info['attacker'] = self.attacker

        if self.attacker == self.player_pokemon:
            self.info['defender'] = self.enemy_pokemon
        else:
            self.info['defender'] = self.player_pokemon

        self.text.append(f"{self.info['attacker'].name.capitalize()} used {self.info['move'].name}")

        if self.info['hit'] is None:
            if self.info['type'] is not None:
                self.text.append(f"It {self.info['type']}")

            if self.info['critical'] is not None:
                self.text.append(self.info['critical'])
        else:
            self.text.append(self.info['hit'])

        self.text.append(f"{self.info['defender'].name.capitalize()} took {self.info['damage']} points of damage")

        self.info = {
            'attacker': self.attacker,
            'defender': self.enemy_pokemon if self.attacker == self.player_pokemon else self.player_pokemon,
            'hit': None,
            'move': None,
            'damage': None,
            'type': None,
            'critical': None
        }

    def battle(self, move_num, displays):
        '''
        battling between two pokemons
        :param move_num: player move to be us
        :param displays: displays to be displayed
        :return: result of battle
        '''
        player_pokemon_move = self.player_pokemon.moves[move_num]
        enemy_pokemon_move = self.enemy_pokemon.moves[random.randint(0, 3)]

        player_pokemon_damage_class_modifier = self.damage_class_modifier(self.player_pokemon, self.enemy_pokemon, player_pokemon_move.damage_class)
        player_pokemon_type_modifier = self.type_modifier(player_pokemon_move.type, self.enemy_pokemon)
        player_pokemon_crit_modifier = self.crit_modifier()
        player_pokemon_damage = int((((self.player_pokemon.level*(2/5) + 2) * player_pokemon_move.power * player_pokemon_damage_class_modifier / 50) + 2) * player_pokemon_type_modifier * player_pokemon_crit_modifier * self.random_modifier() * self.hit_modifier(player_pokemon_move))

        enemy_pokemon_damage_class_modifier = self.damage_class_modifier(self.enemy_pokemon, self.player_pokemon, enemy_pokemon_move.damage_class)
        enemy_pokemon_type_modifier = self.type_modifier(enemy_pokemon_move.type, self.player_pokemon)
        enemy_pokemon_crit_modifier = self.crit_modifier()
        enemy_pokemon_damage = int((((self.enemy_pokemon.level*(2/5) + 2) * enemy_pokemon_move.power * enemy_pokemon_damage_class_modifier / 50) + 2) * enemy_pokemon_type_modifier * enemy_pokemon_crit_modifier * self.random_modifier() * self.hit_modifier((enemy_pokemon_move)))

        if self.player_pokemon.current_stats['speed'] >= self.enemy_pokemon.current_stats['speed']: #faster pokemon attacks first

            self.attacker = self.player_pokemon
            self.info['move'] = player_pokemon_move
            self.info['damage'] = player_pokemon_damage
            self.organize_info()
            self.animate(self.player_pokemon, displays)
            self.enemy_pokemon.take_damage(player_pokemon_damage)

            result = self.check_condition(displays)
            if result == 'continue':
                self.attacker = self.enemy_pokemon
                self.info['move'] = enemy_pokemon_move
                self.info['damage'] = enemy_pokemon_damage
                self.organize_info()
                self.animate(self.enemy_pokemon, displays)
                self.player_pokemon.take_damage(enemy_pokemon_damage)

                result = self.check_condition(displays)
                if result == 'done' or result == 'continue':
                    return 'done'
                else:
                    return result
            elif result == 'done':
                return 'done'
            else:
                return result
        else:
            self.attacker = self.enemy_pokemon
            self.info['move'] = enemy_pokemon_move
            self.info['damage'] = enemy_pokemon_damage
            self.organize_info()
            self.animate(self.enemy_pokemon, displays)
            self.player_pokemon.take_damage(enemy_pokemon_damage)

            result = self.check_condition(displays)
            if result == 'continue':
                self.attacker = self.player_pokemon
                self.info['move'] = player_pokemon_move
                self.info['damage'] = player_pokemon_damage
                self.organize_info()
                self.animate(self.player_pokemon, displays)
                self.enemy_pokemon.take_damage(player_pokemon_damage)

                result = self.check_condition(displays)
                if result == 'done' or result == 'continue':
                    return 'done'
                else:
                    return result
            elif result == 'done':
                return 'done'
            else:
                return result
        return "Done"

    def check_condition(self, displays):
        '''
        checks if the battle is still ongoing
        :param displays: things to be displayed
        :return: if battle is still on
        '''
        self.update_info(displays)
        for pokemon in self.player.team:
            if pokemon.name == self.player_pokemon:
                pokemon = self.player_pokemon

        for pokemon in self.enemy.team:
            if pokemon.name == self.enemy_pokemon:
                pokemon = self.enemy_pokemon

        if self.player_pokemon.is_alive() and self.enemy_pokemon.is_alive():
            return "continue"
        else:
            if not self.player_pokemon.is_alive():
                self.text.append(f"Your {self.player_pokemon.name} fainted")
                self.animate(self.player_pokemon, displays, faint=True)

                for pokemon in self.player.team:
                    if pokemon.is_alive():
                        self.player_pokemon = pokemon
                        self.update_info(displays)
                        return "done"
                self.text.append("You lost the battle")
                self.animate(self.player_pokemon, displays, faint=True)
                self.update_info(displays)
                return "player-lost"

            if not self.enemy_pokemon.is_alive():

                self.text.append(f"The opposing {self.enemy_pokemon.name} fainted")
                self.animate(self.enemy_pokemon, displays, faint=True)

                for pokemon in self.enemy.team:
                    if pokemon.is_alive():
                        self.enemy_pokemon = pokemon
                        self.update_info(displays)
                        return "done"
                self.text.append("You won the battle")
                self.update_info(displays)
                self.animate(self.enemy_pokemon, displays, faint=True)
                return "enemy-lost"
            else:
                return "Game Over"

    def damage_class_modifier(self, attacker, defender, damage_class):
        '''
        determines damage class modifier
        :param attacker: attacking pokemon
        :param defender: defending pokemon
        :param damage_class: special or physical
        :return: damage class modifier
        '''
        if damage_class == 'special':
            return attacker.current_stats['special-attack'] / defender.current_stats['special-defense']
        elif damage_class == 'physical':
            return attacker.current_stats['attack'] / defender.current_stats['defense']
        else:
            print(f'ERROR Damage Class: {damage_class}')

    def hit_modifier(self, move):
        '''
        checks if the attack hits the opposing pokemon based on move accuracy
        :param move: move to be check
        :return: if the attack hit
        '''
        hit = random.randint(0, move.accuracy) < move.accuracy
        if not hit:
            self.info['hit'] = "The attack missed"
            return 0
        return 1

    def type_modifier(self, attacking_type, defending_pokemon):
        '''
        determines the type advantage modifier
        :param attacking_type: type that's attacking
        :param defending_pokemon: type(s) that's defending
        :return: type modifier
        '''
        attacking_type = attacking_type.capitalize()
        defending_type_list = defending_pokemon.types
        modifier = 1

        with open('modules/type.json', 'r') as file:
            type_object = json.load(file)

            for defending_type in defending_type_list:
                defending_type = defending_type.capitalize()
                if defending_type in type_object[attacking_type]['immunes']:
                    modifier *= 0
                elif defending_type in type_object[attacking_type]['weaknesses']:
                    modifier *= 0.5
                elif defending_type in type_object[attacking_type]['strengths']:
                    modifier *= 2
                else:
                    modifier *= 1

            if modifier == 0:
                self.info['type'] = 'did nothing'
            elif modifier < 1:
                self.info['type'] = 'was not very effective'
            elif modifier > 1:
                self.info['type'] = 'was super effective'
            else:
                pass
            return modifier

    def crit_modifier(self):
        '''
        pokemon has a 6.25% to crit
        :return: if pokemon crits
        '''
        if random.random() < 0.0625:
            self.info['critical'] = "Critical Hit!"
            return 2
        else:
            return 1

    def random_modifier(self):
        '''
        random modifier between 0.85 and 1
        :return: random modifier
        '''
        return random.randint(85,100)/100

    def update_info(self, displays):
        '''
        update displays
        :param displays: displays to be updated
        :return: updated displays
        '''
        displays['images'][0] = self.player_pokemon.sprite_back
        displays['images'][1] = self.enemy_pokemon.sprite_front
        displays['buttons'][0] = ViewButton((10, 455), (330, 80), self.player_pokemon.moves[0].name, 30, 'clear', (10, 25))
        displays['buttons'][1] = ViewButton((360, 455), (330, 80), self.player_pokemon.moves[1].name, 30, 'clear', (10, 25))
        displays['buttons'][2] = ViewButton((10, 545), (330, 80), self.player_pokemon.moves[2].name, 30, 'clear', (10, 25))
        displays['buttons'][3] = ViewButton((360, 545), (330, 80), self.player_pokemon.moves[3].name, 30, 'clear', (10, 25))
        displays['buttons'][4] = ViewButton((385, 330), (250, 100), self.player_pokemon.info(), 20, 'clear')
        displays['buttons'][5] = ViewButton((60, 120), (250, 100), self.enemy_pokemon.info(), 20, 'clear')
        return displays
