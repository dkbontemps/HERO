import pygame
from os import path

# Width and Height
WIDTH = 800
HEIGHT = 500

# FPS
FPS = 56

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Initialise game window and mixer for sound
pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hero")
clock = pygame.time.Clock()

# Setttin image for enemy and player
img_dir = path.join(path.dirname(__file__), "Enemy sprites")
img_dir2 = path.join(path.dirname(__file__), "player")
enemy_img = pygame.image.load(path.join(img_dir, "slime.png")).convert()

# Define classes
class Player(pygame.sprite.Sprite):
     def __init__(self):
          pygame.sprite.Sprite.__init__(self)
          self.walking = False
          self.current_frame = 0
          self.last_update = 0
          self.load_image()
          self.image = self.stand
          self.rect = self.image.get_rect()
          self.rect.centerx = WIDTH / 2
          self.rect.bottom = HEIGHT
          self.speedx = 0

     def  load_image(self):
         self.walk_right = [pygame.image.load(path.join(img_dir2, "Right (1).png")).convert(), pygame.image.load(path.join(img_dir2, "Right (2).png")).convert(), pygame.image.load(path.join(img_dir2, "Right (3).png")).convert(),
                            pygame.image.load(path.join(img_dir2, "Right (4).png")).convert(), pygame.image.load(path.join(img_dir2, "Right (5).png")).convert(), pygame.image.load(path.join(img_dir2, "Right (6).png")).convert(),
                            pygame.image.load(path.join(img_dir2, "Right (7).png")).convert(), pygame.image.load(path.join(img_dir2, "Right (8).png")).convert(), pygame.image.load(path.join(img_dir2, "Right (9).png")).convert(),
                            pygame.image.load(path.join(img_dir2, "Right (10).png")).convert(), pygame.image.load(path.join(img_dir2, "Right (11).png")).convert(), pygame.image.load(path.join(img_dir2, "Right (12).png")).convert()]
         for frame in self.walk_right:
               frame.set_colorkey(WHITE)
               
         self.walk_left = []
         for frames in self.walk_right:
              self.walk_left.append(pygame.transform.flip(frames, True, False))
              frame.set_colorkey(WHITE)

         self.stand = pygame.image.load(path.join(img_dir2, "Right (1).png")).convert()
         self.stand.set_colorkey(WHITE)

     def update(self):
          self.animate()
          self.speedx = 0
          keys = pygame.key.get_pressed()
          if keys[pygame.K_LEFT]:
               self.speedx = -5
          if keys[pygame.K_RIGHT]:
               self.speedx = 5
          self.rect.x += self.speedx
          if self.rect.right > WIDTH:
               self.rect.right = WIDTH
          if self.rect.left < 0:
               self.rect.left = 0

     def animate(self):
          now = pygame.time.get_ticks()
          if not self.walking:
               if now - self.last_update > 100:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.walk_right)
                    self.image = self.walk_right[self.current_frame]
     
class Enemies(pygame.sprite.Sprite):
     def __init__(self):
          pygame.sprite.Sprite.__init__(self)
          self.image = pygame.transform.scale(enemy_img, (49, 34))
          self.image.set_colorkey(BLACK)
          self.rect = self.image.get_rect()
          self.rect.left = 0
          self.rect.bottom = HEIGHT
          self.speedx = 2


     def update(self):
          self.rect.x += self.speedx
          if self.rect.right > WIDTH:
               self.speedx = -2
          if self.rect.left < 0:
               self.speedx = 2
          
# Sprites group
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

mob = pygame.sprite.Group()
enemies = Enemies()
mob.add(enemies)
all_sprites.add(enemies)

# Game loop
running = True
while running:
     # Keep loop running at the right speed
     clock.tick(FPS)

     # Events in pygame
     for event in pygame.event.get ():
          if event.type == pygame.QUIT:
               running = False

     # Update
     all_sprites.update()

     #Check for collision
     hits = pygame.sprite.spritecollide(player, mob, False)
     if hits:
          player.kill()

     # Draw on window
     window.fill(BLACK)     
     all_sprites.draw(window)

     pygame.display.flip()
     
pygame.quit()
