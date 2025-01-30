import pygame  # Import pygame library
pygame.init()  # Initialize pygame

# Setting up the game window
w_width = 500  # Width of the window
w_height = 500  # Height of the window
screen = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Adding health state")  # Title of the window

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

# Setting up the font for displaying the score
font = pygame.font.SysFont("helvetica", 30, 1, 1)
score = 0  # Initialize score

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
        self.left = False  # Movement direction flag (left)
        self.right = False  # Movement direction flag (right)
        self.walkCount = 0  # Animation frame counter
        self.standing = True  # Standing flag
        self.hitbox = (self.x, self.y, self.width, self.height)  # Player's collision box
        self.hit = pygame.Rect(self.hitbox)  # Pygame rectangle for hitbox

    def draw(self, screen):
        # Draw the player with animation
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:  # If player is moving
            if self.left:
                screen.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:  # If player is standing
            if self.right:
                screen.blit(walkRight[0], (self.x, self.y))
            else:
                screen.blit(walkLeft[0], (self.x, self.y))

        # Update the hitbox
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.hit = pygame.Rect(self.hitbox)

    def touch(self):
        # Reset player position on touch
        self.x = 0
        self.y = w_height - self.height

# Define the `projectile` class for bullets
class projectile():
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction  # Direction of the projectile
        self.vel = 8 * direction  # Speed of the projectile

    def draw(self, screen):
        # Draw the projectile
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
        self.health = 9  # Enemy health
        self.visible = True  # Enemy visibility flag

    def draw(self, screen):
        # Draw the enemy with animations and health bar
        self.move()  # Move the enemy
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
            pygame.draw.rect(screen, "grey", (self.hitbox[0], self.hitbox[1] + 3, 50, 10))  # Background health bar
            pygame.draw.rect(screen, "green", (self.hitbox[0], self.hitbox[1] + 3, 50 - (5.5 * (9 - self.health)), 10))  # Health level

    def move(self):
        # Move the enemy within the defined path
        if self.vel > 0:  # Moving right
            if self.x < self.path[1] - self.width + 20:
                self.x += self.vel
            else:
                self.vel = -self.vel
                self.walkCount = 0
        else:  # Moving left
            if self.x > self.path[0] - 20:
                self.x += self.vel
            else:
                self.vel = -self.vel
                self.walkCount = 0

    def touch(self):
        # Reduce health on touch
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False  # Hide enemy if health is depleted

# Function to draw game elements
def DrawInGameloop():
    screen.blit(bg_img, (0, 0))  # Draw background
    clock.tick(25)  # Set frame rate
    soldier.draw(screen)  # Draw player
    text = font.render("Score : " + str(score), 1, "red")  # Display score
    screen.blit(text, (0, 10))
    enemy.draw(screen)  # Draw enemy
    for bullet in bullets:  # Draw projectiles
        bullet.draw(screen)
    pygame.display.flip()  # Update the display

# Initialize game objects
soldier = player(210, 435, 64, 64)
enemy = enemy(0, w_height - 64, 64, 64, w_width)
bullets = []  # List to store bullets
shoot = 0  # Shooting cooldown

# Main game loop
done = True
while done:
    for event in pygame.event.get():  # Handle events
        if event.type == pygame.QUIT:  # Quit game if close button is clicked
            done = False

    # Collision between player and enemy
    if enemy.visible:
        if soldier.hit.colliderect(enemy.hit):  # Check for collision
            enemy.vel = -enemy.vel  # Reverse enemy direction
            soldier.touch()  # Reset player position

    # Shooting cooldown
    if shoot > 0:
        shoot += 1
    if shoot > 3:
        shoot = 0

    # Handle bullet collisions and movement
    for bullet in bullets:
        if enemy.visible:
            if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > enemy.hitbox[1]:
                if bullet.x + bullet.radius > enemy.hitbox[0] and bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]:
                    bullets.pop(bullets.index(bullet))  # Remove bullet on hit
                    score += 1  # Increment score
                    enemy.touch()  # Reduce enemy health

        if 0 < bullet.x < 500:  # Move bullets within bounds
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))  # Remove bullets out of bounds

    # Handle player input
    keys = pygame.key.get_pressed()

    # Shooting bullets
    if keys[pygame.K_SPACE] and shoot == 0:
        direction = 1 if soldier.right else -1
        if len(bullets) < 5:  # Limit bullets
            bullets.append(projectile((soldier.x + soldier.width // 2), (soldier.y + soldier.height // 2), 6, "black", direction))
        shoot = 1

    # Movement controls
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
        if keys[pygame.K_UP]:  # Start jump
            soldier.is_jump = True
            soldier.right = False
            soldier.left = False
    else:  # Jump motion
        if soldier.jump_count >= -10:
            neg = 1 if soldier.jump_count > 0 else -1
            soldier.y -= (soldier.jump_count ** 2) * neg * 0.5
            soldier.jump_count -= 1
        else:
            soldier.jump_count = 10  # Reset jump
            soldier.is_jump = False

    DrawInGameloop()  # Redraw all elements
