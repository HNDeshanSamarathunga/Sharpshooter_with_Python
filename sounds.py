import pygame  # Importing the pygame library
pygame.init()  # Initializing pygame

# Setting up the window dimensions
w_width = 500
w_height = 500

# Create the game window
screen = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Adding Sounds")  # Set the title of the window

# Clock for controlling frame rate
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

# Setting up the font for displaying score
font = pygame.font.SysFont("helvetica", 30, 1, 1)
score = 0  # Initial score

# Loading and setting up sounds
bulletsound = pygame.mixer.Sound("assets/sounds/Bulletsound.mp3")  # Sound for shooting bullets
hitsound = pygame.mixer.Sound("assets/sounds/Hit.mp3")  # Sound for when an enemy is hit
music = pygame.mixer.music.load("assets/sounds/music.mp3")  # Background music
pygame.mixer.music.play(-1)  # Play background music on a loop
pygame.mixer.music.set_volume(0.6)  # Set volume for background music

# Define the `player` class
class player():
    def __init__(self, x, y, width, height):
        # Initialize player attributes
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5  # Movement speed
        self.is_jump = False  # Jump state
        self.jump_count = 10  # Jump height control
        self.left = False  # Moving left flag
        self.right = False  # Moving right flag
        self.walkCount = 0  # Animation frame counter
        self.standing = True  # Standing state
        self.hitbox = (self.x, self.y, self.width, self.height)  # Player hitbox
        self.hit = pygame.Rect(self.hitbox)  # Pygame rectangle for collision detection

    def draw(self, screen):
        # Draw the player with animations
        if self.walkCount + 1 >= 27:
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

        # Update hitbox
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.hit = pygame.Rect(self.hitbox)

    def touch(self):
        # Reset player position on touch
        self.x = 0
        self.y = w_height - self.height

# Define the `projectile` class
class projectile():
    def __init__(self, x, y, radius, color, direction):
        # Initialize projectile attributes
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.vel = 8 * direction  # Projectile speed

    def draw(self, screen):
        # Draw the projectile as a circle
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# Define the `enemy` class
class enemy():
    def __init__(self, x, y, width, height, end):
        # Initialize enemy attributes
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.walkCount = 0  # Animation frame counter
        self.vel = 3  # Movement speed
        self.path = [x, end]  # Enemy's movement range
        self.hitbox = (self.x + 20, self.y, self.width - 40, self.height - 4)
        self.hit = pygame.Rect(self.hitbox)  # Pygame rectangle for collision detection
        self.health = 9  # Health of the enemy
        self.visible = True  # Visibility flag

    def draw(self, screen):
        # Draw the enemy with animations and health bar
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 27:
                self.walkCount = 0

            if self.vel > 0:  # Moving right
                screen.blit(moveRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:  # Moving left
                screen.blit(moveLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            # Update hitbox and draw health bar
            self.hitbox = (self.x + 20, self.y, self.width - 40, self.height - 4)
            self.hit = pygame.Rect(self.hitbox)
            pygame.draw.rect(screen, "grey", (self.hitbox[0], self.hitbox[1] + 3, 50, 10))  # Background of health bar
            pygame.draw.rect(screen, "green", (self.hitbox[0], self.hitbox[1] + 3, 50 - (5.5 * (9 - self.health)), 10))  # Green health bar

    def move(self):
        # Move the enemy back and forth within the path
        if self.vel > 0:  # Moving right
            if self.x < self.path[1] - self.width + 20:
                self.x += self.vel
            else:  # Reverse direction at the path's end
                self.vel = -self.vel
                self.walkCount = 0
        else:  # Moving left
            if self.x > self.path[0] - 20:
                self.x += self.vel
            else:  # Reverse direction at the path's start
                self.vel = -self.vel
                self.walkCount = 0

    def touch(self):
        hitsound.play()  # Play hit sound when enemy is touched
        if self.health > 0:
            self.health -= 1  # Reduce health
        else:
            self.visible = False  # Hide enemy when health is depleted

# Function to draw all game elements
def DrawInGameloop():
    screen.blit(bg_img, (0, 0))  # Draw background
    clock.tick(25)  # Set frame rate
    soldier.draw(screen)  # Draw player
    text = font.render("Score : " + str(score), 1, "red")  # Render score
    screen.blit(text, (0, 10))  # Display score
    enemy.draw(screen)  # Draw enemy
    for bullet in bullets:  # Draw projectiles
        bullet.draw(screen)
    pygame.display.flip()  # Update display

# Initialize game objects
soldier = player(210, 435, 64, 64)
enemy = enemy(0, w_height - 64, 64, 64, w_width)
bullets = []  # List to store bullets
shoot = 0  # Shooting cooldown

# Main game loop
done = True
while done:
    for event in pygame.event.get():  # Handle events
        if event.type == pygame.QUIT:  # Quit game
            done = False

    # Collision detection between player and enemy
    if enemy.visible and soldier.hit.colliderect(enemy.hit):
        enemy.vel = -enemy.vel  # Reverse enemy direction
        soldier.touch()  # Reset player position

    # Shooting cooldown logic
    if shoot > 0:
        shoot += 1
    if shoot > 3:
        shoot = 0

    # Handle bullet collisions and movement
    for bullet in bullets:
        if enemy.visible and bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > enemy.hitbox[1]:
            if bullet.x + bullet.radius > enemy.hitbox[0] and bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]:
                bullets.pop(bullets.index(bullet))  # Remove bullet on hit
                score += 1  # Increment score
                enemy.touch()  # Reduce enemy health

        if 0 < bullet.x < 500:  # Move bullet within bounds
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))  # Remove bullet if out of bounds

    # Handle player input
    keys = pygame.key.get_pressed()

    # Shooting bullets
    if keys[pygame.K_SPACE] and shoot == 0:
        bulletsound.play()  # Play bullet sound
        direction = 1 if soldier.right else -1  # Determine bullet direction
        if len(bullets) < 5:  # Limit number of bullets
            bullets.append(projectile((soldier.x + soldier.width // 2), (soldier.y + soldier.height // 2), 6, "black", direction))
        shoot = 1

    # Player movement controls
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
    else:  # Player is standing still
        soldier.standing = True
        soldier.walkCount = 0

    # Jumping logic
    if not soldier.is_jump:
        if keys[pygame.K_UP]:  # Start jump
            soldier.is_jump = True
            soldier.right = False
            soldier.left = False
    else:  # Handle jump motion
        if soldier.jump_count >= -10:
            neg = 1 if soldier.jump_count > 0 else -1
            soldier.y -= (soldier.jump_count ** 2) * neg * 0.5  # Update y-coordinate
            soldier.jump_count -= 1
        else:  # Reset jump
            soldier.jump_count = 10
            soldier.is_jump = False

    DrawInGameloop()  # Redraw the screen
