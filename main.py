# main.py
import pygame
import sys
from settings import *
from sprites import *

# Game class handles all game functions, from initializing pygame, 
# creating sprites, managing score and shots, to updating and drawing elements on the screen.
class Game:
    def __init__(self):
        # Initialize pygame, screen dimensions, and game display settings.
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Soccer Penalty Shootout")
        
        # Set up a clock for controlling the frame rate.
        self.clock = pygame.time.Clock()
        
        # Define the game font and size for displaying text like score and game-over messages.
        self.font = pygame.font.Font(None, FONT_SIZE)
        
        # Initialize score and tracking shots taken by the player.
        self.score = 0
        self.shots_taken = 0
        self.max_shots = 5  # Limit on maximum shots allowed in the game.
        
        # Setup all sprite objects (like ball and goalie) used in the game.
        self.setup_sprites()

    def setup_sprites(self):
        # Initialize a group to hold all game sprites and create instances of the Ball and Goalie classes.
        self.all_sprites = pygame.sprite.Group()
        
        # Initialize the ball and goalie and add them to the all_sprites group.
        self.ball = Ball()
        self.goalie = Goalie()
        self.all_sprites.add(self.ball, self.goalie)

    def check_goal(self):
        # Method to check whether the ball successfully enters the goal after being shot.
        if not self.ball.shot:
            return  # Only check for a goal if the ball has been shot.
        
        # Define the rectangular area of the goal as a target for the ball.
        goal_rect = pygame.Rect(
            (SCREEN_WIDTH - GOAL_WIDTH) // 2,
            GOAL_Y,
            GOAL_WIDTH,
            GOAL_HEIGHT
        )
        
        # If the ball crosses the goal line within goal bounds, check for a goal or goalie block.
        if self.ball.rect.centery <= GOAL_Y + GOAL_HEIGHT:
            # Check if the goalie blocks the ball; reset ball position if blocked.
            if pygame.sprite.collide_rect(self.ball, self.goalie):
                self.ball.reset()
            # If the ball enters the goal area, increase score and reset ball.
            elif goal_rect.colliderect(self.ball.rect):
                self.score += 1
                self.ball.reset()
            
    def draw_text(self):
        # Method for rendering text onto the screen, including score and game-over message.
        
        # Display the current score and shots taken on the screen's top left corner.
        score_text = self.font.render(f"Score: {self.score}/{self.shots_taken}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        # If player has reached max shots, display the game-over and restart instructions.
        if self.shots_taken >= self.max_shots:
            game_over_text = self.font.render("Game Over!", True, BLACK)
            self.screen.blit(game_over_text, 
                           (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 
                            SCREEN_HEIGHT//2))
            
            restart_text = self.font.render("Press R to restart", True, BLACK)
            self.screen.blit(restart_text, 
                           (SCREEN_WIDTH//2 - restart_text.get_width()//2, 
                            SCREEN_HEIGHT//2 + 50))

    def reset_game(self):
        # Reset game variables when player chooses to restart after reaching max shots.
        self.score = 0
        self.shots_taken = 0
        self.ball.reset()

    def run(self):
        # Main game loop that manages events, updates, and rendering until the game is quit.
        running = True
        while running:
            # Event handling loop to capture player input like quitting or shooting the ball.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    # Space bar shoots the ball if shots are available.
                    if event.key == pygame.K_SPACE and self.shots_taken < self.max_shots:
                        if not self.ball.shot:
                            self.ball.shoot()
                            self.shots_taken += 1
                    # R key resets the game after max shots have been reached.
                    elif event.key == pygame.K_r and self.shots_taken >= self.max_shots:
                        self.reset_game()

            # Update the position and state of all sprites.
            self.all_sprites.update()
            self.check_goal()  # Check if a shot has resulted in a goal.
            
            # Draw the game field, sprites, and display text for score and messages.
            draw_field(self.screen)
            self.all_sprites.draw(self.screen)
            self.draw_text()
            
            # Refresh the display to show the latest frame, with the clock controlling FPS.
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    # Run the game if the script is executed directly.
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
