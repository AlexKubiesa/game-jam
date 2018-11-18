import pygame
import colors


class Weapon:

    def __init__(self, color):
        self.color = color
        self.icon = pygame.Surface((20, 20))
        self.icon.fill(color)


bazooka = Weapon(colors.red)
mortar = Weapon(colors.yellow)
grenade = Weapon(colors.green)
