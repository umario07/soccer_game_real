import pygame
# imports pygame library for game development
from settings import *
# imports all variables/constants from settings file

class Ball(pygame.sprite.Sprite):
    # inherits from pygame's Sprite class
    # handles ball movement, shooting, bouncing mechanics
    

    #Made by ChatGPT: intended to change sprite icons
    def __init__(self):
        super().__init__()
        # initializes parent Sprite class
        
        try:
            original_image = pygame.image.load("assets/ball.png").convert_alpha()
            self.image = pygame.transform.scale(original_image, (BALL_RADIUS * 3, BALL_RADIUS * 3))

        except Exception as e:
            print(f"Error loading ball image: {e}")
            self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
            pygame.draw.circle(self.image, WHITE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)

        
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        # creates rectangle for collision detection
        # positions ball at bottom center of screen
        
        self.speed = 0
        # initial vertical speed
        self.shot = False
        # tracks if ball has been shot
        self.horizontal_speed = 0
        # initial horizontal speed for bouncing
        self.bounce_speed = 8
        # speed applied after hitting goalie
        self.gravity = 0.2
        # gravity effect on ball trajectory

    def update(self):
        if self.shot:
            # only updates if ball has been shot
            self.rect.y += self.speed
            # updates vertical position
            self.rect.x += self.horizontal_speed
            # updates horizontal position
            
            self.speed += self.gravity
            # applies gravity effect
            
            if (self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT or 
                self.rect.left < 0 or self.rect.right > SCREEN_WIDTH):
                # checks if ball is off screen
                self.reset()
                # resets ball position if off screen

    def shoot(self):
        if not self.shot:
            # prevents multiple shots
            self.speed = BALL_SPEED
            # sets initial upward velocity
            self.shot = True
            # marks ball as shot

    def reset(self):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        # returns ball to starting position
        self.speed = 0
        # resets vertical speed
        self.horizontal_speed = 0
        # resets horizontal speed
        self.shot = False
        # allows ball to be shot again

    def bounce_off_goalie(self, goalie):
        if self.rect.centerx < goalie.rect.centerx:
            # checks which side of goalie was hit
            self.horizontal_speed = -self.bounce_speed
            # bounces left if hit on left
        else:
            self.horizontal_speed = self.bounce_speed
            # bounces right if hit on right
        
        self.speed = abs(self.speed) * 0.7
        # reduces vertical speed after bounce
        # maintains upward movement
        self.shot = True
        # keeps ball in motion
class Goalie(pygame.sprite.Sprite):
    # inherits from pygame's Sprite class
    # handles goalie movement and positioning
    
    def __init__(self):
        super().__init__()
        # initializes parent Sprite class
        
        try:
            original_image = pygame.image.load("assets/goalie.png").convert_alpha()
            # attempts to load goalie sprite image
            # convert_alpha() for transparency handling
            
            self.image = pygame.transform.scale(original_image, (60, 60))
            # scales image to 60x60 pixels
            # maintains consistent goalie size
        except:
            self.image = pygame.Surface((60, 60))
            # creates fallback surface if image fails
            self.image.fill((255, 165, 0))
            # fills with orange color as fallback
        
        self.rect = self.image.get_rect(midtop=(SCREEN_WIDTH // 2, GOAL_Y))
        # creates rectangle for collision detection
        # positions goalie at top center of goal
        
        self.speed = GOALIE_SPEED
        # sets movement speed from settings
        self.direction = 1
        # 1 for right movement, -1 for left

    def update(self):
        self.rect.x += self.speed * self.direction
        # moves goalie horizontally
        # speed * direction determines movement direction
        
        goal_left = (SCREEN_WIDTH - GOAL_WIDTH) // 2
        # calculates left boundary of goal
        goal_right = goal_left + GOAL_WIDTH - self.rect.width
        # calculates right boundary of goal
        
        if self.rect.left <= goal_left or self.rect.right >= (goal_left + GOAL_WIDTH):
            # checks if goalie hits goal boundaries
            self.direction *= -1
            # reverses direction at boundaries

    def reset_position(self):
        self.rect.midtop = (SCREEN_WIDTH // 2, GOAL_Y)
        # resets goalie to center position
        # used when restarting game

def draw_field(screen):
    # handles drawing of soccer field elements
    
    screen.fill(GREEN)
    # fills background with green color
    # represents grass field

    goal_rect = pygame.Rect(
        (SCREEN_WIDTH - GOAL_WIDTH) // 2,
        GOAL_Y,
        GOAL_WIDTH,
        GOAL_HEIGHT
    )
    # creates rectangle for goal area
    # centers goal horizontally
    
    pygame.draw.rect(screen, WHITE, goal_rect, 5)
    # draws goal outline in white
    # thickness of 5 pixels

    penalty_box_width = GOAL_WIDTH * 1.5
    # wider than goal for visual effect
    penalty_box_height = GOAL_HEIGHT * 2
    # taller than goal for visual effect
    
    penalty_box_rect = pygame.Rect(
        (SCREEN_WIDTH - penalty_box_width) // 2,
        GOAL_Y,
        penalty_box_width,
        penalty_box_height
    )
    # creates rectangle for penalty box
    # centers relative to goal
    
    pygame.draw.rect(screen, WHITE, penalty_box_rect, 3)
    # draws penalty box outline
    # thinner than goal lines

    pygame.draw.line(screen, WHITE, (0, SCREEN_HEIGHT // 2), 
                    (SCREEN_WIDTH, SCREEN_HEIGHT // 2), 3)
    # draws horizontal midfield line
    # adds realism to field appearance