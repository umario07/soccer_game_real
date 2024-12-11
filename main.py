# Import necessary libraries for the game
# 'pygame' manages graphics and input for the game
# 'sys' handles system operations
import pygame
import sys
from settings import *  # Import settings (screen size, colors, speeds)
from sprites import *  # Import Ball and Goalie classes

# Main Game class
# Handles screen setup, scoring, and game logic
class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Create game screen
        # Dimensions defined in settings.py
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Set window title
        pygame.display.set_caption("Soccer Penalty Shootout")
        
        # Create clock to manage frame rate
        self.clock = pygame.time.Clock()
        
        # Setup font for score and messages
        # Uses default font, size from settings
        self.font = pygame.font.Font(None, FONT_SIZE)
        
        # Initialize score and shot tracking
        self.score = 0  # Start with 0 goals
        self.shots_taken = 0  # Start with 0 shots
        self.max_shots = 5  # Limit to 5 shots per game
        
        # Initialize game objects
        self.setup_sprites()

    def setup_sprites(self):
        # Group for all game sprites
        self.all_sprites = pygame.sprite.Group()
        
        # Create Ball object
        self.ball = Ball()
        
        # Create Goalie object
        self.goalie = Goalie()
        
        # Add Ball and Goalie to sprite group
        self.all_sprites.add(self.ball, self.goalie)

    def check_goal(self):
        # Only check if the ball has been kicked
        if not self.ball.shot:
            return
        
        # Define goal area rectangle
        goal_rect = pygame.Rect(
            (SCREEN_WIDTH - GOAL_WIDTH) // 2,  # Center horizontally
            GOAL_Y,  # Top edge defined in settings
            GOAL_WIDTH,  # Width defined in settings
            GOAL_HEIGHT  # Height defined in settings
        )
        
        # Check if ball is near goal
        if self.ball.rect.centery <= GOAL_Y + GOAL_HEIGHT:
            # Check collision with goalie
            if pygame.sprite.collide_rect(self.ball, self.goalie):
                print("Saved!")  # Ball blocked
                self.ball.reset()  # Reset ball position
            # Check if ball entered goal
            elif goal_rect.colliderect(self.ball.rect):
                self.score += 1  # Increment score
                print("You scored!")  # Display goal message
                self.ball.reset()  # Reset ball position

    def draw_text(self):
        # Render score display
        score_text = self.font.render(f"Score: {self.score}/{self.max_shots}", True, BLACK)
        # Display score in top-left corner
        self.screen.blit(score_text, (10, 10))
        
        # Show "Game Over" if all shots taken
        if self.shots_taken >= self.max_shots:
            game_over_text = self.font.render("Game Over!", True, BLACK)
            # Center "Game Over" text on screen
            self.screen.blit(game_over_text, 
                             (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                              SCREEN_HEIGHT // 2))
            
            # Show restart instructions
            restart_text = self.font.render("Press R to restart", True, BLACK)
            self.screen.blit(restart_text, 
                             (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                              SCREEN_HEIGHT // 2 + 50))

    def reset_game(self):
        # Reset score and shot counters
        self.score = 0
        self.shots_taken = 0
        
        # Reset ball and goalie positions
        self.ball.reset()
        self.goalie.reset_position()

    def run(self):
        # Main game loop
        running = True
        while running:
            # Handle events (e.g., key presses, quit)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Window close event
                    return
                if event.type == pygame.KEYDOWN:  # Key press event
                    # Shoot ball on SPACE press (if shots available)
                    if event.key == pygame.K_SPACE and self.shots_taken < self.max_shots:
                        if not self.ball.shot:
                            self.ball.shoot()  # Shoot ball
                            self.shots_taken += 1  # Increment shots counter
                    # Restart game on R press (if game over)
                    elif event.key == pygame.K_r and self.shots_taken >= self.max_shots:
                        self.reset_game()

            # Update game objects
            self.all_sprites.update()
            self.check_goal()  # Check if goal was scored or blocked
            
            # Draw game elements
            draw_field(self.screen)  # Draw field background
            self.all_sprites.draw(self.screen)  # Draw Ball and Goalie
            self.draw_text()  # Display score and messages
            
            # Update display
            pygame.display.flip()
            # Limit frame rate
            self.clock.tick(FPS)

# Run game if file is executed directly
if __name__ == "__main__":
    game = Game()  # Create Game object
    game.run()  # Start game loop
    pygame.quit()  # Quit pygame when finished
