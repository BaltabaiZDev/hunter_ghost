import pygame
import random
from config import GHOST_GROUND_IMG, GHOST_FLYING_IMG, GROUND_Y

class Ghost:
    def __init__(self, ghost_type, level):
        self.type = ghost_type  # "ground" немесе "flying"
        self.x = 1100
        self.y = GROUND_Y if ghost_type == 'ground' else 350
        self.speed = (15 if ghost_type == 'ground' else 9) + level

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        img = GHOST_FLYING_IMG if self.type == 'flying' else GHOST_GROUND_IMG
        screen.blit(img, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 60, 70)
