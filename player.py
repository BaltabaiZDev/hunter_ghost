import pygame
from config import PLAYER_RIGHT, PLAYER_LEFT, GROUND_Y

class Player:
    def __init__(self):
        self.x = 250
        self.y = GROUND_Y
        self.speed = 10
        self.is_jumping = False
        self.jump_speed = 0
        self.gravity = 2
        self.direction = 'right'
        self.anim_count = 0
        self.ammo = 50

    def move(self, keys):
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.direction = 'right'
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.direction = 'left'
        if not (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]):
            self.direction = 'right'
        self.x = max(0, min(700 - PLAYER_RIGHT[0].get_width(), self.x))

    def jump(self, keys):
        if not self.is_jumping and keys[pygame.K_UP]:
            self.is_jumping = True
            self.jump_speed = -26

        if self.is_jumping:
            self.y += self.jump_speed
            self.jump_speed += self.gravity
            if self.y >= GROUND_Y:
                self.y = GROUND_Y
                self.is_jumping = False

    def get_rect(self):
        return pygame.Rect(self.x + 10, self.y + 10, 40, 70)

    def draw(self, screen, moving=False):
        img_list = PLAYER_RIGHT if self.direction == 'right' else PLAYER_LEFT
        if moving:
            screen.blit(img_list[self.anim_count], (self.x, self.y))
            self.anim_count = (self.anim_count + 1) % 4
        else:
            screen.blit(img_list[0], (self.x, self.y))
            self.anim_count = 0

