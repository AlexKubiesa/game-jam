import pygame
import colors
import controls


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

    def __init__(self, player_id, rect):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.__controls = controls.get_controls(player_id)
        self.rect = rect

        self.image = pygame.Surface(rect.size)
        self.image.fill(colors.grey)
        self.image.set_alpha(0)
        self.__visible = False

        self.__padding = 10
        self.__items = []
        self.__selected_index = None

    def get_visible(self):
        return self.__visible

    def set_visible(self, value):
        if value == self.__visible:
            return
        if value:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(0)
        self.__visible = value
        for menu_item in self.__items:
            menu_item.set_visible(value)

    def set_items(self, value):
        self.__items = []
        icon_topleft = (self.__padding, self.__padding)
        for item in value:
            icon_rect = item.icon.get_rect(topleft=icon_topleft)
            if icon_rect.right > self.rect.right - self.__padding:
                icon_rect.topleft = (self.__padding, icon_rect.bottom + self.__padding)
            menu_item = InventoryMenuItem(self, icon_rect, item)
            self.__items.append(menu_item)
            menu_item.set_visible(self.__visible)
            icon_topleft = (icon_rect.right + self.__padding, icon_rect.top)
        self.__select_item(0)

    def __select_item(self, index):
        if not (self.__selected_index is None):
            self.__items[self.__selected_index].set_selected(False)
        self.__selected_index = index
        self.__items[self.__selected_index].set_selected(True)

    def update(self):
        if not self.__visible:
            return
        button_states = controls.get_button_pressed(self.__controls)
        move_direction = button_states[controls.Button.RIGHT] - button_states[controls.Button.LEFT]
        if move_direction == 0:
            return
        new_index = self.__selected_index + move_direction
        if 0 <= new_index < len(self.__items):
            self.__select_item(new_index)

    def get_selected_item(self):
        if self.__selected_index is None:
            return None
        return self.__items[self.__selected_index].weapon


class InventoryMenuItem(pygame.sprite.Sprite):
    depth = 2

    def __init__(self, menu, rect, weapon):
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.__border_thickness = 2
        self.__default_border_color = colors.black
        self.__selected_border_color = colors.white

        self.__menu = menu
        self.rect = rect.copy()
        self.rect.top += menu.rect.top
        self.rect.left += menu.rect.left
        self.weapon = weapon

        self.__selected = False
        self.__border_color = self.__default_border_color

        self.image = pygame.Surface([t + 2 * self.__border_thickness for t in weapon.icon.get_size()])
        self.__update_image()

        self.__visible = False
        self.image.set_alpha(0)

    def __update_image(self):
        self.image.fill(self.__border_color)
        self.image.blit(self.weapon.icon, (self.__border_thickness, self.__border_thickness))

    def set_visible(self, value):
        if self.__visible == value:
            return
        self.__visible = value
        if self.__visible:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(0)

    def set_selected(self, value):
        self.__selected = value
        if self.__selected:
            self.__border_color = self.__selected_border_color
        else:
            self.__border_color = self.__default_border_color
        self.__update_image()

