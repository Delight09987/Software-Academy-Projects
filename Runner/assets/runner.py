import pygame as pg
import random

pg.init()

pg.mixer.music.load("assets/audio/music.wav")
pg.mixer.music.set_volume(0.03)
pg.mixer.music.play(loops=-1)
screen = pg.display.set_mode((600, 460))
pg.display.set_caption('Runner!')

jump_sound = pg.mixer.Sound("assets/audio/jump.wav")
jump_sound.set_volume(0.03)
clock = pg.time.Clock()
FPS = 60

highscore_file = "highscore.txt"
def save_highscore(highscore):
    # 'w' - open in write mode (so we can write to the file)
    # '+' - creates a new file, if one doesn't already exist
    with open(highscore_file, "w+") as file:
        file.write(str(int(highscore)))


def load_highscore():
    highscore = 0
    try:
        with open(highscore_file, "r") as file:
            highscore = int(file.read())
    except Exception as e:
        print("Unable to read highscore.")
    return highscore


highscore = load_highscore()

# Loading images
main_menu_bg = pg.image.load('assets/graphics/Sky.png')
main_menu_bg2 = pg.image.load('assets/graphics/ground.png')

player_stand = pg.image.load('assets/graphics/Player/player_stand.png')
player_stand = pg.transform.scale_by(player_stand, 2.7)

player_0 = pg.transform.scale_by(pg.image.load('assets/graphics/Player/player_walk_1.png'), 0.5)
player_1 = pg.transform.scale_by(pg.image.load('assets/graphics/Player/player_walk_2.png'), 0.5)


player_current_sprite = player_0
player_animation_time = 400 # in milliseconds
player_animation_start = pg.time.get_ticks()
# 'get_ticks' means 'get the time right now'

snail_1 = pg.image.load('assets/graphics/snail/snail1.png')
snail_2 = pg.image.load('assets/graphics/snail/snail2.png')

fly_1 = pg.image.load('assets/graphics/Fly/Fly1.png')
fly_2 = pg.image.load('assets/graphics/Fly/Fly2.png')

# Load fonts
main_menu_font = pg.font.Font('assets/font/Pixeltype.ttf', 70)
game_over_font = pg.font.Font('assets/font/Pixeltype.ttf', 120)
restart_font = pg.font.Font('assets/font/Pixeltype.ttf', 50)
score_font = pg.font.Font('assets/font/Pixeltype.ttf', 50)

GAME_MAIN_MENU = 0
GAME_PLAYING = 1
GAME_OVER = 2
game_mode = GAME_MAIN_MENU

floor_y = 300

score = 0
score_delta = 8.3333 
# 8.3 gets you 500 points every second
# this is because our game updates 60 times per second
# and 60*8.3 = 498
# NOTE: you can set the `score_delta` to whatever you want!

# Player variables
player_rect = player_current_sprite.get_rect()
player_rect.bottom = floor_y
player_rect.x += 18

player_y_velocity = 0
player_y_jump_velocity = -16
gravity = 6

can_jump = True

enemies_speed = 5

# Enemy class
class Enemy:
    def __init__(self, sprites):
        self.sprites = sprites
        self.sprite_index = 0
        self.anim_start = pg.time.get_ticks()
        self.rect = sprites[0].get_rect()
        self.animation_cooldown = 250
        self.rect.bottom = floor_y

        sw = screen.get_width()
        self.rect.left = sw + 200

    def update(self):
        self.rect.x -= enemies_speed

    def draw(self):
        time_now = pg.time.get_ticks()
        time_diff = time_now - self.anim_start
        if time_diff > self.animation_cooldown:
            self.sprite_index += 1
            if self.sprite_index > len(self.sprites) - 1:
                self.sprite_index = 0
            self.anim_start = time_now
        
        sprite = self.sprites[self.sprite_index]
        screen.blit(sprite, self.rect)

class Snail(Enemy):
    def __init__(self):
        sprites = [snail_1, snail_2]
        super().__init__(sprites)

class Fly(Enemy):
    def __init__(self):
        sprites = [fly_1, fly_2]
        super().__init__(sprites)

        self.rect.y -= 200

class EnemySpawner:
    def __init__(self):
        self.enemies = []

        # How often we spawn an enemy
        self.spawn_cooldown = 1000 # in milliseconds

        # Time at which we spawned the last enemy
        self.last_spawn_time = pg.time.get_ticks() # 'get_ticks' = 'time now'

    def can_spawn(self):
        # Return True if we should spawn an enemy
        # Otherwise, return False

        time_now = pg.time.get_ticks()
        time_diff = time_now - self.last_spawn_time
        return time_diff > self.spawn_cooldown
    
    def spawn_enemy(self):

        enemy_class = random.choice([Snail, Fly])
        enemy = enemy_class()
        self.enemies.append(enemy)

    def update(self):
        if self.can_spawn():
            self.spawn_enemy()
            self.last_spawn_time = pg.time.get_ticks()

        for enemy in self.enemies:
            enemy.update()

    def draw_all_enemies(self):
        for enemy in self.enemies:
            enemy.draw()

enemy_spawner = EnemySpawner()


running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if game_mode == GAME_MAIN_MENU:
                game_mode = GAME_PLAYING
                continue
            
            if game_mode == GAME_PLAYING:
                if event.key == pg.K_SPACE and can_jump:
                    player_y_velocity = player_y_jump_velocity
                    jump_sound.play()
                    can_jump = False # 

            if game_mode == GAME_OVER:
                if event.key == pg.K_r:
                    # Restart game!
                    enemy_spawner = EnemySpawner()
                    can_jump = True
                    player_y_velocity = 0
                    player_rect.bottom = floor_y
                    game_mode = GAME_PLAYING
                    score = 0
                    enemies_speed = 5

    # Drawing
    
    # Playing
    if game_mode == GAME_PLAYING:

        # TRY EITHER OF THESE SEE WHICH ONE YOU PREFER
        # FEEL FREE TO CHANGE THE ACTUAL VALUES
        #enemies_speed *= 1.001
        enemies_speed += 0.001
        score += score_delta

        main_menu_bg_rect = main_menu_bg.get_rect()
        screen.blit(main_menu_bg, (0,0))
        screen.blit(main_menu_bg2, main_menu_bg_rect.bottomleft)

        # Update enmies
        enemy_spawner.update()

        # Update player animation
        time_now = pg.time.get_ticks()
        time_diff = time_now - player_animation_start
        if time_diff > player_animation_time:
            player_animation_start += player_animation_time
            # Update animation
            if player_current_sprite == player_0:
                player_current_sprite = player_1
            else:
                player_current_sprite = player_0

        floor_y = main_menu_bg_rect.bottom
        
        player_y_velocity += gravity * 0.1
        player_rect.y += player_y_velocity

        if player_rect.bottom > floor_y:
            player_y_velocity = 0
            player_rect.bottom = floor_y
            can_jump = True

        for enemy in enemy_spawner.enemies:
            if player_rect.colliderect(enemy.rect):
                #print("Player should lose!")
                game_mode = GAME_OVER
                if score > highscore:
                    highscore = score
                    save_highscore(highscore)
        
        screen.blit(player_current_sprite, player_rect)

        enemy_spawner.draw_all_enemies()

        text = f"Score: {int(score)}"
        surface = score_font.render(text, True, (255,255,255))
        rect = surface.get_rect()
        rect.bottom = screen.get_height() - 10
        rect.left += 10
        
        screen.blit(surface, rect)

    # Main menu
    if game_mode == GAME_MAIN_MENU:
        main_menu_bg_rect = main_menu_bg.get_rect()
        screen.blit(main_menu_bg, (0,0))
        screen.blit(main_menu_bg2, main_menu_bg_rect.bottomleft)

        pos = (screen.get_width() // 2, screen.get_height() // 2)
        rect = player_stand.get_rect()
        rect.center = pos
        screen.blit(player_stand, rect)

        # Draw text
        text = 'Press any key to start'
        text_img = main_menu_font.render(text, True, pg.Color('white'))
        text_rect = text_img.get_rect()
        text_rect.bottom = screen.get_height() - 10
        text_rect.centerx = screen.get_width() // 2
        screen.blit(text_img, text_rect)

    if game_mode == GAME_OVER:
        main_menu_bg_rect = main_menu_bg.get_rect()
        screen.blit(main_menu_bg, (0,0))
        screen.blit(main_menu_bg2, main_menu_bg_rect.bottomleft)

        text = 'Game Over'
        text_color = (255,0,0)
        surface = game_over_font.render(text, True, text_color)
        rect = surface.get_rect()
        rect.centerx = screen.get_width() // 2
        rect.centery = screen.get_height() // 2
        screen.blit(surface, rect)

        text = "Press 'R' to restart"
        text_color = (255,255,255)
        surface = restart_font.render(text, True, text_color)
        rect = surface.get_rect(top = rect.bottom, centerx = rect.centerx)
        rect.y += 25
        screen.blit(surface, rect)

        # Draw score
        text = f"Score: {int(score)}"
        text_color = (255,255,255)
        surface = restart_font.render(text, True, text_color)
        rect = surface.get_rect(top = rect.bottom, centerx = rect.centerx)
        rect.y += 25
        screen.blit(surface, rect)

        # Draw highscore
        text = f"Highcore: {int(highscore)}"
        text_color = (255,255,255)
        surface = restart_font.render(text, True, text_color)
        rect = surface.get_rect(top = rect.bottom, centerx = rect.centerx)
        rect.y += 25
        screen.blit(surface, rect)


    pg.display.update()
    clock.tick(FPS)

pg.quit()