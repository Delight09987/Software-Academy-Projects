import pygame
import sys
import random
import tkinter as tk

pygame.init()
pygame.display.set_caption("Sidescrolling Shooter")
clock = pygame.time.Clock()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

class Player():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dy = 0
        self.dx = 0
        self.surface = pygame.image.load('player.png').convert()
        self.max_health = 20
        self.health = self.max_health
    
    def up(self):
        self.dy = -6

    def down(self):
        self.dy = 6

    def left(self):
        self.dx = -6

    def right(self):
        self.dx = 6

    def move(self):
        self.y = self.y + self.dy
        self.x = self.x + self.dx
        #Border Collision
        if self.y < 0:
            self.y = 0
            self.dy = 0
        elif self.y > 550:
            self.y = 550
            self.dy = 0

        if self.x < 0:
            self.x = 0
            self.dx = 0
        elif self.x > 750:
            self.x = 750
            self.dx = 0

    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def render(self):
        screen.blit(self.surface, (int (self.x), int(self.y)))
        pygame.draw.line(screen, GREEN, (int(self.x), int(self.y)), (int(self.x + (40 *(self.health/self.max_health))), int(self.y)), 2)

class Missile():
    def __init__(self):
        self.x = 0
        self.y = 1000
        self.dx = 0
        self.surface = pygame.image.load('missile.png').convert()
        self.state = "ready"

    def fire(self):
        self.state = "firing"
        self.x = player.x + 25
        self.y = player.y + 16
        self.dx = 10

    def move(self):
        if self.state == "firing":
            self.x = self.x + self.dx
        if self.x > 800:
            self.state = "ready"
            self.y = 1000

    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def render(self):
        screen.blit(self.surface, (int(self.x), int(self.y)))

missile_sound = pygame.mixer.Sound("missile.wav")
missile_sound.set_volume(0.2)

player = Player()
missiles = [Missile(),Missile(),Missile()]

def fire_missile():
    for missile in missiles:
        if missile.state == "ready":
            missile.fire()
            missile_sound.play()
            break
        

#While Loop for running the game 
while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.up()
            elif event.key == pygame.K_DOWN:
                player.down()
            elif event.key == pygame.K_LEFT:
                player.left()
            elif event.key == pygame.K_RIGHT:
                player.right()
            elif event.key == pygame.K_SPACE:
                fire_missile()

    player.move()
    for missile in missiles:
        missile.move()

    screen.fill(BLACK)

    player.render()
    for missile in missiles:
        missile.render()

    pygame.display.flip()

    clock.tick(30)

    
pygame.quit()

    
