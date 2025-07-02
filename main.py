import pygame
import random
from config import *
from player import Player
from ghost import Ghost
from bullet import Bullet
from bonus import Bonus
from datetime import datetime, timezone
from db import save_result

def input_nickname(screen, font):
    input_box = pygame.Rect(350, 300, 400, 60)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = True
    text = ""
    done = False

    info_font = pygame.font.SysFont('Arial', 36)
    prompt = info_font.render("Enter your nickname:", True, (255, 255, 255))

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if len(text.strip()) > 0:
                            return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        # Қазақ, орыс, ағылшын әріптерін қолдайды
                        if len(text) < 20:
                            text += event.unicode

        screen.fill((30, 30, 30))
        # Prompt
        screen.blit(prompt, (screen.get_width() // 2 - prompt.get_width() // 2, 200))
        # Input box
        txt_surface = font.render(text, True, (255, 255, 255))
        width = max(400, txt_surface.get_width() + 20)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ghost Hunter")
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 30)

    # --- Nickname input ---
    nickname = input_nickname(screen, font)
    start_time = datetime.now(timezone.utc)

    player = Player()
    bullets = []
    ghosts = []
    bonus_obj = None

    score = 0
    level = 1
    required_score = 20
    bg_x = 0
    castle_hp = 10
    ground_timer, flying_timer, bonus_timer = 0, 0, 0
    ground_interval = 75
    flying_interval = 70
    bonus_interval = 500
    win_game, game_over = False, False
    a = 0

    running = True
    while running:
        screen.blit(BG_IMG, (bg_x, 0))
        screen.blit(BG_IMG, (bg_x + 1100, 0))
        screen.blit(CASTLE_IMG, (20, 400))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not game_over and not win_game:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and player.ammo > 0:
                        SHOOT_SOUND.play()
                        bullets.append(Bullet(player.x + 50, player.y + 30))
                        player.ammo -= 1

        if not game_over and not win_game:
            keys = pygame.key.get_pressed()
            player.move(keys)
            player.jump(keys)

            ground_timer += 1
            flying_timer += 1
            bonus_timer += 1

            if ground_timer >= ground_interval:
                ground_timer = 0
                ground_interval = random.randint(15-int(a*0.05), 60 - int(a*0.3))
                ghosts.append(Ghost('ground', level))

            if flying_timer >= flying_interval and level >= 2:
                flying_timer = 0
                flying_interval = random.randint(20-int(a*0.1), 90 - a)
                ghosts.append(Ghost('flying', level))

            if bonus_timer >= bonus_interval:
                bonus_timer = 0
                bonus_obj = Bonus()
            

            for b in bullets[:]:
                b.update()
                b.draw(screen)
                if b.x > WIDTH + 100:
                    bullets.remove(b)

            for g in ghosts[:]:
                g.update()
                g.draw(screen)
                if g.x < 70:
                    ghosts.remove(g)
                    castle_hp -= 1
                    if castle_hp <= 0:
                        game_over = True
                    continue

                if player.get_rect().colliderect(g.get_rect()):
                    game_over = True

                for b in bullets[:]:
                    if b.get_rect().colliderect(g.get_rect()):
                        ghosts.remove(g)
                        if b in bullets: bullets.remove(b)
                        score += 1
                        break

            if bonus_obj:
                bonus_obj.draw(screen)
                if player.get_rect().colliderect(bonus_obj.get_rect()):
                    player.ammo += 20
                    bonus_obj = None

            if score >= required_score:
                level += 1
                a += 5
                score = 0
                required_score += 10
                ground_interval = max(20, ground_interval - 10)
                flying_interval = max(60, flying_interval - 20)
                if level > 5:
                    win_game = True

            moving = keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]
            player.draw(screen, moving=moving)
            screen.blit(font.render(f"HP: {castle_hp}", True, (255, 0, 0)), (40, 30))
            screen.blit(font.render(f"Ammo: {player.ammo}", True, (255, 255, 0)), (40, 60))
            screen.blit(font.render(f"Level: {level}", True, (0, 255, 0)), (40, 90))
            screen.blit(font.render(f"Score: {score}/{required_score}", True, (0, 255, 255)), (40, 120))

        if win_game:
            pygame.mixer.music.stop()
            WIN_SOUND.play()
            win_font = pygame.font.SysFont('Arial', 60)
            small_font = pygame.font.SysFont('Arial', 30)
            screen.fill((0, 0, 0))
            text = win_font.render("VICTORY! YOU SAVED THE CASTLE!", True, (0, 255, 0))
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 250))
            info = small_font.render("Press any key to restart...", True, (200, 200, 200))
            screen.blit(info, (screen.get_width() // 2 - info.get_width() // 2, 350))
            pygame.display.update()

            end_time = datetime.now(timezone.utc)
            save_result(nickname, castle_hp, score, level, start_time, end_time)

            pygame.time.delay(500)
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting = False
                    elif event.type == pygame.KEYDOWN:
                        player = Player()
                        bullets.clear()
                        ghosts.clear()
                        bonus_obj = None
                        score = 0
                        level = 1
                        required_score = 20
                        castle_hp = 10
                        ground_timer = flying_timer = bonus_timer = 0
                        ground_interval = 50
                        flying_interval = 120
                        win_game = False
                        start_time = datetime.now(timezone.utc)
                        pygame.mixer.music.play(-1)
                        waiting = False

        if game_over:
            over_font = pygame.font.SysFont('Arial', 60)
            screen.blit(over_font.render("GAME OVER", True, (255, 0, 0)), (440, 300))
            pygame.display.update()

            end_time = datetime.now(timezone.utc)
            save_result(nickname, castle_hp, score, level, start_time, end_time)

            pygame.time.delay(3000)
            running = False

        pygame.display.update()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
