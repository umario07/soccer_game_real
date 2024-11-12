#This file was created by: Umair Mughal 

import pygame
# import pygame library
from settings import * 
# import everything from the settings library 

# define the ball class
class Ball(pygame.sprite.Sprite):
    # now set up its appearance, position, and speed
    def __init__(self):
        # initialize ball object
        super().__init__()
        # keeps the initialization process consistent and lets the ball have the functions of the sprite
       
        # Create a pygame circle that represents the ball's visual area
        # The surface dimensions are twice the BALL_RADIUS in both width and height
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
        # pygame.SRCALPHA allows for transparency 
        # makes it so that anything behind the ball can still be shown 
        
        pygame.draw.circle(self.image, WHITE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        # draws a white circle using the ball radius as a dimension 
        
        # define the rectangle (rect) that represents the ball's position and dimensions
        # Set the initial center position for the ball on the screen (for this game it is horizontally centered)
        
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        # SCREEN_WIDTH // 2 centers the ball horizontally, 
        # SCREEN_HEIGHT - 100 places it near the bottom

        # Initialize the ball's vertical speed to 0 (so that it doesn't move when it spawns)
        self.speed = 0

    # Update the Ball's position on the screen based on its current speed
    def update(self):
        # Move the ball vertically by adding the current speed to the y-coordinate of its rectangle
        
        self.rect.y += self.speed
        # makes it move up negatively and down positively 

        # this portion is to check if the ball goes outside the display 
        # if the top of the ball is, then reset it to its starting position
        if self.rect.top < 0:
            # resets ball to starting position 
            self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
            # teleports the ball back to the starting point
            self.speed = 0
            # makes the speed 0 so that after it teleports back it is motionless

    # how to actually shoot the ball
    def shoot(self):
        # defining the shoot feature
        self.speed = BALL_SPEED
        # this allows us to put a speed on the ball so that it can move 

class Goalie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create an orange rectangle representing the goalie
        self.image = pygame.Surface((40, GOAL_HEIGHT))  
        self.image.fill((255, 165, 0))  # Fill with orange color
        
        # Position the goalie at the top of the screen, centered in the goal
        goal_x = (SCREEN_WIDTH - GOAL_WIDTH) // 2
        self.rect = self.image.get_rect(midtop=(SCREEN_WIDTH // 2, GOAL_Y))

        # Set the speed of the goalie
        self.speed = 3  # Adjust for smooth, consistent motion

    def update(self):
        # Move the goalie back and forth across the entire goal width
        self.rect.x += self.speed
        goal_left = (SCREEN_WIDTH - GOAL_WIDTH) // 2  # Left edge of the goal
        goal_right = goal_left + GOAL_WIDTH - self.rect.width  # Right edge of the goal

        # Reverse direction if the goalie hits the goal boundaries
        if self.rect.left <= goal_left or self.rect.right >= goal_right:
            self.speed = -self.speed


# Define the draw_field function to render the field, goal, and lines
def draw_field(screen):
    # Fill the screen with the field color (green background)
    screen.fill(GREEN)

    # Draw the center line in the middle of the field
    pygame.draw.line(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 5)

    # Draw the main goal box (top of the screen)
    goal_rect = pygame.Rect((SCREEN_WIDTH - GOAL_WIDTH) // 2, GOAL_Y, GOAL_WIDTH, GOAL_HEIGHT)
    pygame.draw.rect(screen, WHITE, goal_rect, 5)

    # Draw the penalty box around the goal
    penalty_box_rect = pygame.Rect((SCREEN_WIDTH - GOAL_WIDTH * 2) // 2, GOAL_Y, GOAL_WIDTH * 2, GOAL_HEIGHT * 3)
    pygame.draw.rect(screen, WHITE, penalty_box_rect, 3)
