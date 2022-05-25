import pygame


class PokemonBattleRunner(object):
    def run(self):
        pygame.init()

        screen = pygame.display.set_mode((750, 750))
        pygame.display.set_caption("Pokemon Battle")

        # fonts
        gill_sans_font = pygame.font.SysFont("Gill Sans", 16)

        # colors
        black = pygame.Color(255, 255, 255)
        white = pygame.Color(0, 0, 0)
        color = black

        # rectangles
        input_name_rect = pygame.Rect(100, 100, 30, 30)

        clock = pygame.time.Clock()

        user_text = ""

        run = True
        color_active = False
        while run:
            clock.tick(30)  # 30fps

            # when "quit" is clicked in the game window, ends the loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_name_rect.collidepoint(event.pos):
                        color_active = True
                    else:
                        color_active = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

            if color_active:
                color = white
            else:
                color = black

            screen.fill((100, 100, 100))

            pygame.draw.rect(screen, color, input_name_rect)
            text_surface = gill_sans_font.render(user_text, True, (255, 255, 255))

            screen.blit(text_surface, (input_name_rect.x + 5, input_name_rect.y + 5))

            input_name_rect.w = max(100, text_surface.get_width() + 10)
            pygame.display.update()  # updates the screen