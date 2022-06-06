import pygame
import json

class Button(object):
    def __init__(self, pos, size, text, font_size, bg, text_pos=(0, 0)):
        '''
        button class
        :param pos: position of the button on screen
        :param size: size of the button
        :param text: text on the button
        :param font_size:
        :param bg: tuple containing (active background, inactive background)
        '''

        self.pos = pos
        self.font = pygame.font.SysFont("Times", font_size)
        self.size = size
        self.text_pos = text_pos

        if bg == 'clear':
            self.surface = pygame.Surface(self.size, pygame.SRCALPHA, 32)
        else:
            self.surface = pygame.Surface(self.size)
            self.bg = {'active': bg[0], 'inactive': bg[1]}
            self.surface.fill(self.bg['inactive'])
            self.current_bg = self.bg['inactive']

        self.rect = pygame.Rect(pos[0], pos[1], self.size[0], self.size[1])

        self.text_string = text
        if isinstance(text, str):
            self.setup_text_string(self.text_string, self.text_pos)

    def setup_text_string(self, text, pos=(0,0)):
        '''
        :param text: text to be displayed
        :param pos: position of text
        :return: None
        '''
        self.text = self.font.render(text, False, pygame.Color('Black'))
        self.surface.blit(self.text, pos)

    def draw(self, screen):
        '''
        draws the button on the screen
        :param screen: screen to be drawn on
        :return: None
        '''
        screen.blit(self.surface, self.pos)

    def click(self, coord):
        '''
        determines if button is clicked
        :param coord: coord of the mouse
        :return: if button is clicked
        '''
        if self.rect.collidepoint(coord[0], coord[1]):
            return True
        return False

    def inactive(self):
        pass

class TextButton(Button):
    def __init__(self, pos, size, text, font_size, bg, text_pos=(0, 0)):
        super(TextButton, self).__init__(pos, size, text, font_size, bg, text_pos)
        self.original_text = text
        self.setup_text_string(self.text_string)

    def active(self, key):
        '''
        active button allows user to modify it
        :param key: key to be added
        :return: None
        '''
        if key == -1:
            self.text_string= self.text_string[:-1]
        else:
            self.text_string += key
        self.setup_text_string(self.text_string)

    def inactive(self):
        '''
        inactive button does not allow user to do anything
        :return: None
        '''
        if self.text_string == "":
            self.text_string = self.original_text
        self.current_bg = self.bg['inactive']
        self.setup_text_string(self.text_string)

    def setup_text_string(self, text, pos=(0,0)):
        '''
        :param text: text to be displayed
        :param pos: position of text
        :return: None
        '''
        self.text = self.font.render(self.text_string, False, pygame.Color('Black'))
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.current_bg)
        self.surface.blit(self.text, pos)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def click(self, coord):
        '''
        determines if button is clicked
        :param coord: coord of the mouse
        :return: if button is clicked
        '''
        if self.rect.collidepoint(coord[0], coord[1]):
            self.current_bg = self.bg['active']
            if self.text_string == self.original_text:
                self.text_string = ""
            self.setup_text_string(self.text_string)
            return True
        return False

class ViewButton(Button):
    def __init__(self, pos, size, text, font_size, bg, text_pos=(0, 0)):
        super(ViewButton, self).__init__(pos, size, text, font_size, bg, text_pos)
        if isinstance(text, list):
            self.load_pokemon_info(text)

    def load(self, type_, name):
        '''
        loads information
        :param type_: type of information
        :param name: name of type
        :return: None
        '''
        self.surface.fill((255, 255, 255))
        if type_ == "move":
            with open('modules/move.json', "r") as file:
                move_object = json.load(file)
            try:
                move_info = move_object['results'][name]
                self.load_move(name, move_info)
            except:
                self.setup_text_string("Move does not exist", pos=(10,10))
        elif type_ == 'pokemon':
            with open('modules/pokemon.json', "r") as file:
                pokemon_object = json.load(file)
            try:
                pokemon_info = pokemon_object['results'][name]
                self.load_pokemon(name, pokemon_info)
            except:
                self.setup_text_string("Pokemon does not exist", pos=(10, 10))
        elif type_ == 'type':
            with open('modules/type.json', 'r') as file:
                type_object = json.load(file)
            try:
                type_info = type_object[name.capitalize()]
                self.load_type(name.capitalize(), type_info)
            except:
                self.setup_text_string("Type does not exist", pos=(10,10))
        else:
            self.setup_text_string("Invaild Input", pos=(10, 10))

    def load_pokemon_info(self, text):
        '''
        loads pokemon info
        :param text: texts to be displayed
        :return: None
        '''
        for i in range(len(text)):
            if i == 0:
                pos = (10, 10)
                new_text = text[i]
            elif i == 1:
                pos = (175, 10)
                new_text = f'LV: {text[i]}'
            elif i == 2:
                pos = (100, 40)
                new_text = f'HP: {text[i][0]} / {text[i][1]}'
            elif i == 3:
                pos = (10, 70)
                new_text = ''
                for type_ in text[i]:
                    new_text += type_ + " "
            else:
                new_text = text[i]
                pos = (0, 0)
            self.setup_text_string(str(new_text), pos=pos)

    def load_type(self, name, type_obj):
        '''
        loads type
        :param name: name of type
        :param type_obj: information about type
        :return: None
        '''
        self.setup_text_string(f"Type: {name}", pos=(10, 10))
        self.setup_text_string(f"Immunes: ", pos=(10, 40))
        self.setup_text_string(f"{type_obj['immunes']}", pos=(10, 55))
        self.setup_text_string(f"Weaknessess: ", pos=(10, 85))
        self.setup_text_string(f"{type_obj['weaknesses']} ", pos=(10, 100))
        self.setup_text_string(f"Strengths: ", pos=(10, 130))
        self.setup_text_string(f"{type_obj['strengths']} ", pos=(10, 145))

    def load_move(self, name, move_obj):
        '''
        loads move
        :param name: name of move
        :param move_obj: information about move
        :return: None
        '''
        self.setup_text_string(f"Move: {name}", pos=(10, 10))
        y_increase = 10

        for key, value in move_obj.items():
            y_increase += 30
            self.setup_text_string(f"{key}: {value}", pos=(10, y_increase))

    def load_pokemon(self, name, pokemon_obj):
        '''
        loads pokemon
        :param name: name of pokemon
        :param pokemon_obj: information about pokemon
        :return: None
        '''
        self.setup_text_string(f"Pokemon: {name}", pos=(10, 10))
        y_increase = 10

        for key, value in pokemon_obj.items():
            y_increase += 30

            if key == 'moves':
                self.setup_text_string(f"{key}: ", pos=(10, y_increase))
                i = 0
                while True:
                    y_increase += 15
                    if i == len(value)-1:
                        self.setup_text_string(f"{value[i]}", pos=(10, y_increase))
                        break
                    elif i == len(value)-2:
                        self.setup_text_string(f"{value[i]}          {value[i + 1]}", pos=(10, y_increase))
                        break
                    else:
                        self.setup_text_string(f"{value[i]}          {value[i + 1]}", pos=(10, y_increase))
                    i += 2
            else:
                self.setup_text_string(f"{key}: {value}", pos=(10, y_increase))
