import pygame
import sys

pygame.init()
pygame.display.set_caption("sidescrolling Shooter")
clock = pygame.time.Clock()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
