import pygame
from constants import *


class Button:
    def __init__(self, color, selected_color, x, y, width, height, text=''):
        self.color = color
        self.selected_color = selected_color  # Add this line
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.selected = False  # Add this line

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y -
                             2, self.width+4, self.height+4), 0)

        if self.selected:  # Add this if-else block
            pygame.draw.rect(win, self.selected_color,
                             (self.x, self.y, self.width, self.height), 0)
        else:
            pygame.draw.rect(win, self.color, (self.x, self.y,
                             self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('arial', 30)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                            self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


class Text:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y

    def draw(self, win):
        font = pygame.font.SysFont('arial', 30)
        text_surface = font.render(self.text, True, BLACK)
        win.blit(text_surface, (self.x, self.y))
