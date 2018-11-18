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
    depth = 1

    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.rect = rect

        self.image = pygame.Surface(rect.size)
        self.image.fill(colors.grey)
        self.image.set_alpha(0)
        self.__visible = False

        self.__padding = 10
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
        self.__items = []

        icon_topleft = (self.__padding, self.__padding)
        for item in value:
            icon_rect = item.icon.get_rect(topleft=icon_topleft)
            if icon_rect.right > self.rect.right - self.__padding:
                icon_rect.topleft = (self.__padding, icon_rect.bottom + self.__padding)
            self.__items.append(InventoryMenuItem(self, icon_rect, item))
            icon_topleft = (icon_rect.right + self.__padding, icon_rect.top)
        if not self.__visible:
            self.image.set_alpha(0)


class InventoryMenuItem(pygame.sprite.Sprite):
    depth = 2

    def __init__(self, menu, rect, weapon):
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.__border_thickness = 4

        self.__menu = menu
        self.rect = rect.copy()
        self.rect.top += menu.rect.top
        self.rect.left += menu.rect.left
        self.weapon = weapon

        self.image = pygame.Surface([t + 2 * self.__border_thickness for t in weapon.icon.get_size()])
        self.image.fill(colors.black)
        self.image.blit(weapon.icon, (self.__border_thickness, self.__border_thickness))
