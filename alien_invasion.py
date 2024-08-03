import sys 
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    # manages the games behaviour.


    def __init__(self): 
        
        
        pygame.init()
        self.game_active = False

        # initialises the game
       
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.stats = GameStats(self)
        

        # self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        self.screen = pygame.display.set_mode((self.settings.screen_width,\
                                               self.settings.screen_height))
        

        pygame.display.set_caption("Alien Invasion")
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, "Play")

        

    def run_game(self): 
        # starts the main loop of the game

        while True: 
            self._check_events()
            
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)


    def _check_events(self): 
        # checks for user keyboard inputs

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    self._check_keydown(event)

                elif event.type == pygame.KEYUP:
                    self._check_keyup(event)

                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)


    def _check_keydown(self,event): 
        
        if event.key == pygame.K_RIGHT or  event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or  event.key == pygame.K_a:
            self.ship.moving_left = True

    def _check_keyup(self,event): 

        if event.key == pygame.K_RIGHT or  event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or  event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_q: 
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    

    def _check_play_button(self, mouse_pos): 
        
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            pygame.mouse.set_visible(False) 
            
            
            self.game_active = True

            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level() 
            self.sb.prep_ships()

    def _fire_bullet(self): 
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self): 

        
        self.bullets.update()

        for bullet in self.bullets.copy(): 
            if bullet.rect.bottom <= 0: 
                self.bullets.remove(bullet)
        # gets rid of the bullets and aliens on collision
        self._check_bullet_alien_collisions()

        

    def _update_screen(self): 
        # updates events on the screen.  
        
        # redraw the screen on each pass
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        # draws the ship and alien
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # draw the scoreboard 
        self.sb.show_score()

        # draw the play butto when the game is not active
        if not self.game_active: 
            self.play_button.draw_button()

        # make the most recent screen visible 
        pygame.display.flip()


    def _create_fleet(self): 
        # create the fleet of aliens. 

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        self.aliens.add(alien)

        # continues to add aliens until the screen is filled. 
        current_x, current_y = alien_width, alien_height

        while current_y < (self.settings.screen_height - 3*alien_height): 
            while current_x < (self.settings.screen_width - 2*alien_width): 
                self._create_alien(current_x, current_y)
                current_x += 2*alien_width
            current_x = alien_width
            current_y += 2*alien_height

    def _create_alien(self,x_position,y_position): 
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
    

    def _update_aliens(self): 
        self._check_fleet_edges()
        self.aliens.update()
        
        if pygame.sprite.spritecollideany(self.ship,self.aliens): 
            self._ship_hit()
        
        self._check_aliens_bottom()


    def _check_fleet_edges(self): 
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self): 
        for alien in self.aliens.sprites(): 
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1 


    def _check_bullet_alien_collisions(self): 
        # check for collisions between aliens and bullets. 
        collisions = pygame.sprite.groupcollide(
                                self.bullets, self.aliens, True, True)
        if collisions: 
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points* len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens: 
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level() 
            

    def _ship_hit(self): 
        if self.stats.ships_left > 0: 
            self.stats.ships_left -= 1 
            self.sb.prep_ships()

            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else: 
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self): 
        for alien in self.aliens.sprites(): 
            if alien.rect.bottom >= self.settings.screen_height: 
                self._ship_hit() 
                break


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
