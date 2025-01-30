import pygame
pygame.init()

# Setting up window dimensions
w_width = 500  # Width of the game window
w_height = 500  # Height of the game window

# Creating the game window
screen = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Displaying text")  # Setting the window title

# Setting up the clock for controlling the frame rate
clock = pygame.time.Clock()

# Loading and scaling the background image
bg_img = pygame.image.load("assets/Img/bg_img.jpeg")
bg_img = pygame.transform.scale(bg_img, (w_width, w_height))

# Loading animations for the player and enemy
walkRight = [pygame.image.load(f'assets/Img/soldier/{i}.png') for i in range(1, 10)]
walkLeft = [pygame.image.load(f'assets/Img/soldier/L{i}.png') for i in range(1, 10)]
char = pygame.image.load('assets/Img/soldier/standing.png')
moveLeft = [pygame.image.load(f'assets/Img/enemy/L{i}.png') for i in range(1, 10)]
moveRight = [pygame.image.load(f'assets/Img/enemy/R{i}.png') for i in range(1, 10)]

# Font setup for displaying the score
font = pygame.font.SysFont("helvetica", 30, 1, 1)
score = 0  # Variable to keep track of the score

# Class to define the player's behavior
class player():
    def __init__(self, x, y, width, height):
        # Initialize player attributes
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5  # Movement speed
        self.is_jump = False  # Flag for jumping state
        self.jump_count = 10  # Jump height control
        self.left = False  # Flag for moving left
        self.right = False  # Flag for moving right
        self.walkCount = 0  # Frame counter for walking animation
        self.standing = True  # Flag for standing state
        self.hitbox = (self.x, self.y, self.width, self.height)  # Hitbox for collisions
        self.hit = pygame.Rect(self.hitbox)

    def draw(self, screen):
        # Animate walking
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:  # If the player is moving
            if self.left:
                screen.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:  # If the player is standing
            if self.right:
                screen.blit(walkRight[0], (self.x, self.y))
            else:
                screen.blit(walkLeft[0], (self.x, self.y))

        # Update the hitbox
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.hit = pygame.Rect(self.hitbox)

# Class to define projectiles (e.g., bullets)
class projectile():
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction  # Direction (1 for right, -1 for left)
        self.vel = 8 * direction  # Projectile speed

    def draw(self, screen):
        # Draw the projectile as a circle
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# Class to define enemy behavior
class enemy():
    def __init__(self, x, y, width, height, end):
        # Initialize enemy attributes
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.walkCount = 0  # Animation frame counter
        self.vel = 3  # Movement speed
        self.path = [x, end]  # Movement range
        self.hitbox = (self.x + 20, self.y, self.width - 40, self.height - 4)  # Enemy hitbox
        self.hit = pygame.Rect(self.hitbox)

    def draw(self, screen):
        # Update enemy position and draw the animation
        self.move()
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if self.vel > 0:  # Moving right
            screen.blit(moveRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:  # Moving left
            screen.blit(moveLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1

        # Update the hitbox
        self.hitbox = (self.x + 20, self.y, self.width - 40, self.height - 4)
        self.hit = pygame.Rect(self.hitbox)

    def move(self):
        # Move the enemy within its path
        if self.vel > 0:  # Moving right
            if self.x < self.path[1] - self.width + 20:
                self.x += self.vel
            else:  # Change direction at the end of the path
                self.vel = -self.vel
                self.walkCount = 0
        else:  # Moving left
            if self.x > self.path[0] - 20:
                self.x += self.vel
            else:  # Change direction at the start of the path
                self.vel = -self.vel
                self.walkCount = 0

# Function to draw everything on the screen
def DrawInGameloop():
    screen.blit(bg_img, (0, 0))  # Draw the background
    clock.tick(25)  # Set frame rate
    soldier.draw(screen)  # Draw the player
    text = font.render("Score : " + str(score), 1, "red")  # Render the score text
    screen.blit(text, (0, 10))  # Display the score at the top-left corner
    enemy.draw(screen)  # Draw the enemy
    for bullet in bullets:  # Draw each bullet
        bullet.draw(screen)
    pygame.display.flip()  # Update the screen

# Initialize game objects
soldier = player(210, 435, 64, 64)
enemy = enemy(0, w_height - 64, 64, 64, w_width)
bullets = []  # List to store bullets
shoot = 0  # Shooting cooldown

# Main game loop
done = True
while done:
    for event in pygame.event.get():  # Handle events
        if event.type == pygame.QUIT:  # Quit the game if the close button is clicked
            done = False

    # Collision detection between player and enemy
    if soldier.hit.colliderect(enemy.hit):
        enemy.vel = -enemy.vel  # Reverse enemy direction on collision

    # Handle shooting cooldown
    if shoot > 0:
        shoot += 1
    if shoot > 3:
        shoot = 0

    # Check for bullet collisions with the enemy
    for bullet in bullets:
        if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > enemy.hitbox[1]:
            if bullet.x + bullet.radius > enemy.hitbox[0] and bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]:
                bullets.pop(bullets.index(bullet))  # Remove the bullet on collision
                score += 1  # Increment the score

        # Move bullets or remove them if out of bounds
        if 0 < bullet.x < 500:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    # Handle player input
    keys = pygame.key.get_pressed()

    # Shooting bullets
    if keys[pygame.K_SPACE] and shoot == 0:
        direction = 1 if soldier.right else -1
        if len(bullets) < 5:  # Limit the number of bullets
            bullets.append(projectile((soldier.x + soldier.width // 2), (soldier.y + soldier.height // 2), 6, "black", direction))
        shoot = 1

    # Movement controls
    if keys[pygame.K_LEFT] and soldier.x > 0:  # Move left
        soldier.x -= soldier.vel
        soldier.left = True
        soldier.right = False
        soldier.standing = False
    elif keys[pygame.K_RIGHT] and soldier.x < w_width - soldier.width:  # Move right
        soldier.x += soldier.vel
        soldier.right = True
        soldier.left = False
        soldier.standing = False
    else:
        soldier.standing = True
        soldier.walkCount = 0

    # Handle jumping
    if not soldier.is_jump:
        if keys[pygame.K_UP]:  # Start jump
            soldier.is_jump = True
            soldier.right = False
            soldier.left = False
    else:
        if soldier.jump_count >= -10:  # Jump motion
            neg = 1 if soldier.jump_count > 0 else -1
            soldier.y -= (soldier.jump_count ** 2) * neg * 0.5
            soldier.jump_count -= 1
        else:  # Reset jump
            soldier.jump_count = 10
            soldier.is_jump = False

    DrawInGameloop()  # Redraw everything
