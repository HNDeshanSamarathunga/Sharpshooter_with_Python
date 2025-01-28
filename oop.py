import pygame  # Importing the pygame library
pygame.init()  # Initializing pygame

# Setting up window dimensions
w_width = 500  # Width of the game window
w_height = 500  # Height of the game window

# Creating the game window
screen = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Moving and animating sprites")  # Setting the window title

# Setting up the clock for controlling the frame rate
clock = pygame.time.Clock()

# Loading the background image and scaling it to fit the screen dimensions
bg_img = pygame.image.load("assets/Img/bg_img.jpeg")
bg_img = pygame.transform.scale(bg_img, (w_width, w_height))

# Loading walking animation frames for the right direction
walkRight = [pygame.image.load(f'assets/Img/soldier/{i}.png') for i in range(1, 10)]

# Loading walking animation frames for the left direction
walkLeft = [pygame.image.load(f'assets/Img/soldier/L{i}.png') for i in range(1, 10)]

# Loading the standing image of the character
char = pygame.image.load('assets/Img/soldier/standing.png')

# Defining the `player` class to represent the character
class player():

    def __init__(self, x, y, width, height):
        # Initializing attributes for the player character
        self.x = x  # x-coordinate of the character
        self.y = y  # y-coordinate of the character
        self.width = width  # Width of the character
        self.height = height  # Height of the character
        self.vel = 5  # Movement speed
        self.is_jump = False  # Jump state (True if jumping, False otherwise)
        self.jump_count = 10  # Controls jump height and duration
        self.left = False  # Indicates if the character is moving left
        self.right = False  # Indicates if the character is moving right
        self.walkCount = 0  # Counter for walking animation frames

    def draw(self, screen):
        # Method to draw the character on the screen
        if self.walkCount + 1 >= 27:  # Reset animation frame if it exceeds 27
            self.walkCount = 0

        if self.left:  # If the character is moving left
            # Display the current frame of the left walking animation
            screen.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1

        elif self.right:  # If the character is moving right
            # Display the current frame of the right walking animation
            screen.blit(walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        
        else:  # If the character is stationary
            # Display the standing image
            screen.blit(char, (self.x, self.y))

# Function to update the game display
def DrawInGameloop():
    screen.blit(bg_img, (0, 0))  # Draw the background image
    clock.tick(25)  # Set the frame rate to 25 frames per second
    soldier.draw(screen)  # Draw the soldier (character) on the screen
    pygame.display.flip()  # Update the display

# Creating an instance of the `player` class
soldier = player(50, 435, 64, 64)

# Game loop
done = True
while done:
    for event in pygame.event.get():  # Handling events
        if event.type == pygame.QUIT:  # If the close button is clicked
            done = False  # Exit the game loop

    keys = pygame.key.get_pressed()  # Get the state of all keys

    # Movement to the left
    if keys[pygame.K_LEFT] and soldier.x > 0:  # Check if left arrow is pressed and within bounds
        soldier.x -= soldier.vel  # Move left
        soldier.left = True  # Set left movement flag
        soldier.right = False  # Reset right movement flag

    # Movement to the right
    elif keys[pygame.K_RIGHT] and soldier.x < w_width - soldier.width:  # Check if right arrow is pressed and within bounds
        soldier.x += soldier.vel  # Move right
        soldier.right = True  # Set right movement flag
        soldier.left = False  # Reset left movement flag

    else:  # If no horizontal movement
        soldier.left = False  # Reset left movement flag
        soldier.right = False  # Reset right movement flag
        soldier.walkCount = 0  # Reset walk animation frame counter

    # Handling jumping
    if not soldier.is_jump:  # If not already jumping
        if keys[pygame.K_SPACE]:  # Check if spacebar is pressed
            soldier.is_jump = True  # Set jump flag
            soldier.right = False  # Reset right movement flag
            soldier.left = False  # Reset left movement flag

    else:  # If already jumping
        if soldier.jump_count >= -10:  # If jump height is not yet complete
            neg = 1  # Direction multiplier for upward movement
            if soldier.jump_count < 0:  # If descending
                neg = -1  # Reverse direction multiplier
            soldier.y -= (soldier.jump_count ** 2) * neg * 0.5  # Adjust y-coordinate
            soldier.jump_count -= 1  # Decrease jump counter
        else:  # If jump is complete
            soldier.jump_count = 10  # Reset jump counter
            soldier.is_jump = False  # Reset jump flag

    DrawInGameloop()  # Update the screen
