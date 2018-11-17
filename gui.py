import pygame
import colors


class HealthBar(pygame.sprite.Sprite):

    def __init__(self, rect, max_health):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.rect = rect

        self.back_image = pygame.Surface(rect.size)
        self.front_image = self.back_image.copy()
        self.back_image.fill(colors.red)
        self.front_image.fill(colors.white)

        self.max_health = max_health
        self.health = max_health

        self.__update_image()

    def __update_image(self):
        self.image = self.back_image.copy()
        area = self.back_image.get_rect()
        area.width *= self.health / self.max_health
        self.image.blit(self.front_image, (0, 0), area)

    def change_health(self, health_change):
        self.health += health_change
        self.__update_image()


class InventoryMenu(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.rect = rect

        self.image = pygame.Surface(rect.size)
        self.image.fill(colors.grey)

        self.image.set_alpha(0)
        self.__visible = False

    def show(self):
        self.image.set_alpha(255)
        self.__visible = True

    def hide(self):
        self.image.set_alpha(0)
        self.__visible = False

    def is_visible(self):
        return self.__visible
