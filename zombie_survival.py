import pygame
import random
import os

# ---------------- INIT ----------------
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survival")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (220, 60, 60)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()

# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(__file__)
IMG_PATH = os.path.join(BASE_DIR, "assets", "images")
SND_PATH = os.path.join(BASE_DIR, "assets", "sounds")

# ---------------- FONTS ----------------
title_font = pygame.font.SysFont("arialblack", 85)
ui_font = pygame.font.SysFont("arialblack", 45)
small_font = pygame.font.SysFont("consolas", 32)

# ---------------- TEXT ----------------
def draw_text_center(text, font, color, center):
    base = font.render(text, True, color)
    for ox, oy in [(-2,-2),(2,-2),(-2,2),(2,2),(0,-2),(0,2),(-2,0),(2,0)]:
        outline = font.render(text, True, BLACK)
        rect = outline.get_rect(center=(center[0]+ox, center[1]+oy))
        screen.blit(outline, rect)
    rect = base.get_rect(center=center)
    screen.blit(base, rect)

def draw_text_topright(text, font, color, x, y):
    base = font.render(text, True, color)
    for ox, oy in [(-2,-2),(2,-2),(-2,2),(2,2),(0,-2),(0,2),(-2,0),(2,0)]:
        outline = font.render(text, True, BLACK)
        rect = outline.get_rect(topright=(x+ox, y+oy))
        screen.blit(outline, rect)
    rect = base.get_rect(topright=(x, y))
    screen.blit(base, rect)

# ---------------- SOUND ----------------
menu_music = os.path.join(SND_PATH, "menu_music.mp3")
game_music = os.path.join(SND_PATH, "game_music.mp3")

hit_sound = pygame.mixer.Sound(os.path.join(SND_PATH, "hit.wav"))
heal_sound = pygame.mixer.Sound(os.path.join(SND_PATH, "heal.wav"))
speed_sound = pygame.mixer.Sound(os.path.join(SND_PATH, "speed.wav"))

# ---------------- IMAGES ----------------
menu_bg = pygame.transform.scale(
    pygame.image.load(os.path.join(IMG_PATH, "menu_bg.png")), (WIDTH, HEIGHT)
)

bg_img = pygame.transform.scale(
    pygame.image.load(os.path.join(IMG_PATH, "background.png")), (WIDTH, HEIGHT)
)

# ONE zombie image (facing RIGHT)
zombie_img = pygame.transform.scale(
    pygame.image.load(os.path.join(IMG_PATH, "zombie.png")).convert_alpha(), (60, 60)
)

heal_img = pygame.transform.scale(
    pygame.image.load(os.path.join(IMG_PATH, "heal.png")).convert_alpha(), (35, 35)
)

speed_img = pygame.transform.scale(
    pygame.image.load(os.path.join(IMG_PATH, "speed.png")).convert_alpha(), (35, 35)
)

characters = {
    f"c{i}": pygame.transform.scale(
        pygame.image.load(os.path.join(IMG_PATH, f"char{i}.png")), (80, 70)
    )
    for i in range(1, 8)
}

# ---------------- SETTINGS ----------------
player_size = 65
base_speed = 6
zombie_speed = 2.6

# ---------------- CHARACTER SELECT ----------------
def character_select():
    selected = None
    keys = list(characters.keys())

    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play(-1)

    while selected is None:
        screen.blit(menu_bg, (0, 0))

        draw_text_center("CHOOSE YOUR CHARACTER", ui_font, WHITE, (WIDTH//2, 100))
        draw_text_center("Press 1 - 7 to Select", small_font, WHITE, (WIDTH//2, 600))

        spacing = 120
        start_x = WIDTH//2 - (len(keys)*spacing)//2

        for i, key in enumerate(keys):
            screen.blit(characters[key], (start_x + i*spacing, 300))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_7:
                    selected = characters[f"c{event.key - pygame.K_0}"]

    return selected

# ---------------- RESET ----------------
def reset_game():
    return {
        "player_x": WIDTH//2,
        "player_y": HEIGHT//2,
        "health": 100,
        "zombies": [],
        "items": [],
        "speed_boost_end": 0,
        "start_time": pygame.time.get_ticks(),
        "game_over": False
    }

def spawn_zombie():
    side = random.choice(["top","bottom","left","right"])
    if side=="top": return [random.randint(0, WIDTH), 0]
    if side=="bottom": return [random.randint(0, WIDTH), HEIGHT]
    if side=="left": return [0, random.randint(0, HEIGHT)]
    return [WIDTH, random.randint(0, HEIGHT)]

def spawn_item():
    return {
        "type": random.choice(["heal", "speed"]),
        "pos": [random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)]
    }

# ---------------- GAME LOOP ----------------
running = True

while running:

    player_img = character_select()

    pygame.mixer.music.stop()
    pygame.mixer.music.load(game_music)
    pygame.mixer.music.play(-1)

    state = reset_game()
    final_time = 0
    game_running = True

    while game_running:
        clock.tick(60)
        screen.blit(bg_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_running = False

        # TIMER
        if not state["game_over"]:
            final_time = (pygame.time.get_ticks() - state["start_time"]) // 1000

        draw_text_topright(f"TIME: {final_time}s", ui_font, WHITE, WIDTH-20, 20)

        if not state["game_over"]:

            speed = base_speed
            if pygame.time.get_ticks() < state["speed_boost_end"]:
                speed += 4

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                state["player_x"] -= speed
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                state["player_x"] += speed
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                state["player_y"] -= speed
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                state["player_y"] += speed

            state["player_x"] = max(0, min(WIDTH-player_size, state["player_x"]))
            state["player_y"] = max(0, min(HEIGHT-player_size, state["player_y"]))

            if random.randint(1,50) == 1:
                state["zombies"].append(spawn_zombie())

            if random.randint(1,200) == 1:
                state["items"].append(spawn_item())

            player_rect = pygame.Rect(state["player_x"], state["player_y"], player_size, player_size)

            # 🧟 ZOMBIES (WITH FLIP)
            for zombie in state["zombies"]:
                dx = state["player_x"] - zombie[0]
                dy = state["player_y"] - zombie[1]

                zombie[0] += dx * 0.01 * zombie_speed
                zombie[1] += dy * 0.01 * zombie_speed

                # FLIP IMAGE
                if dx < 0:
                    img = pygame.transform.flip(zombie_img, True, False)
                else:
                    img = zombie_img

                if player_rect.colliderect(pygame.Rect(zombie[0], zombie[1],55,55)):
                    state["health"] -= 0.3
                    hit_sound.play()

                screen.blit(img, zombie)

            # ITEMS
            for item in state["items"][:]:
                rect = pygame.Rect(item["pos"][0], item["pos"][1], 35, 35)

                if item["type"] == "heal":
                    screen.blit(heal_img, item["pos"])
                else:
                    screen.blit(speed_img, item["pos"])

                if player_rect.colliderect(rect):
                    if item["type"] == "heal":
                        state["health"] = min(100, state["health"] + 25)
                        heal_sound.play()
                    else:
                        state["speed_boost_end"] = pygame.time.get_ticks() + 5000
                        speed_sound.play()

                    state["items"].remove(item)

            screen.blit(player_img, (state["player_x"], state["player_y"]))

            pygame.draw.rect(screen, WHITE, (10,10,220,25))
            pygame.draw.rect(screen, GREEN, (10,10,state["health"]*2.2,25))

            if state["health"] <= 0:
                state["game_over"] = True
                pygame.mixer.music.stop()

        else:
            draw_text_center("GAME OVER", title_font, RED, (WIDTH//2, HEIGHT//2 - 140))
            draw_text_center(f"You survived: {final_time}s", ui_font, WHITE, (WIDTH//2, HEIGHT//2))
            draw_text_center("Press R to Return to Menu", small_font, WHITE, (WIDTH//2, HEIGHT//2 + 90))

        pygame.display.update()

pygame.quit()