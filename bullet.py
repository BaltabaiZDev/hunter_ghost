import pygame
from config import BULLET_IMG

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 40

    def update(self):
        self.x += self.speed

    def draw(self, screen):
        screen.blit(BULLET_IMG, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 20, 10)
