import pygame
from button import Button, TextButton, ViewButton
from image import Image
from player import Player
from enemy import Enemy
from battle import Battle

class PokemonGame():
    def __init__(self):
        pygame.init()

        # screens
        self.current_screen = pygame.display.set_mode((960, 640), pygame.RESIZABLE)

        # backgrounds
        self.beginning_bg = Image((0, 0), file_path='images/opening.png', scale=(960, 640))
        self.battle_bg = Image((0, 0), file_path='images/battle.png', scale=(700, 640))

        # images
        self.pokemon_logo = Image((180, 50), file_path='images/pokemon_logo.png', scale=(600, 220))

        # colors
        self.LIGHT_PEACH = pygame.Color(255,236,217)
        self.DARK_PEACH = pygame.Color(255,203,164)

        # buttons
        self.name_button = TextButton((380, 400), (200, 30), "Enter your name", 30, (self.LIGHT_PEACH, self.DARK_PEACH))
        self.ask_button = TextButton((700, 580), (260, 60), "type name e.g. move pound", 15, (self.LIGHT_PEACH, self.DARK_PEACH), (10, 10))
        self.restart_button = ViewButton((380, 400), (200, 30), "Restart?", 30, (self.LIGHT_PEACH, self.DARK_PEACH))
        self.info_button = ViewButton((700, 0), (260, 580), "", 15, 'clear', (10,10))

        # display list
        self.active_displays = {
            'background': [self.beginning_bg],
            'images': [self.pokemon_logo],
            'buttons': [self.name_button],
        }

    def redraw_window(self):
        '''
        updates the screen
        :return: None
        '''
        for key, displays in self.active_displays.items():
            for display in displays:
                display.draw(self.current_screen)
        pygame.display.update()

    def change_to_battle_screen(self, name):
        '''
        changes the screen to battle screen
        :param name: name of player
        :return: None
        '''
        self.current_screen.fill((255, 255, 255))
        self.player = Player(name)
        self.enemy = Enemy("Bob")
        self.battle = Battle(self.player, self.enemy)

        self.active_displays['images'].clear()
        self.active_displays['images'].append(None)
        self.active_displays['images'].append(None)
        self.active_displays['buttons'].clear()
        self.active_displays['buttons'].append(None)
        self.active_displays['buttons'].append(None)
        self.active_displays['buttons'].append(None)
        self.active_displays['buttons'].append(None)
        self.active_displays['buttons'].append(None)
        self.active_displays['buttons'].append(None)

        self.active_displays['background'] = [self.battle_bg]
        self.active_displays = self.battle.update_info(self.active_displays)

        self.active_displays['images'].append(Image((325, 300), file_path='images/pokemon_info_textbox.png', scale=(350, 160)))
        self.active_displays['images'].append(Image((0, 90), file_path='images/pokemon_info_textbox.png', scale=(350, 160)))

        self.active_displays['images'].append(Image((-20, 450), file_path='images/move_textbox.png', scale=(375, 80)))
        self.active_displays['images'].append(Image((330, 450), file_path='images/move_textbox.png', scale=(375, 80)))
        self.active_displays['images'].append(Image((-20, 540), file_path='images/move_textbox.png', scale=(375, 80)))
        self.active_displays['images'].append(Image((330, 540), file_path='images/move_textbox.png', scale=(375, 80)))

        self.active_displays['buttons'].append(self.info_button)
        self.active_displays['buttons'].append(self.ask_button)

    def change_to_opening_screen(self, result):
        '''
        changes the screen to opening screen
        :param result: outcome of player battle
        :return: None
        '''
        self.current_screen.fill((255, 255, 255))

        if result == 'player-lost': #display the outcome of player battle
            self.winner_button = ViewButton((380, 350), (200, 30), "You Lost", 30, (self.LIGHT_PEACH, self.DARK_PEACH))
        else:
            self.winner_button = ViewButton((380, 350), (200, 30), "You Won", 30, (self.LIGHT_PEACH, self.DARK_PEACH))

        self.active_displays = {
            'background': [self.beginning_bg],
            'images': [self.pokemon_logo],
            'buttons': [self.restart_button, self.winner_button],
        }


    def run(self):
        '''
        starts the game
        :return: None
        '''
        clock = pygame.time.Clock()
        active_button = None
        while True:
            clock.tick(30)  # 30fps

            for event in pygame.event.get():
                if event.type == pygame.QUIT: #ends the game if player exited
                    pygame.quit()
                    break

                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    for display in self.active_displays['buttons']:
                        if isinstance(display, Button):
                            if display.click((x, y)):
                                if display == self.restart_button:
                                    self.change_to_battle_screen(self.player.name)
                                    break
                                active_button = display
                                break
                            else:
                                if isinstance(display, TextButton):
                                    display.inactive()
                                active_button = None

                if isinstance(active_button, TextButton): #TextButton features
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            active_button.active(-1)
                        elif event.key == 13:
                            if active_button == self.name_button:
                                self.change_to_battle_screen(active_button.text_string)
                            elif active_button == self.ask_button:
                                self.load_info(active_button.text_string)
                        else:
                            active_button.active(event.unicode)

                if isinstance(active_button, ViewButton): #ViewButton features
                    for i in range(4):
                        if self.active_displays['buttons'][i] == active_button:
                            result = self.battle.battle(i, self.active_displays)
                            if result == 'done':
                                self.active_displays = self.battle.update_info(self.active_displays)
                            elif result == 'player-lost' or result == 'enemy-lost':
                                self.change_to_opening_screen(result)
                                active_button = False
                            break

            self.redraw_window() #redraws the screen

    def load_info(self, text):
        '''
        display info
        :param text: command
        :return: None
        '''
        try:
            text_list = text.split(" ")
            self.info_button.load(text_list[0], text_list[1])
        except:
            self.info_button.load("Error", "Error")
        self.ask_button.text_string = ""

if __name__ == '__main__':
    pokemon_game = PokemonGame()
    pokemon_game.run()
