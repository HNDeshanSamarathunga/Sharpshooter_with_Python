import pygame  

# Initialize Pygame
pygame.init()

# Window dimensions
w_width = 500  # Width of the game window
w_height = 500  # Height of the game window
screen = pygame.display.set_mode((w_width, w_height))  # Create a display window
screen.fill("white")  # Fill the screen with a white background
pygame.display.set_caption("Moving and Animating Sprites")  # Set the window title

# Creating object
x = 50  # Initial x-coordinate of the character
y = 435  # Initial y-coordinate of the character
width = 64  # Width of the character
height = 64  # Height of the character
vel = 5  # Movement speed of the character
clock = pygame.time.Clock()  # Clock to control frame rate

# Jump Variable
is_Jump = False  # Tracks if the character is currently jumping
jump_Count = 10  # Controls the jump height and animation

# Background image
bg_img = pygame.image.load("assets/Img/bg_img.jpeg")  # Load the background image
bg_img = pygame.transform.scale(bg_img, (w_width, w_height))  # Scale the background image to fit the window

# Character variables
left = False  # Tracks if the character is moving left
right = False  # Tracks if the character is moving right
walkCount = 0  # Tracks the current frame of the walking animation

# Load character animations
walkRight = [pygame.image.load(f'assets/Img/soldier/{i}.png') for i in range(1, 10)]  # Load frames for moving right
walkLeft = [pygame.image.load(f'assets/Img/soldier/L{i}.png') for i in range(1, 10)]  # Load frames for moving left
char = pygame.image.load('assets/Img/soldier/standing.png')  # Load the standing frame


def DrawInGameLoop():
    global walkCount  # Declare walkCount as global to modify it inside the function
    global x, y  # Declare x and y as global to update the character's position

    screen.blit(bg_img, (0, 0))  # Draw the background image on the screen

    # Control frame rate
    clock.tick(25)  # Limit the game to 25 frames per second

    if walkCount + 1 >= 9:  # Reset the walking animation frame count
        walkCount = 0

    # Draw the character based on the direction it is facing
    if left:
        screen.blit(walkLeft[walkCount], (x, y))  # Draw the current frame for moving left
        walkCount += 1  # Move to the next frame
    elif right:
        screen.blit(walkRight[walkCount], (x, y))  # Draw the current frame for moving right
        walkCount += 1  # Move to the next frame
    else:
        screen.blit(char, (x, y))  # Draw the standing frame if not moving

    pygame.display.flip()  # Update the display with the new drawings


# Main loop flag
done = True  # Flag to keep the game running
while done:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Check if the user closes the window
            done = False  # Exit the game loop

    # Handle key presses
    keys = pygame.key.get_pressed()  # Get the current state of all keys
    if keys[pygame.K_UP] and y > 0:  # Move up
        y -= vel
    if keys[pygame.K_DOWN] and y < w_height - height:  # Move down
        y += vel
    if keys[pygame.K_LEFT] and x > 0:  # Move left
        x -= vel
        left = True  # Set the left direction flag
        right = False  # Clear the right direction flag
    elif keys[pygame.K_RIGHT] and x < w_width - width:  # Move right
        x += vel
        right = True  # Set the right direction flag
        left = False  # Clear the left direction flag
    else:
        left = False  # Clear the left direction flag if no movement
        right = False  # Clear the right direction flag if no movement
        walkCount = 0  # Reset the walking animation frame count

    # Jump logic
    if not is_Jump:  # Check if the character is not already jumping
        if keys[pygame.K_SPACE]:  # Check if the spacebar is pressed
            is_Jump = True  # Start the jump
            right = False  # Clear movement flags during the jump
            left = False
    else:
        if jump_Count >= -10:  # Check if the jump is ongoing
            neg = 1
            if jump_Count < 0:  # Start falling when reaching the apex
                neg = -1
            y -= (jump_Count ** 2) * neg * 0.5  # Update the y-coordinate for the jump
            jump_Count -= 1  # Decrease the jump counter
        else:
            jump_Count = 10  # Reset the jump counter
            is_Jump = False  # End the jump

    DrawInGameLoop()  # Call the function to update the game screen
