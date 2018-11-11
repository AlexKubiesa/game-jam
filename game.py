import sys, pygame, math
import physics
from pygame.locals import *

# Game constants
black = 0, 0, 0
white = 255, 255, 255

FRAMERATE = 60
SCREENRECT = Rect(0, 0, 800, 600)
END_TURN_EVENT = pygame.USEREVENT
NEXT_TURN_EVENT = pygame.USEREVENT + 1

class CircularListEnumerator:
    
    def __init__(self, list):
        self.__list = list
        self.__index = -1
        
    def next(self):
        self.__index = (self.__index + 1) % len(self.__list)
        return self.__list[self.__index]
        
class Player(pygame.sprite.Sprite):
    
    speed = 1

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        size = 48, 48
        self.image = pygame.Surface(size)
        self.image.fill(white)
        self.rect = self.image.get_rect()
        
        self.position = position
        self.__update_position()
        
        self.crosshair = Crosshair(self)
        self.facing = 1
        self.active = False
    
    def __update_position(self):
        self.center = pygame.math.Vector2(self.position.x, self.position.y - self.rect.height / 2)
        self.rect.midbottom = self.position
    
    def update(self):
        if not self.active:
            return
        keystate = pygame.key.get_pressed()
        self.__move(keystate[K_RIGHT] - keystate[K_LEFT])
        self.__aim(keystate[K_DOWN] - keystate[K_UP])
        if keystate[K_SPACE] != 0:
            self.__shoot()
            self.__end_turn()
    
    def __end_turn(self):
        self.active = False
        end_turn_event = pygame.event.Event(END_TURN_EVENT, player = self)
        pygame.event.post(end_turn_event)
    
    def __move(self, direction):
        if direction != 0:
            self.facing = direction
            self.position.x += direction * self.speed
            self.__update_position()
            self.crosshair.reset()
    
    def __aim(self, direction):
        if direction != 0:
            self.crosshair.move_vert(direction)
    
    def __shoot(self):
        Projectile(self.crosshair)
        
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
        self.__set_angle(0)
    
    def __set_angle(self, new_angle):
        self.angle = new_angle
        self.position.from_polar((self.radius, self.angle))
        self.position += self.player.center
        self.rect.center = self.position
    
    def reset(self):
        self.__set_angle(90 * (self.player.facing - 1))
    
    def move_vert(self, direction):
        self.__set_angle(self.angle + direction * self.player.facing)
        
class Projectile(physics.Particle):
    
    size = 8, 8
    speed = 10
    
    def __init__(self, crosshair):
        physics.Particle.__init__(self, crosshair.position, self.groups)
        
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect()
        self.velocity.from_polar((self.speed, crosshair.angle))
        
        self.image.fill(white)
        self.rect.center = crosshair.rect.center
        
    def update(self):
        physics.Particle.update(self)
        self.rect.center = self.position
    
def main():
    pygame.init()
    
    game_ended = False
    
    # Initialise sprite groups
    all = pygame.sprite.RenderUpdates()
    
    # Assign default sprite groups to each sprite class
    Player.groups = all
    Crosshair.groups = all
    Projectile.groups = all
    
    screen = pygame.display.set_mode(SCREENRECT.size)
    background = screen.copy()
    
    clock = pygame.time.Clock()
    
    players_list = []
    players_list.append(Player(pygame.math.Vector2(SCREENRECT.centerx - 300, SCREENRECT.bottom)))
    players_list.append(Player(pygame.math.Vector2(SCREENRECT.centerx + 300, SCREENRECT.bottom)))
    players = CircularListEnumerator(players_list)
    current_player = players.next()
    current_player.active = True
    
    def process_event(event):
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
        

#call the "main" function if running this script
if __name__ == '__main__': main()