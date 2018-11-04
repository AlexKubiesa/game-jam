import sys, pygame, math
from pygame.locals import *

# Game constants
black = 0, 0, 0
white = 255, 255, 255

SCREENRECT = Rect(0, 0, 800, 600)

class Player(pygame.sprite.Sprite):
    
    speed = 1

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.groups)
        size = 48, 48
        self.image = pygame.Surface(size)
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.midbottom = pos
        self.crosshair = Crosshair(self)
        self.facing = 1
    
    def step(self):
        keystate = pygame.key.get_pressed()
        hor = keystate[K_RIGHT] - keystate[K_LEFT]
        vert = keystate[K_DOWN] - keystate[K_UP]
        shoot = keystate[K_SPACE]
        if hor != 0:
            self._move_hor(hor)
            return True
        elif vert != 0:
            self._move_vert(vert)
            return True
        elif shoot:
            self._shoot()
            return False
        else:
            return True
    
    def _move_hor(self, direction):
        self.facing = direction
        self.rect.move_ip(direction * self.speed, 0)
        self.crosshair.reset()
    
    def _move_vert(self, direction):
        self.crosshair.move_vert(direction)
    
    def _shoot(self):
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
        self.angle = 0
    
    def reset(self):
        self.angle = 90 * (self.player.facing - 1)
    
    def move_vert(self, direction):
        self.angle += direction * self.player.facing
        
    def update(self):
        x, y = polar_to_cartesian(self.radius, self.angle)
        self.rect.center = (self.player.rect.centerx + x, self.player.rect.centery + y)
        
class Projectile(pygame.sprite.Sprite):
    
    size = 8, 8
    speed = 10
    
    def __init__(self, crosshair):
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect()
        self.velocity = polar_to_cartesian(self.speed, crosshair.angle)
        
        self.image.fill(white)
        self.rect.center = crosshair.rect.center
        
    def update(self):
        self.rect.move_ip(self.velocity[0], self.velocity[1])

def polar_to_cartesian(r, theta):
    """theta in degrees

    returns tuple; (float, float); (x,y)
    """
    x = r * math.cos(math.radians(theta))
    y = r * math.sin(math.radians(theta))
    return x, y
    
def main():
    pygame.init()
    
    # Initialise sprite groups
    all = pygame.sprite.RenderUpdates()
    
    # Assign default sprite groups to each sprite class
    Player.groups = all
    Crosshair.groups = all
    Projectile.groups = all
    
    screen = pygame.display.set_mode(SCREENRECT.size)
    background = screen.copy()
    
    clock = pygame.time.Clock()
    
    player1 = Player((SCREENRECT.centerx - 300, SCREENRECT.bottom))
    player2 = Player((SCREENRECT.centerx + 300, SCREENRECT.bottom))
    active_player = player1

    def next_player(player):
        if player == player1:
            return player2
        return player1
        
    def update():
        # Get input
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
        keystate = pygame.key.get_pressed()
        
        # Erase the old sprites
        all.clear(screen, background)
        
        # Update all the sprites
        all.update()
        
        # Draw the new sprites
        dirty = all.draw(screen)
        pygame.display.update(dirty)
        
        # Cap the framerate
        clock.tick(60)
    
    def move_to_next_player():
        nonlocal active_player
        for i in range(120):
            update()
        active_player = next_player(active_player)
    
    while 1:
        update()
        
        if (active_player.step() == False):
            move_to_next_player()
        

#call the "main" function if running this script
if __name__ == '__main__': main()