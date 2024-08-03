import pygame
from pygame.sprite import Sprite

class Ship(Sprite): 

    def __init__(self,ai_game): 
        
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()


        # load the ship and its rectangle. 
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()


        # start the ship at the bottom of the screen. 
        self.rect.midbottom = self.screen_rect.midbottom


        # store a float for the horizontal position of the ship. 
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False


    def update(self): 
        if self.moving_right and self.rect.right < self.screen_rect.right: 
            self.rect.x += self.settings.ship_speed 
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.settings.ship_speed


    def blitme(self): 
        # draws the ship at its current location 
        self.screen.blit(self.image,self.rect)

    def center_ship(self): 
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

