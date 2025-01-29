import pygame  # Importing the pygame library
pygame.init()  # Initializing pygame

# Window dimensions
w_width = 500  # Width of the game window
w_height = 500  # Height of the game window

# Create the game window
screen = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Adding enemies")  # Set the window title

# Set up the clock for controlling the frame rate
clock = pygame.time.Clock()

# Load and scale the background image
bg_img = pygame.image.load("assets/Img/bg_img.jpeg")
bg_img = pygame.transform.scale(bg_img, (w_width, w_height))

# Load walking animations for the player and the enemy
walkRight = [pygame.image.load(f'assets/Img/soldier/{i}.png') for i in range(1, 10)]
walkLeft = [pygame.image.load(f'assets/Img/soldier/L{i}.png') for i in range(1, 10)]
char = pygame.image.load('assets/Img/soldier/standing.png')
moveLeft = [pygame.image.load(f'assets/Img/enemy/L{i}.png') for i in range(1, 10)]
moveRight = [pygame.image.load(f'assets/Img/enemy/R{i}.png') for i in range(1, 10)]

# Define the player class
class player():
    def __init__(self, x, y, width, height):
        # Initialize player attributes
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5  # Movement speed
        self.is_jump = False  # Flag to indicate if the player is jumping
        self.jump_count = 10  # Jump height control
        self.left = False  # Moving left flag
        self.right = False  # Moving right flag
        self.walkCount = 0  # Animation frame counter
        self.standing = True  # Flag to indicate if the player is standing

    def draw(self, screen):
        # Animate walking
        if self.walkCount + 1 >= 27:  # Reset animation after all frames
            self.walkCount = 0

        if not self.standing:  # If the player is moving
            if self.left:
                screen.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:  # If the player is standing still
            if self.right:
                screen.blit(walkRight[0], (self.x, self.y))
            else:
                screen.blit(walkLeft[0], (self.x, self.y))

# Define the projectile class
class projectile():
    def __init__(self, x, y, radius, color, direction):
        # Initialize projectile attributes
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction  # Direction: 1 (right), -1 (left)
        self.vel = 8 * direction  # Speed of the projectile

    def draw(self, screen):
        # Draw the projectile as a circle
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# Define the enemy class
class enemy():
    def __init__(self, x, y, width, height, end):
        # Initialize enemy attributes
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.walkCount = 0  # Animation frame counter
        self.vel = 3  # Movement speed
        self.path = [x, end]  # Range of movement (start and end positions)

    def draw(self, screen):
        # Update enemy position and draw it
        self.move()
        if self.walkCount + 1 >= 27:  # Reset animation after all frames
            self.walkCount = 0

        if self.vel > 0:  # Moving right
            screen.blit(moveRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:  # Moving left
            screen.blit(moveLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1

    def move(self):
        # Control enemy movement within the path range
        if self.vel > 0:  # Moving right
            if self.x < self.path[1] - self.width + 20:
                self.x += self.vel
            else:  # Reverse direction at the end of the path
                self.vel = -self.vel
                self.walkCount = 0
        else:  # Moving left
            if self.x > self.path[0] - 20:
                self.x += self.vel
            else:  # Reverse direction at the start of the path
                self.vel = -self.vel
                self.walkCount = 0

# Function to draw all elements in the game loop
def DrawInGameloop():
    screen.blit(bg_img, (0, 0))  # Draw the background
    clock.tick(25)  # Set frame rate
    soldier.draw(screen)  # Draw the player
    enemy.draw(screen)  # Draw the enemy
    for bullet in bullets:  # Draw each bullet
        bullet.draw(screen)
    pygame.display.flip()  # Update the display

# Initialize the player and enemy objects
soldier = player(50, 435, 64, 64)
enemy = enemy(0, w_height - 64, 64, 64, w_width)
bullets = []  # List to store projectiles
shoot = 0  # Shooting cooldown

# Main game loop
done = True
while done:
    for event in pygame.event.get():  # Event handling
        if event.type == pygame.QUIT:  # Quit the game if close button is clicked
            done = False

    # Shooting cooldown logic
    if shoot > 0:
        shoot += 1
    if shoot > 3:
        shoot = 0

    # Update projectile positions or remove them if out of bounds
    for bullet in bullets:
        if 0 < bullet.x < 500:  # If the bullet is within the screen bounds
            bullet.x += bullet.vel
        else:  # Remove the bullet if it moves out of bounds
            bullets.pop(bullets.index(bullet))

    # Handle player controls
    keys = pygame.key.get_pressed()

    # Shooting bullets
    if keys[pygame.K_SPACE] and shoot == 0:  # Spacebar to shoot
        direction = 1 if soldier.right else -1  # Set bullet direction
        if len(bullets) < 5:  # Limit the number of bullets
            bullets.append(projectile((soldier.x + soldier.width // 2), (soldier.y + soldier.height // 2), 6, "black", direction))
        shoot = 1  # Start cooldown

    # Moving left
    if keys[pygame.K_LEFT] and soldier.x > 0:  # If within bounds
        soldier.x -= soldier.vel
        soldier.left = True
        soldier.right = False
        soldier.standing = False

    # Moving right
    elif keys[pygame.K_RIGHT] and soldier.x < w_width - soldier.width:  # If within bounds
        soldier.x += soldier.vel
        soldier.right = True
        soldier.left = False
        soldier.standing = False

    else:  # If no movement keys are pressed
        soldier.standing = True
        soldier.walkCount = 0

    # Jumping
    if not soldier.is_jump:  # If the player is not already jumping
        if keys[pygame.K_UP]:  # Start jump
            soldier.is_jump = True
            soldier.right = False
            soldier.left = False
    else:
        if soldier.jump_count >= -10:  # Jump motion
            neg = 1 if soldier.jump_count > 0 else -1  # Determine direction (up or down)
            soldier.y -= (soldier.jump_count ** 2) * neg * 0.5  # Update y-coordinate
            soldier.jump_count -= 1  # Reduce jump count
        else:  # Reset jump
            soldier.jump_count = 10
            soldier.is_jump = False

    DrawInGameloop()  # Redraw all elements on the screen
