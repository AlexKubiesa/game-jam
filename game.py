import pygame
from pygame.locals import *

import physics

import random

# Game constants
black = 0, 0, 0
white = 255, 255, 255

FRAMERATE = 60
SCREEN_RECT = Rect(0, 0, 800, 600)
END_TURN_EVENT = pygame.USEREVENT
NEXT_TURN_EVENT = pygame.USEREVENT + 1


class Terrain(pygame.sprite.Sprite):

    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = image
        self.rect = image.get_rect()
        self.mask = pygame.mask.from_surface(image)

    def get_spawn_point(self, x):
        y = next(y for y in range(self.mask.get_size()[1]) if self.mask.get_at((x, y)) != 0)
        return x, y


class CircularListEnumerator:

    def __init__(self, list):
        self.__list = list
        self.__index = -1

    def next(self):
        self.__index = (self.__index + 1) % len(self.__list)
        return self.__list[self.__index]


class Player(pygame.sprite.Sprite):
    speed = 1

    def __init__(self, position, terrain):
        pygame.sprite.Sprite.__init__(self, self.groups)

        size = 48, 48
        self.image = pygame.Surface(size)
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.mask.fill()

        self.position = position
        self.__update_position()

        self.terrain = terrain

        if(self.position[0] > SCREEN_RECT.centerx):
            self.facing = 1
        else:
            self.facing = 0
        self.active = False
        self.crosshair = Crosshair(self)


    def __update_position(self):
        self.center = pygame.math.Vector2(self.position.x, self.position.y - self.rect.height / 2)
        self.rect.midbottom = self.position

    def update(self):
        if not self.active:
            return
        keystate = pygame.key.get_pressed()
        if(random.randint(0,1) == 0):
            self.__move(keystate[K_RIGHT] - keystate[K_LEFT])
            self.__aim(keystate[K_UP] - keystate[K_DOWN])
        else:
            self.__aim(keystate[K_UP] - keystate[K_DOWN])
            self.__move(keystate[K_RIGHT] - keystate[K_LEFT])
        if keystate[K_SPACE] != 0:
            self.__shoot()
            self.__end_turn()

    def __end_turn(self):
        self.active = False
        end_turn_event = pygame.event.Event(END_TURN_EVENT, player=self)
        pygame.event.post(end_turn_event)

    def __move(self, direction):
        if direction != 0:
            normal = get_collision_normal(self.terrain.mask, self.mask, self.center)
            if normal.length() == 0:
                # No collision
                change = pygame.math.Vector2(0, 1)
            else:
                # Collision
                angle = -90.0 * direction
                tangent = normal.rotate(angle)
                tangent.scale_to_length(self.speed)
                change = tangent
            self.position += change
            self.__update_position()
            self.crosshair.reset()

    def __aim(self, direction):
        if direction != 0:
            self.crosshair.move_vert(direction)

    def __shoot(self):
        Projectile(self.crosshair, self)


class Crosshair(pygame.sprite.Sprite):
    size = 8, 8
    radius = 100

    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.Surface(self.size)
        self.image.fill(white)

        self.rect = self.image.get_rect()

        self.player = player
        self.position = pygame.math.Vector2()
        self.__set_angle(self.player.facing*180)

    def __set_angle(self, new_angle):
        self.angle = new_angle
        self.position.from_polar((self.radius, self.angle))
        self.position += self.player.center
        self.rect.center = self.position

    def reset(self):
        self.__set_angle(self.angle)

    def move_vert(self, direction):
        self.__set_angle(self.angle + direction * (self.player.facing - 0.5) * 2)


class Projectile(physics.Particle):
    size = 8, 8
    speed = 10

    def __init__(self, crosshair, player):
        physics.Particle.__init__(self, crosshair.position, self.groups)

        self.player = player
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect()
        self.velocity.from_polar((self.speed, crosshair.angle))

        self.image.fill(white)
        self.rect.center = crosshair.rect.center

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        physics.Particle.update(self)
        self.rect.center = self.position
        if self.position[0] < 0 or self.position[0] > SCREEN_RECT[2] or self.position[1] < -SCREEN_RECT[3]:
            self.kill()



def get_collision_normal(mask, othermask, offset):
    x, y = (int(i) for i in offset)
    f_x = mask.overlap_area(othermask, (x + 1, y)) - mask.overlap_area(othermask, (x - 1, y))
    f_y = mask.overlap_area(othermask, (x, y + 1)) - mask.overlap_area(othermask, (x, y - 1))
    return pygame.math.Vector2(f_x, f_y)


def main():
    pygame.init()

    game_ended = False

    # Initialise sprite groups
    all = pygame.sprite.RenderUpdates()

    # Assign default sprite groups to each sprite class
    Terrain.groups = all
    Player.groups = all
    Crosshair.groups = all
    Projectile.groups = all

    screen = pygame.display.set_mode(SCREEN_RECT.size)
    background = screen.copy()

    terrain_image = pygame.image.load("terrain.png")
    terrain = Terrain(terrain_image)

    clock = pygame.time.Clock()

    player_xs = [SCREEN_RECT.centerx - 300, SCREEN_RECT.centerx + 300]
    players_list = [Player(pygame.math.Vector2(terrain.get_spawn_point(x)), terrain) for x in player_xs]
    for player in players_list:
        player.players_list = players_list
    players = CircularListEnumerator(players_list)
    current_player = players.next()
    current_player.active = True

    def process_event(event):
        nonlocal game_ended
        nonlocal players
        nonlocal current_player
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            game_ended = True
        if event.type == END_TURN_EVENT:
            current_player.active = False
            current_player = players.next()
            pygame.time.set_timer(NEXT_TURN_EVENT, 2000)
        if event.type == NEXT_TURN_EVENT:
            pygame.time.set_timer(NEXT_TURN_EVENT, 0)
            current_player.active = True

    while True:
        # Get input
        for event in pygame.event.get():
            process_event(event)

        if game_ended:
            return

        # Erase the old sprites
        all.clear(screen, background)

        # Update all the sprites
        all.update()

        # Draw the new sprites
        dirty = all.draw(screen)
        pygame.display.update(dirty)

        # Cap the framerate
        clock.tick(FRAMERATE)


# call the "main" function if running this script
if __name__ == '__main__':
    main()
