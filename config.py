import pygame

# Экран
WIDTH, HEIGHT = 1100, 700
GROUND_Y = 550

# Файлдар
BG_IMG = pygame.image.load('assets/images/background.png')
CASTLE_IMG = pygame.image.load('assets/images/castle.png')
BULLET_IMG = pygame.image.load('assets/images/bullet.png')
PLAYER_RIGHT = [pygame.image.load(f'assets/images/player_right/{i}.png') for i in range(1, 5)]
PLAYER_LEFT = [pygame.image.load(f'assets/images/player_left/{i}.png') for i in range(1, 5)]
GHOST_GROUND_IMG = pygame.image.load('assets/images/ghost_ground.png')
GHOST_FLYING_IMG = pygame.image.load('assets/images/ghost_flying.png')
BONUS_IMG = pygame.image.load('assets/images/ammo.png')

# Дыбыстар
pygame.mixer.init()
pygame.mixer.music.load('assets/sounds/music.mp3')
SHOOT_SOUND = pygame.mixer.Sound('assets/sounds/shoot.mp3')
WIN_SOUND = pygame.mixer.Sound('assets/sounds/win.wav')
