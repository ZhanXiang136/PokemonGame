import pygame

class Button(object):
    def __init__(self, pos, text, font, feedback="", bg="black"):
        pygame.init()
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Gill Sans", font)
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, bg)

    def change_text(self, text, bg="black"):
        self.text = self.font.render(text, False, pygame.Color("Black"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0,0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x,y):
                    self.change_text(self.feedback, bg="red")