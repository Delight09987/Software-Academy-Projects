# create a game window

import pygame as pg
import sys
import os

pg.init()

flag = pg.NOFRAME
 
screen = pg.display.set_mode((700, 500), flag)  # Fullscreen mode will use the full display resolution
background = pg.Color(0,0,0) # black colour
screen.fill(background)

file_path = os.path.join("net.jpg")

net = pg.image.load("net.jpg")

def net(net):
    size = pg.transform.scale(net, (400,600))
    screen.blit(size, (0,0))

pg.display.update() # updates the window 

clock = pg.time.Clock()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    clock.tick(60)  # Limit frame rate to 60 FPS

pg.quit()
sys.exit()



