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
        if not self.ball.shot:
            return
        
        goal_rect = pygame.Rect(
            (SCREEN_WIDTH - GOAL_WIDTH) // 2, GOAL_Y, GOAL_WIDTH, GOAL_HEIGHT)

        if self.ball.rect.centery <= GOAL_Y + GOAL_HEIGHT:
            if pygame.sprite.collide_rect(self.ball, self.goalie):
                print("Saved!")
                # Add bounce effect when ball hits goalie
                self.ball.bounce_off_goalie(self.goalie)
            elif goal_rect.colliderect(self.ball.rect):
                self.score += 1
                print("You scored!")
                self.ball.reset()

    def draw_text(self):
        score_text = self.font.render(f"Score: {self.score}/{self.shots_taken}", True, BLACK)
        # creates score display showing current score out of shots taken
        self.screen.blit(score_text, (10, 10))
        # positions score in top-left
        
        if self.shots_taken >= self.max_shots and not self.ball.shot:
            # only show end game text after ball has completed its motion
            if self.score == self.max_shots:
                # perfect score condition
                win_text = self.font.render("You Win! Perfect Score!", True, BLACK)
                # creates win message
                self.screen.blit(win_text, 
                               (SCREEN_WIDTH // 2 - win_text.get_width() // 2, 
                                SCREEN_HEIGHT // 2))
                # centers win text
            else:
                # normal game over condition
                game_over_text = self.font.render("Game Over!", True, BLACK)
                # creates game over message
                self.screen.blit(game_over_text, 
                               (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                                SCREEN_HEIGHT // 2))
                # centers game over text
            
            restart_text = self.font.render("Press R to restart", True, BLACK)
            # creates restart instruction
            self.screen.blit(restart_text, 
                           (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                            SCREEN_HEIGHT // 2 + 50))
            # positions restart text below game over

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
    