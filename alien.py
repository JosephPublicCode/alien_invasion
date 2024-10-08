import pygame
from pygame.sprite import Sprite

class Alien(Sprite): 
    # a class to represent an alien. 

    def __init__(self, ai_game): 
        
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # load image
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # initialize alien position
        self.rect.x = self.rect.width 
        self.rect.y = self.rect.height 

        # record the horizontal position
        self.x = float(self.rect.x)

    def update(self): 
        self.x += self.settings.alien_speed*self.settings.fleet_direction
        self.rect.x = self.x 

    def check_edges(self): 
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
    
