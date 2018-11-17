import pygame
import random


class Weapon:

    def __init__(self):
        self.icon = pygame.Surface((20, 20))
        self.icon.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
