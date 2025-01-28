import pygame  # Importing the pygame library

pygame.init()  # Initializing pygame

# Setting up window dimensions
w_width = 500  # Width of the game window
w_height = 500  # Height of the game window

# Creating the game window
screen = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Projectiles & Character Animation")  # Window title

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

# Defining the `Player` class to represent the character
class Player():
    def __init__(self, x, y, width, height):
        # Initializing attributes for the player character
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5  # Movement speed
        self.is_jump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True  # Indicates if the character is standing still

    def draw(self, screen):
        # Reset animation frame if it exceeds 27 (to loop animations)
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        # Display appropriate character sprite
        if not self.standing:
            if self.left:
                screen.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            # Display idle (standing) animation based on last movement
            if self.right:
                screen.blit(walkRight[0], (self.x, self.y))
            else:
                screen.blit(walkLeft[0], (self.x, self.y))


# Defining the `Projectile` class to represent bullets
class Projectile():
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction  # 1 for right, -1 for left
        self.vel = 8 * direction  # Projectile speed (adjusted by direction)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


# Function to update the game display
def DrawInGameLoop():
    screen.blit(bg_img, (0, 0))  # Draw the background image
    clock.tick(25)  # Set the frame rate to 25 frames per second
    soldier.draw(screen)  # Draw the soldier (character)
    for bullet in bullets:
        bullet.draw(screen)  # Draw projectiles
    pygame.display.flip()  # Update the display


# Creating an instance of the `Player` class
soldier = Player(50, 435, 64, 64)

# List to store all projectiles (bullets)
bullets = []

# Variable to control shooting cooldown
shoot = 0

# Game loop
done = True
while done:
    for event in pygame.event.get():  # Handling events
        if event.type == pygame.QUIT:  # If the close button is clicked
            done = False  # Exit the game loop

    # Shooting cooldown logic
    if shoot > 0:
        shoot += 1
    if shoot > 3:  # Cooldown period (3 frames)
        shoot = 0

    # Updating projectile positions
    for bullet in bullets:
        if 0 < bullet.x < w_width:  # Keep projectiles within screen bounds
            bullet.x += bullet.vel
        else:
            bullets.remove(bullet)  # Remove bullets that go off-screen

    # Handling player movement and actions
    keys = pygame.key.get_pressed()

    # Shooting bullets
    if keys[pygame.K_SPACE] and shoot == 0:
        direction = 1 if soldier.right else -1  # Bullet moves in player's direction
        if len(bullets) < 5:  # Limit the number of bullets
            bullets.append(Projectile(soldier.x + soldier.width // 2, 
                                      soldier.y + soldier.height // 2, 
                                      6, "black", direction))
        shoot = 1  # Start cooldown

    # Moving left
    if keys[pygame.K_LEFT] and soldier.x > 0:
        soldier.x -= soldier.vel
        soldier.left = True
        soldier.right = False
        soldier.standing = False

    # Moving right
    elif keys[pygame.K_RIGHT] and soldier.x < w_width - soldier.width:
        soldier.x += soldier.vel
        soldier.right = True
        soldier.left = False
        soldier.standing = False

    else:
        soldier.standing = True  # Character is standing still
        soldier.walkCount = 0  # Reset walk animation

    # Handling jumping
    if not soldier.is_jump:
        if keys[pygame.K_UP]:
            soldier.is_jump = True
            soldier.right = False
            soldier.left = False
    else:
        if soldier.jump_count >= -10:
            neg = 1 if soldier.jump_count >= 0 else -1  # Determine jump direction
            soldier.y -= (soldier.jump_count ** 2) * neg * 0.5
            soldier.jump_count -= 1
        else:
            soldier.jump_count = 10  # Reset jump count
            soldier.is_jump = False  # End jump

    DrawInGameLoop()  # Update the screen
