import pygame
import random

# --- INIT ---
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1100, 700))
pygame.display.set_caption("Ghost Hunter")

# --- LOAD ---
background = pygame.image.load('assets/images/background.png')
castle = pygame.image.load('assets/images/castle.png')
bullet_img = pygame.image.load('assets/images/bullet.png')
player_right = [pygame.image.load(f'assets/images/player_right/{i}.png') for i in range(1, 5)]
player_left = [pygame.image.load(f'assets/images/player_left/{i}.png') for i in range(1, 5)]
ghost_ground = pygame.image.load('assets/images/ghost_ground.png')
ghost_flying = pygame.image.load('assets/images/ghost_flying.png')
bonus_img = pygame.image.load('assets/images/ammo.png')

# --- SOUNDS ---
pygame.mixer.init()
pygame.mixer.music.load('assets/sounds/music.mp3')
pygame.mixer.music.play(-1)
shoot_sound = pygame.mixer.Sound('assets/sounds/shoot.mp3')

# --- VARIABLES ---
player_x, player_y = 250, 550
player_speed = 10
is_jumping = False
jump_speed, gravity = 0, 2
ground_y = 550
player_direction = 'right'
player_anim_count = 0
bg_x = 0
bullet_speed = 20
ammo = 50
bonus_ammo = 20
score = 0
level = 1
required_score = 20
castle_hp = 10
game_over,win_game = False,False

# --- ENTITIES ---
ghosts = []
bullets = []
bonus_obj = None

# --- TIMERS ---
ground_timer, flying_timer, bonus_timer = 0, 0, 0
ground_interval = 50
flying_interval = 120
bonus_interval = 500

font = pygame.font.SysFont('Arial', 30)

# --- GAME LOOP ---
while True:
    screen.blit(background, (bg_x, 0))
    screen.blit(background, (bg_x + 1100, 0))
    screen.blit(castle, (20, 300))
    bg_x -= 5
    if bg_x <= -1100:
        bg_x = 0

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]: player_x += player_speed; player_direction = 'right'
        if keys[pygame.K_LEFT]: player_x -= player_speed; player_direction = 'left'

        if not is_jumping and keys[pygame.K_UP]:
            is_jumping = True
            jump_speed = -26
            
        if not (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]):
            player_direction = 'right'

        if is_jumping:
            player_y += jump_speed
            jump_speed += gravity
            if player_y >= ground_y:
                player_y = ground_y
                is_jumping = False

        # CONSTRAINTS
        player_x = max(0, min(700 - player_right[0].get_width(), player_x))

        # RECT
        player_rect = pygame.Rect(player_x + 10, player_y + 10, 40, 70)

        # SPAWN LOGIC
        ground_timer += 1
        flying_timer += 1
        bonus_timer += 1

        if ground_timer >= ground_interval:
            ground_timer = 0
            ground_interval = random.randint(10, 50)  # 1–1.6 сек аралығы
            ghosts.append({'x': 1100, 'y': ground_y, 'type': 'ground'})


        if flying_timer >= flying_interval and level >= 2:
            flying_timer = 0
            flying_interval = random.randint(180, 360)  # 3–6 сек аралығы (30 FPS)
            ghosts.append({'x': 1100, 'y': 350, 'type': 'flying'})


        if bonus_timer >= bonus_interval:
            bonus_timer = 0
            bonus_obj = {'x': random.randint(200, 500), 'y': ground_y + 65}

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and ammo > 0:
                    shoot_sound.play()
                    bullets.append({'x': player_x + 50, 'y': player_y + 30})
                    ammo -= 1

        # BULLET UPDATE
        for b in bullets[:]:
            b['x'] += bullet_speed
            screen.blit(bullet_img, (b['x'], b['y']))
            if b['x'] > 1200: bullets.remove(b)

        # GHOSTS UPDATE
        # GHOSTS UPDATE
        for g in ghosts[:]:
            if g['type'] == 'flying':
                g['x'] -= 7 + level
            else:
                g['x'] -= 13 + level
            if g['x'] < 70:
                ghosts.remove(g)
                castle_hp -= 1
                if castle_hp <= 0: game_over = True
                continue

            img = ghost_flying if g['type'] == 'flying' else ghost_ground
            screen.blit(img, (g['x'], g['y']))
            ghost_rect = pygame.Rect(g['x'], g['y'], 60, 70)

            if player_rect.colliderect(ghost_rect):
                game_over = True

            for b in bullets[:]:
                if pygame.Rect(b['x'], b['y'], 20, 10).colliderect(ghost_rect):
                    bullets.remove(b)
                    ghosts.remove(g)
                    score += 1
                    break

        # BONUS
        if bonus_obj:
            screen.blit(bonus_img, (bonus_obj['x'], bonus_obj['y']))
            bonus_rect = pygame.Rect(bonus_obj['x'], bonus_obj['y'], 32, 32)
            if player_rect.colliderect(bonus_rect):
                ammo += bonus_ammo
                bonus_obj = None

        # LEVEL UP
        if score >= required_score:
            level += 1
            score = 0
            required_score += 10
            ground_interval = max(20, ground_interval - 10)
            flying_interval = max(60, flying_interval - 20)
            if level > 5:
                win_game = True

        # DRAW
        player_img = player_right[player_anim_count] if player_direction == 'right' else player_left[player_anim_count]
        screen.blit(player_img, (player_x, player_y))
        player_anim_count = (player_anim_count + 1) % 4

        screen.blit(font.render(f"HP: {castle_hp}", True, (255, 0, 0)), (40, 30))
        screen.blit(font.render(f"Ammo: {ammo}", True, (255, 255, 0)), (40, 60))
        screen.blit(font.render(f"Level: {level}", True, (0, 255, 0)), (40, 90))
        screen.blit(font.render(f"Score: {score}/{required_score}", True, (0, 255, 255)), (40, 120))


    if win_game:
        pygame.mixer.music.stop()
        win_font = pygame.font.SysFont('Arial', 60)
        small_font = pygame.font.SysFont('Arial', 30)

        # Optional: жеңіс дыбысы
        win_sound = pygame.mixer.Sound('assets/sounds/win.wav')
        win_sound.play()

        # Анимация және жеңіс экраны
        screen.fill((0, 0, 0))
        text = win_font.render("VICTORY! YOU SAVED THE CASTLE!", True, (0, 255, 0))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, 250))

        info = small_font.render("Press any key to restart...", True, (200, 200, 200))
        screen.blit(info, (screen.get_width()//2 - info.get_width()//2, 350))
        pygame.display.update()

        # Күту және кез келген батырмаға жауап беру
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False
                    # Барлығын бастапқы мәнге келтіру
                    player_x, player_y = 250, 550
                    ammo = 50
                    score = 0
                    level = 1
                    required_score = 20
                    ghosts.clear()
                    bullets.clear()
                    castle_hp = 10
                    bonus_obj = None
                    win_game = False
                    pygame.mixer.music.play(-1)
    if game_over:
        screen.blit(font.render("GAME OVER", True, (255, 0, 0)), (440, 300))
        pygame.display.update()
        pygame.time.delay(3000)
        pygame.quit()
        exit()


    pygame.display.update()
    clock.tick(30 )