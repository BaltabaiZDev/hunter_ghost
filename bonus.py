import pygame
import random
from config import BONUS_IMG, GROUND_Y

class Bonus:
    def __init__(self):
        self.x = random.randint(200, 500)
        self.y = GROUND_Y + 65

    def draw(self, screen):
        screen.blit(BONUS_IMG, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 32, 32)
