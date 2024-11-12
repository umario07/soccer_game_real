# main.py

# Importing the necessary libraries and modules
import pygame  
# The Pygame library allows us to create and display games
from settings import *  
# imports all the game settings like screen size and colors
from sprites import *  
# imports all the 

# Initialize Pygame to set up everything we need to run the game
pygame.init()

# Setting up the game screen (the window where the game will appear)
# We define the width and height from settings, and set a variable `screen` to manage it
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Naming the window to display "Single Player Soccer Game" at the top
pygame.display.set_caption("Single Player Soccer Game")

# Creating a group to store and manage all game sprites (game objects like the ball)
# Using this group allows us to easily update and draw all sprites in one step
all_sprites = pygame.sprite.Group()

# Creating an instance of the Ball class, which represents our soccer ball in the game
ball = Ball()
# Adding the ball to the `all_sprites` group so we can control it with other sprites (will add goalie and player)
all_sprites.add(ball)

# Creating an instance of the Goalie class, which represents the moving goalie
goalie = Goalie()  
# Adding the goalie to the `all_sprites` group
all_sprites.add(goalie)

# Starting the main game loop so that everything on the screen continuously updates and responds to player input
running = True  
# keeps the loop going as long as it is true (it is)
while running:
    # Check for player input events, in this case we want to see when they press the space bar or close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            # If the player closes the game window then...
            pygame.quit() 
            # ...quit the game

        if event.type == pygame.KEYDOWN:  
        # If any key is pressed down
            if event.key == pygame.K_SPACE:  
            # Specifically checking if the "space" key is pressed
                ball.shoot()  
                # Calls the ball’s "shoot" method, making it move forward

    # Update the state of all sprites (this will call each sprite's update method)
    all_sprites.update()

    # Drawing everything on the screen
    draw_field(screen)  
    # Draw the field, goal, and lines on the screen (added goal in draw_field function)
    screen.fill(GREEN)  
    # Fill the screen with a green background color (to represent a soccer field)
    all_sprites.draw(screen)  
    # Draw all sprites on top of the background (right now it is just the ball and the goalie)
    pygame.display.flip()  
    # updates all the graphics, without it you can't see anything on the screen

    pygame.time.Clock().tick(60)
    # make it 60 fps
