import pygame
import random

# Initialize
pygame.init()
pygame.mixer.init()  # FOR SOUND

# Screen
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survival")

# Colors
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Load Images
player_img = pygame.image.load("player.png").convert_alpha()
zombie_img = pygame.image.load("zombie.png").convert_alpha()
bg_img = pygame.image.load("background.png").convert()

# Resize images
player_size = 60
zombie_size = 50

player_img = pygame.transform.scale(player_img, (player_size, player_size))
zombie_img = pygame.transform.scale(zombie_img, (zombie_size, zombie_size))
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

# LOAD SOUNDS
pygame.mixer.music.load("bg_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # LOOP FOREVER

hit_sound = pygame.mixer.Sound("hit.wav")
hit_sound.set_volume(0.7)

# Player
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 6
health = 100

# Zombies
zombies = []
zombie_speed = 2.5

# Font
font = pygame.font.SysFont(None, 60)

# Clock
clock = pygame.time.Clock()

# Spawn zombie
def spawn_zombie():
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        return [random.randint(0, WIDTH), 0]
    elif side == "bottom":
        return [random.randint(0, WIDTH), HEIGHT]
    elif side == "left":
        return [0, random.randint(0, HEIGHT)]
    else:
        return [WIDTH, random.randint(0, HEIGHT)]

# Game loop
running = True
game_over = False

while running:
    clock.tick(60)

    # Background
    screen.blit(bg_img, (0, 0))

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_y -= player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_y += player_speed

        # Keep inside screen
        player_x = max(0, min(WIDTH - player_size, player_x))
        player_y = max(0, min(HEIGHT - player_size, player_y))

        # Spawn zombies
        if random.randint(1, 50) == 1:
            zombies.append(spawn_zombie())

        # Move zombies
        for zombie in zombies:
            if zombie[0] < player_x:
                zombie[0] += zombie_speed
            if zombie[0] > player_x:
                zombie[0] -= zombie_speed
            if zombie[1] < player_y:
                zombie[1] += zombie_speed
            if zombie[1] > player_y:
                zombie[1] -= zombie_speed

        # Collision
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        for zombie in zombies:
            zombie_rect = pygame.Rect(zombie[0], zombie[1], zombie_size, zombie_size)
            if player_rect.colliderect(zombie_rect):
                health -= 0.3
                hit_sound.play()  # PLAY SOUND WHEN HIT

        # Draw player
        screen.blit(player_img, (player_x, player_y))

        # Draw zombies
        for zombie in zombies:
            screen.blit(zombie_img, (zombie[0], zombie[1]))

        # Health bar
        pygame.draw.rect(screen, WHITE, (10, 10, 200, 20))
        pygame.draw.rect(screen, GREEN, (10, 10, max(0, health * 2), 20))

        # Game Over
        if health <= 0:
            game_over = True
            pygame.mixer.music.stop()  # STOP MUSIC

    else:
        text = font.render("GAME OVER", True, WHITE)
        screen.blit(text, (WIDTH // 2 - 170, HEIGHT // 2 - 30))

    pygame.display.update()

pygame.quit()