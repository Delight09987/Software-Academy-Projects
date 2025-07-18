import random
import pygame as pg
from pygame.math import Vector2 as v2
pg.init()

SCALE = 0.5

# Make sure you enable this for testing only!
DEBUG = True

clock = pg.time.Clock()

screen = pg.display.set_mode(v2(1280, 720) * SCALE)
pg.display.set_caption("!! Geometry Bash !!")

bg_color = (67, 61, 68)

floor = pg.Rect(0,0, screen.get_width(), 100*SCALE)
floor.bottom = screen.get_height()

player = pg.Rect(0, 0, 60*SCALE, 60*SCALE)
player.bottom = floor.top
player.left = 40*SCALE

# Jumping parameters - CHANGE THESE as you wish
gravity = 1.5           # how fast you come down
jump_velocity = -30     # how fast you go up/how high you go
max_fall_speed = 30     # limits how fast you can come down
coyote_time = 5       

# Jumping state variables
y_speed = 0
on_ground = True
jump_pressed = False
coyote_timer = 0

# Platforms
platforms = []

# Debug variables for testing
x_speed = 10

dt = 0 # delta time

# Platform spawn timer
spawn_timer = 0
spawn_interval = 2 # Seconds between spawns

environment_speed = 8 # CHANGE THIS TO WHATEVER YOU WANT

max_jump_size = 250


spike_timer = 2000
spike_spawn_time = 0 

def draw_floor():
    color = (127, 67, 188)
    pg.draw.rect(screen, color, floor)

def draw_player():
    color = (167, 92, 92)
    pg.draw.rect(screen, color, player)

spikes = []
def add_spikes(x):
    spikes.append(x)

def rect_from_spike(spike):
    r = pg.Rect(0,0,50,50)
    r.left = spike
    r.bottom = floor.top
    return r

add_spikes(400)
add_spikes(200)


dt = 0
running = True
while running:
    for e in pg.event.get():
        if e.type == pg.QUIT: running = False

    # Input
    keys = pg.key.get_pressed()

    if keys[pg.K_SPACE] and coyote_timer > 0:
        y_speed = jump_velocity
        on_ground = False
        jump_pressed = True
        coyote_timer = 0

    if DEBUG:
        x_move = 0
        if keys[pg.K_a]: 
            x_move = -1
        if keys[pg.K_d]:
            x_move = 1
        player.x += x_move * x_speed
        
    y_speed += gravity
    if y_speed > max_fall_speed:
        y_speed = max_fall_speed
    player.y += y_speed

    if player.bottom > floor.top:
        player.bottom = floor.top
        y_speed = 0
        coyote_timer = coyote_time
    else:
        coyote_timer -= dt


    for platform in platforms:

        platform.x -= environment_speed * SCALE
        
        if player.colliderect(platform):
            if y_speed > 0: # is the player moving downwards?
                player.bottom = platform.top
                coyote_timer = coyote_time

        time_now  = pg.time.get_ticks()
        time_diff = time_now - spike_spawn_time
        if time_diff >= spike_timer:
            add_spikes(screen.get_width() + 69)
            spike_spawn_time = time_now

    for i in range(len(spikes)):
        spikes[i] -= 10
    
    # Spawn platforms
    spawn_timer += dt
    if spawn_timer >= spawn_interval:
        spawn_timer = 0

        # We should spawn a platform!
        platform = pg.Rect(0,0, 0,0)
        platform.width = 100
        platform.height = 30
        platform.left = screen.get_width()
        platform.bottom = floor.top - 250
        for i in range(4):
            if platform.bottom < floor.top - 30:
                platforms.append(platform.copy())
            platform.y += random.randint(-300, max_jump_size)
            platform.x += (i+1) * (platform.width + 25)

    # Draw
    screen.fill(bg_color)
    draw_floor()
    draw_player()

    for platform in platforms:
        pg.draw.rect(screen, pg.Color("red"), platform)
    # drawing a triangle for spikes
    for spike in spikes:
        rect = rect_from_spike(spike)
        x = rect.left * SCALE
        y = rect.bottom 
        w = rect.width * SCALE
        h = rect.height * SCALE
        points = [
            (x,y), 
            (x + w, y),
            (x + w  //2, y-h)
        ]
            
        pg.draw.polygon(screen, pg.Color("red"),points, 0) 
        pg.draw.aalines(screen, pg.Color("red"), True, points)
    pg.display.update()

    dt = clock.tick(60) / 1000

pg.quit()















































