import pygame

from button import Button
from pokemon import Pokemon
from move import Move

try:
    # Python2
    from urllib2 import urlopen
except ImportError:
    # Python3
    from urllib.request import urlopen

pygame.init() #initalize pygame

#screens
battle_screen = pygame.display.set_mode((1600, 950))
opening_screen = pygame.display.set_mode((960, 640))
current_screen = opening_screen

#backgrounds
beginning_bg = pygame.image.load('images/opening.png')
beginning_bg = pygame.transform.scale(beginning_bg, (960, 640))
battle_bg = pygame.image.load('images/battle.png')
battle_bg = pygame.transform.scale(battle_bg, (1600, 950))
current_bg = battle_bg

#colors
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)

#buttons
attack_button = Button((100,100), "Click Here", font=16, feedback="Hello")

#display list
active_display = []
#active_display.append(attack_button)

def image_url_to_loadable(image_str):
    image_str = urlopen(image_url).read()
    # create a file object (stream)
    image_file = io.BytesIO(image_str)

def redraw_window():
    current_screen.blit(current_bg, (0, 0))
    for display in active_display:
        display.draw(current_screen)
    pygame.display.flip()

def run():
    clock = pygame.time.Clock()

    while True:
        clock.tick(30)  # 30fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            for display in active_display:
                display.click(event)
        redraw_window()

if __name__ == '__main__':
    run()



