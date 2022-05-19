import pygame
import random
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
clock = pygame.time.Clock()
clock.tick(30)
index = []
   # Draw the obstacles on the screen
# Fill the screen with black
        
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((0, 0, 0))

class Obstacles(pygame.sprite.Sprite):
    def __init__(self):
        super(Obstacles, self).__init__()
        self.surf = pygame.image.load("brick.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect() 
obstacle = Obstacles()
for x in range(2):
    for y in range(2):
        screen.blit(obstacle.surf, (SCREEN_WIDTH/8+x*40, SCREEN_HEIGHT/8+y*40))
for x in range(2):
    for y in range(2):
        screen.blit(obstacle.surf, (SCREEN_WIDTH/8+x*40, SCREEN_HEIGHT*6/8+y*40))
for x in range(2):
    for y in range(2):
        screen.blit(obstacle.surf, (SCREEN_WIDTH*6/8+x*40, SCREEN_HEIGHT/8+y*40))
for x in range(2):
    for y in range(2):
        screen.blit(obstacle.surf, (SCREEN_WIDTH*6/8+x*40, SCREEN_HEIGHT*6/8+y*40))
class Bullets(pygame.sprite.Sprite):
    def __init__(self):
        super(Bullets, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                300,
                300
            )
        )
    def update(self):
        self.rect.move_ip(0, 5)
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = 0

class Tanks(pygame.sprite.Sprite):
    def __init__(self):
        super(Tanks, self).__init__()
        self.surf = pygame.image.load("tank.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.surf = pygame.image.load("tank.png").convert()
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.surf = pygame.image.load("tank_down.png").convert()
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.surf = pygame.image.load("tank_left.png").convert()
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.surf = pygame.image.load("tank_right.png").convert()
            self.rect.move_ip(5, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def kill(self):
        self.surf = pygame.image.load("killed.png").convert()
class Enemy_tanks(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy_tanks, self).__init__()
        self.surf = pygame.image.load("tank_enemy.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(20, SCREEN_WIDTH-20),
                random.randint(20, SCREEN_HEIGHT-20),
            )
        )
        self.speed = 5
    def update(self):
        while True:
            i = random.randint(1,4)
            if i == 1:
                self.rect.move_ip(5, 0)
                if self.rect.right < 0:
                    self.rect.right=0
            elif i == 2:
                self.rect.move_ip(-5, 0)
                if self.rect.left < 0:
                    self.rect.left=0
            elif i == 3:
                self.rect.move_ip(0, 5)
                if self.rect.top < 0:
                    self.rect.top=0
            else:
                self.rect.move_ip(0, -5)
                if self.rect.bottom < 0:
                    self.rect.bottom=0

ADDENEMY = pygame.USEREVENT + 1
FIRE = pygame.USEREVENT + 2

pygame.time.set_timer(ADDENEMY, 1000, loops = 1)
pygame.time.set_timer(FIRE, 100)
# Objects
tank = Tanks()

# tank_bullet = Bullets()
# new_enemy = Enemy_tanks()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(tank)


# Variable to keep the main loop running
running = True

# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False
        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy_tanks()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            screen.blit(new_enemy.surf, new_enemy.rect)
#             new_enemy.update()
           
        # Fire a bullet
        elif event.type == FIRE:
            tank_bullet = Bullets()
            enemies.add(tank_bullet)
            all_sprites.add(tank_bullet)
            screen.blit(tank_bullet.surf, tank_bullet.rect)
#             tank_bullet.update()

#     for entity in all_sprites:
#         screen.blit(entity.surf, entity.rect)

        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(tank, enemies):
        # If so, then remove the player and stop the loop
            tank.kill()
    # running = False            
            
    

    # Draw the tank on the screen
#     screen.blit(tank.surf, tank.rect)
 
    
#     for entity in all_sprites:
#         screen.blit(entity.surf, entity.rect)
    
    pressed_keys = pygame.key.get_pressed()
    # Update the player sprite based on user keypresses
    tank.update(pressed_keys)
   
    # Update the display
    pygame.display.flip()
pygame.quit()