import sys, pygame, math
from pygame.locals import *

# Game constants
black = 0, 0, 0
white = 255, 255, 255

SCREENRECT = Rect(0, 0, 800, 600)

class Player(pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.groups)
        size = 48, 48
        self.image = pygame.Surface(size)
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.midbottom = pos
        
        
class Crosshair(pygame.sprite.Sprite):
    
    size = 8, 8
    radius = 100
    angle = 0
    
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.player = player
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect()
        
        self.image.fill(white)
        
        self.rect.center = (self.player.rect.centerx + self.radius, self.player.rect.centery)
        
    def move(self, direction):
        self.angle += direction
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
    
    player = Player(SCREENRECT.midbottom)
    crosshair = Crosshair(player)
    
    while 1:
        # Get input
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
        keystate = pygame.key.get_pressed()
        
        # Erase the old sprites
        all.clear(screen, background)
        
        # Update all the sprites
        all.update()
        
        # Move the crosshair
        direction = keystate[K_RIGHT] - keystate[K_LEFT]
        crosshair.move(direction)
        
        # Shoot a projectile
        if keystate[K_SPACE]:
            Projectile(crosshair)
        
        # Draw the new sprites
        dirty = all.draw(screen)
        pygame.display.update(dirty)
        
        # Cap the framerate
        clock.tick(60)

#call the "main" function if running this script
if __name__ == '__main__': main()