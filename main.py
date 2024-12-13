# Import necessary libraries for the game
import pygame
import sys

# Import settings from a separate file
# These include configurations like screen size, colors, and other constants
from settings import *

# Import custom sprite classes for the Ball and Goalie
from sprites import *

# Define the main Game class
# This class handles the screen setup, scoring, and overall game logic
class Game:
    def __init__(self):
        # Initialize pygame, which sets up the game engine
        pygame.init()
        
        # Create the game window with dimensions defined in the settings file
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Set the title of the game window to "Soccer Penalty Shootout"
        pygame.display.set_caption("Soccer Penalty Shootout")
        
        # Create a clock object to manage the frame rate of the game
        self.clock = pygame.time.Clock()
        
        # Set up a font object to display text such as scores and messages
        # The font is set to the default font with a size specified in the settings file
        self.font = pygame.font.Font(None, FONT_SIZE)
        
        # Initialize the score counter, which starts at 0
        self.score = 0
        
        # Initialize the shot counter, which starts at 0
        self.shots_taken = 0
        
        # Set the maximum number of shots allowed in the game to 5
        self.max_shots = 5
        
        # Call a method to initialize the game objects
        self.setup_sprites()

    def setup_sprites(self):
        # Create a group to hold all game sprites for easier updates and rendering
        self.all_sprites = pygame.sprite.Group()
        
        # Create an instance of the Ball class, which represents the soccer ball
        self.ball = Ball()
        
        # Create an instance of the Goalie class, which represents the goalie
        self.goalie = Goalie()
        
        # Add the Ball and Goalie objects to the sprite group for tracking and rendering
        self.all_sprites.add(self.ball, self.goalie)

    def check_goal(self):
        # Only check for goals or saves if the ball has been kicked
        if not self.ball.shot:
            return
        
        # Create a rectangular area to represent the goal
        goal_rect = pygame.Rect(
            (SCREEN_WIDTH - GOAL_WIDTH) // 2, GOAL_Y, GOAL_WIDTH, GOAL_HEIGHT)
        
        # Center the goal horizontally
        # Set the top edge of the goal based on a predefined constant
        # Set the width of the goal based on a predefined constant
        # Set the height of the goal based on a predefined constant

        # Check if the ball has reached the area near the goal
        if self.ball.rect.centery <= GOAL_Y + GOAL_HEIGHT:
            # Check if the ball collides with the goalie
            if pygame.sprite.collide_rect(self.ball, self.goalie):
                # Print a message indicating the ball was saved by the goalie
                print("Saved!")
                
                # Reset the ball to its original position and state
                self.ball.reset()
            # Check if the ball enters the goal area
            elif goal_rect.colliderect(self.ball.rect):
                # Increment the score by 1 for a successful goal
                self.score += 1
                
                # Print a message indicating a goal was scored
                print("You scored!")
                
                # Reset the ball to its original position and state
                self.ball.reset()

    def draw_text(self):
        # Render the score text to display the current score and shots taken
        score_text = self.font.render(f"Score: {self.score}/{self.max_shots}", True, BLACK)
        
        # Display the score text in the top-left corner of the screen
        self.screen.blit(score_text, (10, 10))
        
        # Check if the maximum number of shots has been taken
        if self.shots_taken >= self.max_shots:
            # Render a "Game Over" message when the game ends
            game_over_text = self.font.render("Game Over!", True, BLACK)
            
            # Center the "Game Over" message on the screen
            self.screen.blit(game_over_text, 
                             (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                              SCREEN_HEIGHT // 2))
            
            # Render instructions to restart the game
            restart_text = self.font.render("Press R to restart", True, BLACK)
            
            # Display the restart instructions below the "Game Over" message
            self.screen.blit(restart_text, 
                             (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                              SCREEN_HEIGHT // 2 + 50))

    def reset_game(self):
        # Reset the score counter to 0
        self.score = 0
        
        # Reset the shots taken counter to 0
        self.shots_taken = 0
        
        # Reset the ball's position and state
        self.ball.reset()
        
        # Reset the goalie's position to its default state
        self.goalie.reset_position()

    def run(self):
        # Start the main game loop, which will continue running until the game is exited
        running = True
        
        while running:
            # Process all events, such as key presses or quitting the game
            for event in pygame.event.get():
                # Check if the user has closed the game window
                if event.type == pygame.QUIT:
                    # Exit the game loop
                    return
                
                # Check if a key was pressed
                if event.type == pygame.KEYDOWN:
                    # Check if the SPACE key was pressed to shoot the ball
                    if event.key == pygame.K_SPACE and self.shots_taken < self.max_shots:
                        # Ensure the ball has not already been shot
                        if not self.ball.shot:
                            # Trigger the ball's shooting action
                            self.ball.shoot()
                            
                            # Increment the number of shots taken
                            self.shots_taken += 1
                    # Check if the R key was pressed to restart the game
                    elif event.key == pygame.K_r and self.shots_taken >= self.max_shots:
                        # Reset the game state to start a new game
                        self.reset_game()

            # Update the state of all game objects
            self.all_sprites.update()
            
            # Check if the ball has scored a goal or been saved by the goalie
            self.check_goal()
            
            # Draw the soccer field and all game elements on the screen
            draw_field(self.screen)
            
            # Draw the Ball and Goalie objects on the screen
            self.all_sprites.draw(self.screen)
            
            # Display the current score and messages on the screen
            self.draw_text()
            
            # Update the display to show the latest frame
            pygame.display.flip()
            
            # Limit the frame rate to the predefined frames per second (FPS) value
            self.clock.tick(FPS)

# Check if this file is being run directly (not imported)
if __name__ == "__main__":
    # Create an instance of the Game class
    game = Game()
    
    # Start the game loop
    game.run()
    
    # Quit pygame and clean up resources when the game ends
    pygame.quit()
