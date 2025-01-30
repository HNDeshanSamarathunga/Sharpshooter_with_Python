import pygame
pygame.init()

# Window dimensions
w_width = 500
w_height = 500

# Create the display window
screen = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Collision detection")

# Set up the clock for controlling the frame rate
clock = pygame.time.Clock()

# Load the background image and scale it to the window dimensions
bg_img = pygame.image.load("assets/Img/bg_img.jpeg")
bg_img = pygame.transform.scale(bg_img, (w_width, w_height))

# Load sprite animations for the player and enemy
walkRight = [pygame.image.load(f'assets/Img/soldier/{i}.png') for i in range(1, 10)]
walkLeft = [pygame.image.load(f'assets/Img/soldier/L{i}.png') for i in range(1, 10)]
char = pygame.image.load('assets/Img/soldier/standing.png')
moveLeft = [pygame.image.load(f'assets/Img/enemy/L{i}.png') for i in range(1, 10)]
moveRight = [pygame.image.load(f'assets/Img/enemy/R{i}.png') for i in range(1, 10)]

# Player class to define player behavior
class player():

    def __init__(self, x, y, width, height):
        # Initialize player attributes
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.is_jump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.hit = pygame.Rect(self.hitbox)  # Define collision hitbox

    def draw(self, screen):
        # Animate player movement
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:  # If player is moving
            if self.left:
                screen.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:  # If player is standing still
            if self.right:
                screen.blit(walkRight[0], (self.x, self.y))
            else:
                screen.blit(walkLeft[0], (self.x, self.y))

        # Update hitbox for collision detection
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.hit = pygame.Rect(self.hitbox)

# Class for projectiles (e.g., bullets)
class projectile():
    def __init__(self, x, y, radius, color, direction):
        # Initialize projectile attributes
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.vel = 8 * direction  # Projectile speed depends on direction

    def draw(self, screen):
        # Draw the projectile as a circle
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# Enemy class to define enemy behavior
class enemy():

    def __init__(self, x, y, width, height, end):
        # Initialize enemy attributes
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.walkCount = 0
        self.vel = 3  # Speed of enemy movement
        self.path = [x, end]  # Movement range
        self.hitbox = (self.x + 20, self.y, self.width - 40, self.height - 4)
        self.hit = pygame.Rect(self.hitbox)  # Define collision hitbox

    def draw(self, screen):
        self.move()  # Move the enemy
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if self.vel > 0:  # Moving right
            screen.blit(moveRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:  # Moving left
            screen.blit(moveLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1

        # Update hitbox for collision detection
        self.hitbox = (self.x + 20, self.y, self.width - 40, self.height - 4)
        self.hit = pygame.Rect(self.hitbox)

    def move(self):
        # Move the enemy along its path
        if self.vel > 0:  # Moving right
            if self.x < self.path[1] - self.width + 20:
                self.x += self.vel
            else:  # Change direction at the path's end
                self.vel = self.vel * -1
                self.walkCount = 0
        else:  # Moving left
            if self.x > self.path[0] - 20:
                self.x += self.vel
            else:  # Change direction at the path's start
                self.vel = self.vel * -1
                self.walkCount = 0

# Function to update the game screen
def DrawInGameloop():
    screen.blit(bg_img, (0, 0))  # Draw background
    clock.tick(25)  # Set frame rate
    soldier.draw(screen)  # Draw the player
    enemy.draw(screen)  # Draw the enemy
    for bullet in bullets:  # Draw all projectiles
        bullet.draw(screen)
    pygame.display.flip()  # Update the display

# Initialize game objects
soldier = player(50, 435, 64, 64)
enemy = enemy(0, w_height - 64, 64, 64, w_width)
bullets = []  # List to store projectiles
shoot = 0  # Shooting cooldown

# Game loop
done = True
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit the game
            done = False

    # Collision detection between player and enemy
    if soldier.hit.colliderect(enemy.hit):
        enemy.vel = enemy.vel * -1  # Reverse enemy direction on collision

    # Shooting cooldown logic
    if shoot > 0:
        shoot += 1
    if shoot > 3:
        shoot = 0

    # Check collisions between bullets and enemy
    for bullet in bullets:
        if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > enemy.hitbox[1]:
            if bullet.x + bullet.radius > enemy.hitbox[0] and bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]:
                bullets.pop(bullets.index(bullet))  # Remove bullet on collision

        # Update bullet position or remove it if out of bounds
        if 0 < bullet.x < 500:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    # Player movement and actions
    keys = pygame.key.get_pressed()

    # Shooting projectiles
    if keys[pygame.K_SPACE] and shoot == 0:
        direction = 1 if soldier.right else -1
        if len(bullets) < 5:  # Limit number of bullets
            bullets.append(projectile((soldier.x + soldier.width // 2), (soldier.y + soldier.height // 2), 6, "black", direction))
        shoot = 1

    # Movement keys
    if keys[pygame.K_LEFT] and soldier.x > 0:
        soldier.x -= soldier.vel
        soldier.left = True
        soldier.right = False
        soldier.standing = False
    elif keys[pygame.K_RIGHT] and soldier.x < w_width - soldier.width:
        soldier.x += soldier.vel
        soldier.right = True
        soldier.left = False
        soldier.standing = False
    else:
        soldier.standing = True
        soldier.walkCount = 0

    # Jumping logic
    if not soldier.is_jump:
        if keys[pygame.K_UP]:
            soldier.is_jump = True
            soldier.right = False
            soldier.left = False
    else:
        if soldier.jump_count >= -10:
            neg = 1 if soldier.jump_count > 0 else -1
            soldier.y -= (soldier.jump_count ** 2) * neg * 0.5
            soldier.jump_count -= 1
        else:
            soldier.jump_count = 10
            soldier.is_jump = False

    DrawInGameloop()  # Update the screen
