import pygame

class Particle(pygame.sprite.Sprite):

    def __init__(self, position, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.position = pygame.math.Vector2(position)
        self.gravity = pygame.math.Vector2(0, 1)
        self.velocity = pygame.math.Vector2(0, 0)
        
    def update(self):
        self.position += self.velocity
        self.velocity += self.gravity