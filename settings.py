class Settings: 

    def __init__(self): 
    # defines all of the static values. 

        # Ship Settings
        self.ship_limit = 3 
        self.ships_left = 3 

        # Bullet Settings
        self.bullet_width = 4
        self.bullet_height = 20 
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3 

        # Alien Settings
        self.fleet_drop_speed = 10
        self.fleet_direction = 1 

        #  Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        # game ramp up
        self.speedup_scale = 1.2
        self.score_scale = 1.5

        # scoring settings 
        self.alien_points = 50 


        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
    # defines the dynamic values
        self.ship_speed = 4
        self.bullet_speed = 4
        self.alien_speed = 6

        self.fleet_direction = 1

    def increase_speed(self): 
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *=self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points*self.score_scale)