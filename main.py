import pygame
import random
from config import *
from player import Player
from ghost import Ghost
from bullet import Bullet
from bonus import Bonus

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ghost Hunter")
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()

    player = Player()
    bullets = []
    ghosts = []
    bonus_obj = None

    # Гейм стейттер
    score = 0
    level = 1
    required_score = 20
    bg_x = 0
    castle_hp = 10
    ground_timer, flying_timer, bonus_timer = 0, 0, 0
    ground_interval = 50
    flying_interval = 70
    bonus_interval = 500
    font = pygame.font.SysFont('Arial', 30)
    win_game, game_over = False, False

    running = True
    while running:
        # BG draw + parallax
        screen.blit(BG_IMG, (bg_x, 0))
        screen.blit(BG_IMG, (bg_x + 1100, 0))
        screen.blit(CASTLE_IMG, (20, 400))
      # bg_x -= 5
      # if bg_x <= -1100:
      #    bg_x = 0


        # --- Event Handling ---
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

            # --- Ghost Spawn ---
            ground_timer += 1
            flying_timer += 1
            bonus_timer += 1

            if ground_timer >= ground_interval:
                ground_timer = 0
                ground_interval = random.randint(10, 50)
                ghosts.append(Ghost('ground', level))

            if flying_timer >= flying_interval and level >= 2:
                flying_timer = 0
                flying_interval = random.randint(180, 360)
                ghosts.append(Ghost('flying', level))

            if bonus_timer >= bonus_interval:
                bonus_timer = 0
                bonus_obj = Bonus()

            # --- Bullets update ---
            for b in bullets[:]:
                b.update()
                b.draw(screen)
                if b.x > WIDTH + 100:
                    bullets.remove(b)

            # --- Ghosts update ---
            for g in ghosts[:]:
                g.update()
                g.draw(screen)
                # Castle collision
                if g.x < 70:
                    ghosts.remove(g)
                    castle_hp -= 1
                    if castle_hp <= 0:
                        game_over = True
                    continue

                # Player collision
                if player.get_rect().colliderect(g.get_rect()):
                    game_over = True

                # Bullet collision
                for b in bullets[:]:
                    if b.get_rect().colliderect(g.get_rect()):
                        ghosts.remove(g)
                        if b in bullets: bullets.remove(b)
                        score += 1
                        break

            # --- Bonus update ---
            if bonus_obj:
                bonus_obj.draw(screen)
                if player.get_rect().colliderect(bonus_obj.get_rect()):
                    player.ammo += 20
                    bonus_obj = None

            # --- Level Up ---
            if score >= required_score:
                level += 1
                score = 0
                required_score += 10
                ground_interval = max(20, ground_interval - 10)
                flying_interval = max(60, flying_interval - 20)
                if level > 5:
                    win_game = True

            # --- Draw Player & UI ---
            moving = keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]
            player.draw(screen, moving=moving)
            screen.blit(font.render(f"HP: {castle_hp}", True, (255, 0, 0)), (40, 30)) 
            screen.blit(font.render(f"HP: {castle_hp}", True, (255, 0, 0)), (40, 30))
            screen.blit(font.render(f"Ammo: {player.ammo}", True, (255, 255, 0)), (40, 60))
            screen.blit(font.render(f"Level: {level}", True, (0, 255, 0)), (40, 90))
            screen.blit(font.render(f"Score: {score}/{required_score}", True, (0, 255, 255)), (40, 120))

        # --- Victory Screen ---
        if win_game:
            pygame.mixer.music.stop()
            WIN_SOUND.play()
            win_font = pygame.font.SysFont('Arial', 60)
            small_font = pygame.font.SysFont('Arial', 30)
            screen.fill((0, 0, 0))
            text = win_font.render("VICTORY! YOU SAVED THE CASTLE!", True, (0, 255, 0))
            screen.blit(text, (screen.get_width()//2 - text.get_width()//2, 250))
            info = small_font.render("Press R key to restart...", True, (200, 200, 200))
            screen.blit(info, (screen.get_width()//2 - info.get_width()//2, 350))
            pygame.display.update()
            pygame.time.delay(500)
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting = False
                    elif event.key == pygame.K_r:
                        # Reset everything
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
                        pygame.mixer.music.play(-1)
                        waiting = False

        # --- Game Over ---
        if game_over:
            over_font = pygame.font.SysFont('Arial', 60)
            screen.blit(over_font.render("GAME OVER", True, (255, 0, 0)), (440, 300))
            pygame.display.update()
            pygame.time.delay(3000)
            running = False

        pygame.display.update()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
