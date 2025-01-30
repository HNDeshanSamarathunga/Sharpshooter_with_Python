import pygame
import random
pygame.init()

w_width = 500
w_height = 500
screen = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Enhanced Game")

# Clock for controlling FPS
clock = pygame.time.Clock()

# Loading assets
bg_img = pygame.image.load("assets/Img/bg_img.jpeg")
bg_img = pygame.transform.scale(bg_img, (w_width, w_height))
walkRight = [pygame.image.load(f'assets/Img/soldier/{i}.png') for i in range(1, 10)]
walkLeft = [pygame.image.load(f'assets/Img/soldier/L{i}.png') for i in range(1, 10)]
char = pygame.image.load('assets/Img/soldier/standing.png')
moveLeft = [pygame.image.load(f'assets/Img/enemy/L{i}.png') for i in range(1, 10)]
moveRight = [pygame.image.load(f'assets/Img/enemy/R{i}.png') for i in range(1, 10)]

# Sounds
bulletsound = pygame.mixer.Sound("assets/sounds/Bulletsound.mp3")
hitsound = pygame.mixer.Sound("assets/sounds/Hit.mp3")
music = pygame.mixer.music.load("assets/sounds/music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

# Fonts
font = pygame.font.SysFont("helvetica", 30, 1, 1)

# Player attributes
player_lives = 3
score = 0

class player():
    def __init__(self, x, y, width, height):
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
        self.hit = pygame.Rect(self.hitbox)

    def draw(self, screen):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                screen.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                screen.blit(walkRight[0], (self.x, self.y))
            else:
                screen.blit(walkLeft[0], (self.x, self.y))

        self.hitbox = (self.x, self.y, self.width, self.height)
        self.hit = pygame.Rect(self.hitbox)

    def touch(self):
        global player_lives
        hitsound.play()
        player_lives -= 1
        self.x = 0
        self.y = w_height - self.height
        self.is_jump = False
        self.jump_count = 10

class projectile():
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.vel = 8 * direction

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class enemy():
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.walkCount = 0
        self.vel = 3
        self.path = [x, end]
        self.hitbox = (self.x + 20, self.y, self.width - 40, self.height - 4)
        self.hit = pygame.Rect(self.hitbox)
        self.health = 9
        self.visible = True

    def draw(self, screen):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 27:
                self.walkCount = 0

            if self.vel > 0:
                screen.blit(moveRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                screen.blit(moveLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            self.hitbox = (self.x + 20, self.y, self.width - 40, self.height - 4)
            self.hit = pygame.Rect(self.hitbox)
            pygame.draw.rect(screen, "grey", (self.hitbox[0], self.hitbox[1] + 3, 50, 10))
            pygame.draw.rect(screen, "green", (self.hitbox[0], self.hitbox[1] + 3, 50 - (5.5 * (9 - self.health)), 10))

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] - self.width + 20:
                self.x += self.vel
            else:
                self.vel = -self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - 20:
                self.x += self.vel
            else:
                self.vel = -self.vel
                self.walkCount = 0

    def touch(self):
        hitsound.play()
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False

def DrawInGameloop():
    screen.blit(bg_img, (0, 0))
    clock.tick(25)
    soldier.draw(screen)
    text = font.render(f"Score: {score} | Lives: {player_lives}", 1, "red")
    screen.blit(text, (10, 10))
    for enemy_obj in enemies:
        enemy_obj.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    pygame.display.flip()

soldier = player(210, 435, 64, 64)
enemies = [enemy(random.randint(0, w_width - 64), w_height - 64, 64, 64, random.randint(300, w_width)) for _ in range(3)]
bullets = []
shoot = 0
paused = False

while player_lives > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            player_lives = 0

    keys = pygame.key.get_pressed()

    if keys[pygame.K_p]:
        paused = not paused

    if paused:
        continue

    if shoot > 0:
        shoot += 1
    if shoot > 3:
        shoot = 0

    for bullet in bullets[:]:  # Iterate over a copy of the list
        for enemy_obj in enemies:
            if enemy_obj.visible:
                if bullet.y - bullet.radius < enemy_obj.hitbox[1] + enemy_obj.hitbox[3] and bullet.y + bullet.radius > enemy_obj.hitbox[1]:
                    if bullet.x + bullet.radius > enemy_obj.hitbox[0] and bullet.x - bullet.radius < enemy_obj.hitbox[0] + enemy_obj.hitbox[2]:
                        if bullet in bullets:  # Ensure bullet still exists before removing
                            bullets.remove(bullet)
                        score += 1
                        enemy_obj.touch()
                        break  # Stop checking after first hit
                    
        if 0 < bullet.x < w_width:
            bullet.x += bullet.vel
        else:
            if bullet in bullets:
                bullets.remove(bullet)


    for enemy_obj in enemies:
        if enemy_obj.visible and soldier.hit.colliderect(enemy_obj.hit):
            enemy_obj.vel = -enemy_obj.vel
            soldier.touch()

    if keys[pygame.K_SPACE] and shoot == 0:
        bulletsound.play()
        direction = 1 if soldier.right else -1
        if len(bullets) < 5:
            bullets.append(projectile(soldier.x + soldier.width // 2, soldier.y + soldier.height // 2, 6, "black", direction))
        shoot = 1

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

    DrawInGameloop()
 
pygame.quit()
