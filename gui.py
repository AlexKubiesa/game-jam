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

        self.__back_image = pygame.Surface(rect.size)
        self.__back_image.fill(colors.grey)

        self.image = self.__back_image.copy()
        self.image.set_alpha(0)
        self.__visible = False

        self.__items = []

    def get_visible(self):
        return self.__visible

    def set_visible(self, value):
        if value == self.__visible:
            return
        if value:
            self.image.set_alpha(255)
            self.__visible = True
        else:
            self.image.set_alpha(0)
            self.__visible = False

    def set_items(self, value):
        self.__items = value
        self.image = self.__back_image.copy()
        for item in self.__items:
            self.image.blit(item.icon, (5, 5))
        if not self.__visible:
            self.image.set_alpha(0)
