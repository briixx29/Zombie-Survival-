import pygame
import random
import math
import os

# ---------------- INIT ----------------
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(32)

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

# ---------------- HIGH SCORE ----------------
HIGH_SCORE_FILE = os.path.join(BASE_DIR, "highscore.txt")

def load_highscore():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

def save_highscore(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

# ---------------- FONTS ----------------
title_font = pygame.font.SysFont("arialblack", 85)
ui_font = pygame.font.SysFont("arialblack", 45)
small_font = pygame.font.SysFont("consolas", 32)
mini_font = pygame.font.SysFont("consolas", 20)

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

def draw_text_topleft(text, font, color, x, y):
    base = font.render(text, True, color)
    for ox, oy in [(-2,-2),(2,-2),(-2,2),(2,2),(0,-2),(0,2),(-2,0),(2,0)]:
        outline = font.render(text, True, BLACK)
        rect = outline.get_rect(topleft=(x+ox, y+oy))
        screen.blit(outline, rect)
    rect = base.get_rect(topleft=(x, y))
    screen.blit(base, rect)

# ---------------- SOUND ----------------
main_menu_music = os.path.join(SND_PATH, "mainMenu_sound.mp3")
menu_music = os.path.join(SND_PATH, "menu_music.mp3")
game_music = os.path.join(SND_PATH, "game_music.mp3")

hit_sound = pygame.mixer.Sound(os.path.join(SND_PATH, "hit.wav"))
heal_sound = pygame.mixer.Sound(os.path.join(SND_PATH, "heal.wav"))
speed_sound = pygame.mixer.Sound(os.path.join(SND_PATH, "speed.wav"))

try:
    ejeep_sound = pygame.mixer.Sound(os.path.join(SND_PATH, "ejeep.mp3"))
except:
    ejeep_sound = None

try:
    shot_sound = pygame.mixer.Sound(os.path.join(SND_PATH, "gun_shot.mp3"))
except:
    shot_sound = None

try:
    gameover_sound = pygame.mixer.Sound(os.path.join(SND_PATH, "gameover.mp3"))
except:
    gameover_sound = None

# ---------------- IMAGES ----------------
menu_bg = pygame.transform.scale(
    pygame.image.load(os.path.join(IMG_PATH, "menu_bg.png")), (WIDTH, HEIGHT)
)

bg_img = pygame.transform.scale(
    pygame.image.load(os.path.join(IMG_PATH, "background.png")), (WIDTH, HEIGHT)
)

try:
    bg_img2 = pygame.transform.scale(
        pygame.image.load(os.path.join(IMG_PATH, "bg2.png")), (WIDTH, HEIGHT)
    )
except:
    bg_img2 = pygame.Surface((WIDTH, HEIGHT))
    bg_img2.fill((50, 20, 20))

try:
    bg_img3 = pygame.transform.scale(
        pygame.image.load(os.path.join(IMG_PATH, "bg3.png")), (WIDTH, HEIGHT)
    )
except:
    try:
        bg_img3 = pygame.transform.scale(
            pygame.image.load(os.path.join(IMG_PATH, "bg.3.png")), (WIDTH, HEIGHT)
        )
    except:
        bg_img3 = pygame.Surface((WIDTH, HEIGHT))
        bg_img3.fill((20, 20, 50))

zombie_img = pygame.transform.scale(
    pygame.image.load(os.path.join(IMG_PATH, "zombie.png")).convert_alpha(), (60, 60)
)

heal_img = pygame.transform.scale(
    pygame.image.load(os.path.join(IMG_PATH, "heal.png")).convert_alpha(), (45, 45)
)

speed_img = pygame.transform.scale(
    pygame.image.load(os.path.join(IMG_PATH, "speed.png")).convert_alpha(), (45, 45)
)

try:
    gun_img = pygame.transform.scale(
        pygame.image.load(os.path.join(IMG_PATH, "gun.png")).convert_alpha(), (45, 45)
    )
except:
    gun_img = pygame.Surface((45, 45), pygame.SRCALPHA)
    pygame.draw.rect(gun_img, (150, 150, 150), (0, 0, 45, 45))

try:
    shield_img = pygame.transform.scale(
        pygame.image.load(os.path.join(IMG_PATH, "shield.png")).convert_alpha(), (45, 45)
    )
except:
    shield_img = pygame.Surface((45, 45), pygame.SRCALPHA)
    pygame.draw.rect(shield_img, (100, 100, 255), (0, 0, 45, 45))

try:
    ejeep_img_raw = pygame.image.load(os.path.join(IMG_PATH, "ejeep.png")).convert_alpha()
    ejeep_item_img = pygame.transform.scale(ejeep_img_raw, (80, 80))
    ejeep_wipe_img = pygame.transform.scale(ejeep_img_raw, (800, HEIGHT))
except:
    ejeep_item_img = pygame.Surface((80, 80), pygame.SRCALPHA)
    pygame.draw.rect(ejeep_item_img, (0, 255, 255), (0, 0, 80, 80))
    ejeep_wipe_img = pygame.Surface((800, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(ejeep_wipe_img, (0, 255, 255), (0, 0, 800, HEIGHT))

try:
    portal_img = pygame.transform.scale(
        pygame.image.load(os.path.join(IMG_PATH, "portal.png")).convert_alpha(), (200, 200)
    )
except:
    portal_img = pygame.Surface((200, 200), pygame.SRCALPHA)
    pygame.draw.circle(portal_img, (128, 0, 128), (100, 100), 100)

try:
    boss_img = pygame.transform.scale(
        pygame.image.load(os.path.join(IMG_PATH, "boss.png")).convert_alpha(), (150, 150)
    )
except:
    boss_img = pygame.Surface((150, 150), pygame.SRCALPHA)
    pygame.draw.rect(boss_img, (255, 0, 0), (0, 0, 150, 150))

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
global_volume = 1.0

def update_volume():
    pygame.mixer.music.set_volume(global_volume)
    hit_sound.set_volume(global_volume)
    heal_sound.set_volume(global_volume)
    speed_sound.set_volume(global_volume)
    if ejeep_sound: ejeep_sound.set_volume(global_volume)
    if shot_sound: shot_sound.set_volume(global_volume)
    if gameover_sound: gameover_sound.set_volume(global_volume)

def settings_menu():
    global global_volume
    in_settings = True
    while in_settings:
        screen.blit(menu_bg, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        draw_text_center("SETTINGS AND CONTROLS", ui_font, WHITE, (WIDTH//2, 100))
        
        # Volume
        draw_text_center(f"VOLUME: {int(global_volume * 100)}%", small_font, WHITE, (WIDTH//2, 220))
        
        minus_rect = pygame.Rect(WIDTH//2 - 200, 190, 60, 60)
        plus_rect = pygame.Rect(WIDTH//2 + 140, 190, 60, 60)
        
        mpos = pygame.mouse.get_pos()
        pygame.draw.rect(screen, (100, 100, 100) if minus_rect.collidepoint(mpos) else (80, 80, 80), minus_rect, border_radius=10)
        pygame.draw.rect(screen, (100, 100, 100) if plus_rect.collidepoint(mpos) else (80, 80, 80), plus_rect, border_radius=10)
        
        draw_text_center("-", ui_font, WHITE, (WIDTH//2 - 170, 220))
        draw_text_center("+", ui_font, WHITE, (WIDTH//2 + 170, 220))
        
        # Controls
        controls_rect = pygame.Rect(WIDTH//2 - 400, 290, 800, 240)
        pygame.draw.rect(screen, (30, 30, 30), controls_rect, border_radius=15)
        pygame.draw.rect(screen, (150, 150, 150), controls_rect, 2, border_radius=15)
        
        draw_text_center("CONTROLS", small_font, GREEN, (WIDTH//2, 320))
        draw_text_center("WASD or Arrows - Move character around the map.", mini_font, WHITE, (WIDTH//2, 360))
        draw_text_center("Auto Attack - Automatically fires gun bullets at zombies/boss.", mini_font, WHITE, (WIDTH//2, 395))
        draw_text_center("ESC - Pause the Game.", mini_font, WHITE, (WIDTH//2, 430))
        draw_text_center("Objective: Survive waves, grab items, enter portals, and defeat Boss!", mini_font, (200, 200, 200), (WIDTH//2, 465))
        
        # Back
        back_rect = pygame.Rect(WIDTH//2 - 100, 550, 200, 60)
        
        b_color = (150, 50, 50) if back_rect.collidepoint(mpos) else (100, 40, 40)
        pygame.draw.rect(screen, b_color, back_rect, border_radius=10)
        draw_text_center("BACK", ui_font, WHITE, (WIDTH//2, 580))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    in_settings = False
                elif minus_rect.collidepoint(event.pos):
                    global_volume = max(0.0, global_volume - 0.1)
                    update_volume()
                elif plus_rect.collidepoint(event.pos):
                    global_volume = min(1.0, global_volume + 0.1)
                    update_volume()

def pause_menu():
    pygame.mixer.music.pause()
    bg_surface = screen.copy()
    paused = True
    while paused:
        screen.blit(bg_surface, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        draw_text_center("PAUSED", title_font, RED, (WIDTH//2, 180))
        
        resume_rect = pygame.Rect(WIDTH//2 - 150, 300, 300, 80)
        settings_rect = pygame.Rect(WIDTH//2 - 150, 420, 300, 80)
        quit_rect = pygame.Rect(WIDTH//2 - 150, 540, 300, 80)
        
        mpos = pygame.mouse.get_pos()
        
        pygame.draw.rect(screen, (50, 150, 50) if resume_rect.collidepoint(mpos) else (30, 100, 30), resume_rect, border_radius=15)
        pygame.draw.rect(screen, (50, 50, 150) if settings_rect.collidepoint(mpos) else (30, 30, 100), settings_rect, border_radius=15)
        pygame.draw.rect(screen, (150, 50, 50) if quit_rect.collidepoint(mpos) else (100, 30, 30), quit_rect, border_radius=15)
        
        draw_text_center("RESUME", ui_font, WHITE, (WIDTH//2, 340))
        draw_text_center("SETTINGS", ui_font, WHITE, (WIDTH//2, 460))
        draw_text_center("QUIT TO MENU", small_font, WHITE, (WIDTH//2, 580))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.unpause()
                    return "resume"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_rect.collidepoint(event.pos):
                    pygame.mixer.music.unpause()
                    return "resume"
                elif settings_rect.collidepoint(event.pos):
                    settings_menu()
                elif quit_rect.collidepoint(event.pos):
                    return "quit"

def main_menu():
    update_volume()
    try:
        pygame.mixer.music.load(main_menu_music)
    except:
        pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play(-1)
    
    while True:
        screen.blit(menu_bg, (0, 0))
        
        draw_text_center("ZOMBIE SURVIVAL", title_font, RED, (WIDTH//2, 180))
        
        play_rect = pygame.Rect(WIDTH//2 - 150, 300, 300, 80)
        settings_rect = pygame.Rect(WIDTH//2 - 150, 420, 300, 80)
        quit_rect = pygame.Rect(WIDTH//2 - 150, 540, 300, 80)
        
        mpos = pygame.mouse.get_pos()
        
        pygame.draw.rect(screen, (50, 150, 50) if play_rect.collidepoint(mpos) else (30, 100, 30), play_rect, border_radius=15)
        pygame.draw.rect(screen, (50, 50, 150) if settings_rect.collidepoint(mpos) else (30, 30, 100), settings_rect, border_radius=15)
        pygame.draw.rect(screen, (150, 50, 50) if quit_rect.collidepoint(mpos) else (100, 30, 30), quit_rect, border_radius=15)
        
        draw_text_center("PLAY", ui_font, WHITE, (WIDTH//2, 340))
        draw_text_center("SETTINGS", ui_font, WHITE, (WIDTH//2, 460))
        draw_text_center("QUIT", ui_font, WHITE, (WIDTH//2, 580))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    return "play"
                elif settings_rect.collidepoint(event.pos):
                    settings_menu()
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit(); exit()

# ---------------- CHARACTER SELECT ----------------
def character_select():
    selected = None
    keys = list(characters.keys())
    char_names = ["Survivor", "Ranger", "Soldier", "Medic", "Sniper", "Heavy", "Ninja"]

    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play(-1)

    while selected is None:
        screen.blit(menu_bg, (0, 0))
        
        # Add a subtle dark overlay for better contrast
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        draw_text_center("CHOOSE YOUR CHARACTER", title_font, RED, (WIDTH//2, 120))
        draw_text_center("Click or Press 1 - 7 to Select", small_font, (200, 200, 200), (WIDTH//2, 620))

        spacing = 140
        start_x = WIDTH//2 - (len(keys) * spacing) // 2 + (spacing // 2)
        mpos = pygame.mouse.get_pos()
        
        char_rects = []

        for i, key in enumerate(keys):
            cx = start_x + i * spacing
            cy = HEIGHT // 2 + 30
            
            # Character card rect
            card_rect = pygame.Rect(0, 0, 120, 180)
            card_rect.center = (cx, cy)
            char_rects.append((card_rect, key))
            
            is_hovered = card_rect.collidepoint(mpos)
            
            # Draw card background
            bg_color = (80, 80, 80) if is_hovered else (40, 40, 40)
            pygame.draw.rect(screen, bg_color, card_rect, border_radius=15)
            
            # Draw border
            border_color = GREEN if is_hovered else (150, 150, 150)
            border_width = 4 if is_hovered else 2
            pygame.draw.rect(screen, border_color, card_rect, border_width, border_radius=15)
            
            # Draw character sprite
            char_img = characters[key]
            if is_hovered:
                # Slight scale up on hover
                char_img = pygame.transform.scale(char_img, (90, 80))
            
            img_rect = char_img.get_rect(center=(cx, cy - 25))
            screen.blit(char_img, img_rect)
            
            # Draw character name and number
            name_color = WHITE if is_hovered else (180, 180, 180)
            draw_text_center(char_names[i], mini_font, name_color, (cx, cy + 40))
            draw_text_center(f"[{i+1}]", mini_font, (200, 200, 100), (cx, cy + 65))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_7:
                    selected = characters[f"c{event.key - pygame.K_0}"]
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    for rect, key in char_rects:
                        if rect.collidepoint(event.pos):
                            selected = characters[key]

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
        "shield_end": 0,
        "gun_end": 0,
        "last_shot": 0,
        "lasers": [],
        "last_ticks": pygame.time.get_ticks(),
        "elapsed_ms": 0,
        "stage": 1,
        "ejeep_spawned_1": False,
        "ejeep_spawned_2": False,
        "ejeep_anim_x": -500,
        "ejeep_anim_active": False,
        "portal_active": False,
        "portal_pos": None,
        "boss_active": False,
        "boss_pos": [WIDTH//2 - 75, -200],
        "boss_health": 2000,
        "endgame_choice": False,
        "gun_stage1_count": 0,
        "gun_stage2_count": 0,
        "last_boss_gun_spawn": pygame.time.get_ticks(),
        "start_time": pygame.time.get_ticks(),
        "game_over": False,
        "win": False
    }

def spawn_zombie():
    side = random.choice(["top","bottom","left","right"])
    if side=="top": return [random.randint(0, WIDTH), 0]
    if side=="bottom": return [random.randint(0, WIDTH), HEIGHT]
    if side=="left": return [0, random.randint(0, HEIGHT)]
    return [WIDTH, random.randint(0, HEIGHT)]

def spawn_item():
    items_weighted = ["heal"]*4 + ["speed"]*4 + ["shield"]*2 + ["gun"]*1
    return {
        "type": random.choice(items_weighted),
        "pos": [random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)]
    }

# ---------------- GAME LOOP ----------------
running = True

while running:

    action = main_menu()
    if action == "quit":
        break

    player_img = character_select()
    high_score = load_highscore()

    pygame.mixer.music.stop()
    pygame.mixer.music.load(game_music)
    pygame.mixer.music.play(-1)

    state = reset_game()
    final_time = 0
    game_running = True

    while game_running:
        clock.tick(60)
        if state["stage"] == 1:
            screen.blit(bg_img, (0, 0))
        elif state["stage"] == 2:
            screen.blit(bg_img2, (0, 0))
        else:
            screen.blit(bg_img3, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if not state.get("game_over") and not state.get("endgame_choice"):
                    pause_start = pygame.time.get_ticks()
                    action = pause_menu()
                    if action == "quit":
                        game_running = False
                        break
                    
                    pause_duration = pygame.time.get_ticks() - pause_start
                    state["speed_boost_end"] += pause_duration
                    state["shield_end"] += pause_duration
                    state["gun_end"] += pause_duration
                    state["last_shot"] += pause_duration
                    state["last_ticks"] += pause_duration
                    state["last_boss_gun_spawn"] += pause_duration
                    state["start_time"] += pause_duration
                    for laser in state["lasers"]:
                        laser["time"] += pause_duration

        current_ticks = pygame.time.get_ticks()
        dt = current_ticks - state["last_ticks"]
        state["last_ticks"] = current_ticks

        if not state["game_over"] and not state["endgame_choice"]:
            if not state["portal_active"]:
                state["elapsed_ms"] += dt
            final_time = state["elapsed_ms"] // 1000

        draw_text_topright(f"TIME: {final_time}s", small_font, WHITE, WIDTH-20, 60)
        draw_text_topright(f"HIGH SCORE: {high_score}s", small_font, WHITE, WIDTH-20, 20)

        if state["endgame_choice"]:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            dialog_rect = pygame.Rect(WIDTH//2 - 400, HEIGHT//2 - 200, 800, 400)
            pygame.draw.rect(screen, (30, 30, 30), dialog_rect, border_radius=15)
            pygame.draw.rect(screen, (200, 200, 200), dialog_rect, 3, border_radius=15)

            draw_text_center("BOSS DEFEATED!", ui_font, GREEN, (WIDTH//2, HEIGHT//2 - 120))
            draw_text_center("The infection halts... for now.", small_font, (180, 180, 180), (WIDTH//2, HEIGHT//2 - 60))
            
            btn1_rect = pygame.Rect(WIDTH//2 - 350, HEIGHT//2 + 30, 300, 120)
            pygame.draw.rect(screen, (40, 100, 40), btn1_rect, border_radius=10)
            pygame.draw.rect(screen, (100, 255, 100), btn1_rect, 2, border_radius=10)
            draw_text_center("Press 1", ui_font, WHITE, (WIDTH//2 - 200, HEIGHT//2 + 70))
            draw_text_center("VICTORY (MENU)", small_font, (200, 255, 200), (WIDTH//2 - 200, HEIGHT//2 + 120))

            btn2_rect = pygame.Rect(WIDTH//2 + 50, HEIGHT//2 + 30, 300, 120)
            pygame.draw.rect(screen, (100, 40, 40), btn2_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 100, 100), btn2_rect, 2, border_radius=10)
            draw_text_center("Press 2", ui_font, WHITE, (WIDTH//2 + 200, HEIGHT//2 + 70))
            draw_text_center("ENTER ENDLESS", small_font, (255, 200, 200), (WIDTH//2 + 200, HEIGHT//2 + 120))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_1]:
                state["game_over"] = True
                state["win"] = True
                state["endgame_choice"] = False
            elif keys[pygame.K_2]:
                state["stage"] = "endless"
                state["zombies"] = []
                state["endgame_choice"] = False

        elif not state["game_over"]:

            speed = base_speed
            if current_ticks < state["speed_boost_end"]:
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

            if final_time >= 80 and not state["ejeep_spawned_1"] and state["stage"] == 1:
                state["ejeep_spawned_1"] = True
                state["items"].append({"type": "ejeep", "pos": [WIDTH//2, HEIGHT//2]})

            if final_time >= 160 and not state["ejeep_spawned_2"] and state["stage"] == 2:
                state["ejeep_spawned_2"] = True
                state["items"].append({"type": "ejeep", "pos": [WIDTH//2, HEIGHT//2]})

            if final_time >= 25 and state["gun_stage1_count"] == 0 and state["stage"] == 1:
                state["gun_stage1_count"] += 1
                state["items"].append({"type": "gun", "pos": [random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)]})

            if final_time >= 55 and state["gun_stage1_count"] == 1 and state["stage"] == 1:
                state["gun_stage1_count"] += 1
                state["items"].append({"type": "gun", "pos": [random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)]})

            if final_time >= 100 and state["gun_stage2_count"] == 0 and state["stage"] == 2:
                state["gun_stage2_count"] += 1
                state["items"].append({"type": "gun", "pos": [random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)]})

            if final_time >= 125 and state["gun_stage2_count"] == 1 and state["stage"] == 2:
                state["gun_stage2_count"] += 1
                state["items"].append({"type": "gun", "pos": [random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)]})

            if final_time >= 150 and state["gun_stage2_count"] == 2 and state["stage"] == 2:
                state["gun_stage2_count"] += 1
                state["items"].append({"type": "gun", "pos": [random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)]})

            if not state["portal_active"]:
                spawn_chance = 40
                if state["stage"] == 2: spawn_chance = 25
                if state["stage"] == 3: spawn_chance = 35
                if state["stage"] == "endless":
                    spawn_chance = max(2, 20 - ((state["elapsed_ms"] - 160000) // 5000))
                
                if random.randint(1, spawn_chance) == 1:
                    state["zombies"].append(spawn_zombie())

                if random.randint(1, 350) == 1:
                    state["items"].append(spawn_item())

            player_rect = pygame.Rect(state["player_x"], state["player_y"], player_size, player_size)

            zmb_spd = zombie_speed
            if state["stage"] == "endless":
                zmb_spd += min(5.0, (state["elapsed_ms"] - 160000) / 15000.0)

            for zombie in state["zombies"]:
                dx = state["player_x"] - zombie[0]
                dy = state["player_y"] - zombie[1]

                zombie[0] += dx * 0.01 * zmb_spd
                zombie[1] += dy * 0.01 * zmb_spd

                if dx < 0:
                    img = pygame.transform.flip(zombie_img, True, False)
                else:
                    img = zombie_img

                if player_rect.colliderect(pygame.Rect(zombie[0], zombie[1],55,55)):
                    if current_ticks > state["shield_end"]:
                        state["health"] -= 0.3
                        hit_sound.play()

                screen.blit(img, zombie)

            for item in state["items"][:]:
                item_size = 80 if item["type"] == "ejeep" else 35
                img_w, img_h = (80, 80) if item["type"] == "ejeep" else (45, 45)
                rect = pygame.Rect(item["pos"][0], item["pos"][1], item_size, item_size)

                # Draw pulsing highlight circle behind item
                cx = item["pos"][0] + img_w // 2
                cy = item["pos"][1] + img_h // 2
                pulse = abs(math.sin(current_ticks * 0.005)) * 5
                pygame.draw.circle(screen, (255, 255, 100), (cx, cy), int(img_w // 1.6 + pulse), 3)

                if item["type"] == "heal":
                    screen.blit(heal_img, item["pos"])
                elif item["type"] == "speed":
                    screen.blit(speed_img, item["pos"])
                elif item["type"] == "gun":
                    screen.blit(gun_img, item["pos"])
                elif item["type"] == "shield":
                    screen.blit(shield_img, item["pos"])
                elif item["type"] == "ejeep":
                    screen.blit(ejeep_item_img, item["pos"])

                if player_rect.colliderect(rect):
                    if item["type"] == "heal":
                        state["health"] = min(100, state["health"] + 25)
                        heal_sound.play()
                    elif item["type"] == "speed":
                        state["speed_boost_end"] = current_ticks + 5000
                        speed_sound.play()
                    elif item["type"] == "gun":
                        state["gun_end"] = current_ticks + 9000
                        speed_sound.play()
                    elif item["type"] == "shield":
                        state["shield_end"] = current_ticks + random.randint(5000, 10000)
                        speed_sound.play()
                    elif item["type"] == "ejeep":
                        state["ejeep_anim_active"] = True
                        state["ejeep_anim_x"] = -400
                        if ejeep_sound:
                            ejeep_sound.play()
                        else:
                            speed_sound.play()

                    state["items"].remove(item)

            # EJEEP Animation
            if state["ejeep_anim_active"]:
                state["ejeep_anim_x"] += 20
                screen.blit(ejeep_wipe_img, (state["ejeep_anim_x"], 0))
                wipe_rect = pygame.Rect(state["ejeep_anim_x"], 0, 800, HEIGHT)
                state["zombies"] = [z for z in state["zombies"] if not wipe_rect.colliderect(pygame.Rect(z[0], z[1], 55, 55))]
                
                if state["ejeep_anim_x"] > WIDTH:
                    state["ejeep_anim_active"] = False
                    if state["stage"] == 1:
                        state["portal_active"] = True
                        state["portal_pos"] = [WIDTH//2 - 100, HEIGHT//2 - 100]
                    elif state["stage"] == 2:
                        state["portal_active"] = True
                        state["portal_pos"] = [WIDTH//2 - 100, HEIGHT//2 - 100]

            # Portal logic
            if state["portal_active"]:
                screen.blit(portal_img, state["portal_pos"])
                if player_rect.colliderect(pygame.Rect(state["portal_pos"][0], state["portal_pos"][1], 200, 200)):
                    state["portal_active"] = False
                    if state["stage"] == 1:
                        state["stage"] = 2
                    elif state["stage"] == 2:
                        state["stage"] = 3
                        state["boss_active"] = True
                        state["boss_health"] = 2000

            # Boss Logic
            if state["boss_active"]:
                if current_ticks - state["last_boss_gun_spawn"] > 10000:
                    state["items"].append({"type": "gun", "pos": [random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)]})
                    state["last_boss_gun_spawn"] = current_ticks

                bx, by = state["boss_pos"]
                dx = state["player_x"] - bx
                dy = state["player_y"] - by
                dist = math.hypot(dx, dy)
                if dist != 0:
                    bx += (dx / dist) * 3.2
                    by += (dy / dist) * 3.2
                state["boss_pos"] = [bx, by]
                
                boss_rect = pygame.Rect(bx, by, 150, 150)
                screen.blit(boss_img, (bx, by))
                
                if player_rect.colliderect(boss_rect):
                    if current_ticks > state["shield_end"]:
                        state["health"] -= 0.6
                        hit_sound.play()
                
                if current_ticks - state["last_shot"] > 200:
                    state["lasers"].append({"start": (state["player_x"]+player_size//2, state["player_y"]+player_size//2), "end": (bx+75, by+75), "time": current_ticks})
                    state["boss_health"] -= 15
                    state["last_shot"] = current_ticks

                pygame.draw.rect(screen, RED, (WIDTH//2 - 200, 20, 400, 20))
                pygame.draw.rect(screen, GREEN, (WIDTH//2 - 200, 20, max(0, state["boss_health"])*0.4, 20))
                
                if state["boss_health"] <= 0:
                    state["boss_active"] = False
                    state["endgame_choice"] = True
                    state["zombies"] = []

            # Auto aim gun logic
            if current_ticks < state["gun_end"]:
                if len(state["zombies"]) > 0 and current_ticks - state["last_shot"] > 500:
                    px, py = state["player_x"] + player_size//2, state["player_y"] + player_size//2
                    closest_zombie = min(state["zombies"], key=lambda z: math.hypot(z[0] - state["player_x"], z[1] - state["player_y"]))
                    state["lasers"].append({"start": (px, py), "end": (closest_zombie[0] + 30, closest_zombie[1] + 30), "time": current_ticks})
                    state["zombies"].remove(closest_zombie)
                    state["last_shot"] = current_ticks
                    if shot_sound: 
                        shot_sound.stop()
                        shot_sound.play()
            else:
                if shot_sound: shot_sound.stop()

            # Draw lasers
            for laser in state["lasers"][:]:
                if current_ticks - laser["time"] < 150:
                    pygame.draw.line(screen, (255, 255, 0), laser["start"], laser["end"], 3)
                else:
                    state["lasers"].remove(laser)

            screen.blit(player_img, (state["player_x"], state["player_y"]))
            
            if pygame.time.get_ticks() < state["shield_end"]:
                pygame.draw.circle(screen, (100, 200, 255), (int(state["player_x"] + 40), int(state["player_y"] + 35)), 50, 4)

            pygame.draw.rect(screen, WHITE, (10,10,220,25))
            pygame.draw.rect(screen, GREEN, (10,10,state["health"]*2.2,25))
            draw_text_topleft(f"STAGE: {state['stage']}", ui_font, WHITE, 10, 45)

            if state["health"] <= 0:
                state["game_over"] = True
                pygame.mixer.music.stop()
                pygame.mixer.stop()
                if gameover_sound: gameover_sound.play()

        else:
            if state.get("win"):
                draw_text_center("VICTORY!", title_font, GREEN, (WIDTH//2, HEIGHT//2 - 140))
            else:
                draw_text_center("GAME OVER", title_font, RED, (WIDTH//2, HEIGHT//2 - 140))
            draw_text_center(f"You survived: {final_time}s", ui_font, WHITE, (WIDTH//2, HEIGHT//2))

            if final_time > high_score:
                high_score = final_time
                save_highscore(high_score)

            draw_text_center("Press R to Return to Menu", small_font, WHITE, (WIDTH//2, HEIGHT//2 + 90))

        pygame.display.update()

pygame.quit()