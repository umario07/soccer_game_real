### sprites.py
import pygame
from settings import *

class Ball(pygame.sprite.Sprite):
    # Ball class represents the soccer ball sprite, handling shooting and reset actions.
    def __init__(self):
        super().__init__()
        # Create a circular ball with transparent background and set its initial position near the bottom of the screen.
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))

        # Set the initial speed of the ball to zero, and mark shot status as False.
        self.speed = 0
        self.shot = False

    def update(self):
        # Update the ball's position when it has been shot.
        if self.shot:
            self.rect.y += self.speed

            # If the ball moves off-screen or crosses the bottom, reset its position.
            if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
                self.reset()

    def shoot(self):
        # Initiates the ball's movement by setting speed if it hasn’t already been shot.
        if not self.shot:
            self.speed = BALL_SPEED
            self.shot = True

    def reset(self):
        # Resets the ball to the initial position and halts its movement.
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.speed = 0
        self.shot = False

class Goalie(pygame.sprite.Sprite):
    # Goalie class manages the goalie sprite and its automatic back-and-forth movement.
    def __init__(self):
        super().__init__()
        # Create a rectangular goalie sprite with orange color to distinguish from the field.
        self.image = pygame.Surface((40, 60))
        self.image.fill((255, 165, 0))  # Orange color

        # Position goalie at the center top of the goal area with a designated speed and direction.
        self.rect = self.image.get_rect(midtop=(SCREEN_WIDTH // 2, GOAL_Y))
        self.speed = GOALIE_SPEED  # Use configurable constant for speed
        self.direction = 1

    def update(self):
        # Move the goalie horizontally within the goal area, reversing direction at each boundary.
        self.rect.x += self.speed * self.direction
        goal_left = (SCREEN_WIDTH - GOAL_WIDTH) // 2
        goal_right = goal_left + GOAL_WIDTH - self.rect.width

        # Reverse direction if the goalie reaches the left or right boundary of the goal area.
        if self.rect.left <= goal_left or self.rect.right >= goal_right:
            self.direction *= -1

    def reset_position(self):
        # Optional: Reset goalie position to center (if needed for extended functionality).
        self.rect.midtop = (SCREEN_WIDTH // 2, GOAL_Y)

# Function to render the game field
# Changes made to enhance the visibility and realism of the field lines and penalty box.
def draw_field(screen):
    # Set the background to a green color representing the field.
    screen.fill(GREEN)

    # Draw the goal as a white rectangle centered at the top of the field.
    goal_rect = pygame.Rect(
        (SCREEN_WIDTH - GOAL_WIDTH) // 2,
        GOAL_Y,
        GOAL_WIDTH,
        GOAL_HEIGHT
    )
    pygame.draw.rect(screen, WHITE, goal_rect, 5)

    # Draw the penalty box surrounding the goal, extending it outward for better gameplay visibility.
    penalty_box_width = GOAL_WIDTH * 1.5
    penalty_box_height = GOAL_HEIGHT * 2
    penalty_box_rect = pygame.Rect(
        (SCREEN_WIDTH - penalty_box_width) // 2,
        GOAL_Y,
        penalty_box_width,
        penalty_box_height
    )
    pygame.draw.rect(screen, WHITE, penalty_box_rect, 3)

    # Draw the center line for a realistic soccer field effect.
    pygame.draw.line(screen, WHITE, (0, SCREEN_HEIGHT // 2), (SCREEN_WIDTH, SCREEN_HEIGHT // 2), 3)
