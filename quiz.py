import pygame
import pygame.freetype
import random

pygame.init()
DS = pygame.display.set_mode((600,600))
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pygame.display.flip()








