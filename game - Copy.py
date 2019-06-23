import pygame
from os import path

# Width and Height
WIDTH = 1500
HEIGHT = 686

# FPS
FPS = 45
acc = 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Initialise game window and mixer for sound
pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hero")
clock = pygame.time.Clock()

# Settting image for enemy and player
img_dir = path.join(path.dirname(__file__), "Enemy sprites")
img_dir2 = path.join(path.dirname(__file__), "player")
enemy_img = pygame.image.load(path.join(img_dir, "slime.png")).convert()
player_img = pygame.image.load(path.join(img_dir2, "player3.png")).convert()
background_img = pygame.image.load(path.join(img_dir2, "bg41.png")).convert()
platform_img = pygame.image.load(path.join(img_dir2, "platform2.png")).convert()
platform_img2 = pygame.image.load(path.join(img_dir2, "platform31.png")).convert()

# Setting up sounds for enemy and player
collision = pygame.mixer.Sound(path.join(path.dirname(__file__), "Hit_Hurt5.wav"))
#back_music = pygame.mixer.music(path.join(path.dirname(__file__), 

# Define classes
class Player(pygame.sprite.Sprite):
     def __init__(self):
          pygame.sprite.Sprite.__init__(self)
          self.walkCount = 0
          self.jump = False
          self.jump_count = 10
          self.current_frame = 0
          self.last_update = 0
          self.image = player_img
          self.image.set_colorkey(BLACK)
          self.rect = self.image.get_rect()
          self.rect.centerx = WIDTH / 2
          self.rect.bottom = 100
          self.speedx = 0
          self.speedy = 0
          self.lives = 10
          self.y_speed = 0

     def update(self):
          self.speedx = 0
          self.speedy = 12
          keys = pygame.key.get_pressed()
          if keys[pygame.K_LEFT]:
               self.speedx = -5
          if keys[pygame.K_RIGHT]:
               self.speedx = 5
          self.rect.x += self.speedx
          '''if not (self.jump):
               if keys[pygame.K_SPACE]:
                    self.jump = True
          else:
               if self.jump_count > -10:
                    self.neg = 1
                    if self.jump_count < 0:
                         self.neg = -1
                         self.speedy = 0
                    self.rect.bottom -= (self.jump_count ** 2) * 0.8 * self.neg
                    self.jump_count -= 1
               else:
                    self.jump = False
                    self.jump_count = 10'''
          self.rect.bottom += self.speedy
          if self.rect.right > WIDTH:
               self.rect.right = WIDTH
          if self.rect.left < 0:
               self.rect.left = 0
          if self.jump:
               self.y_speed = -18
               self.jump = False
          self.rect.bottom += self.y_speed

          hits2 = pygame.sprite.spritecollide(self, plat, False)
          for hit in hits2:
               if self.on_ground():
                    if self.y_speed >= 0:
                         self.rect.bottom = hit.rect.top + 1
                         self.y_speed = 0
                    else:
                         self.rect.top = hit.rect.bottom
                         self.y_speed = 2
               else:
                    self.y_speed += acc

     def on_ground(self):
        collision = pygame.sprite.spritecollide(self, plat, False)
        if collision:
            return True
        else:
            return False


     
class Enemies(pygame.sprite.Sprite):
     def __init__(self):
          pygame.sprite.Sprite.__init__(self)
          self.image = pygame.transform.scale(enemy_img, (40, 20))
          self.image.set_colorkey(BLACK)
          self.rect = self.image.get_rect()
          self.rect.left = -15
          self.rect.bottom = HEIGHT - 55
          self.speedx = 2
               
     def update(self):
          self.rect.x += self.speedx
          if self.rect.left > WIDTH:
               self.speedx = 2
               self.rect.right = -10

class Platforms(pygame.sprite.Sprite):
     def __init__(self, posx, posy):
          pygame.sprite.Sprite.__init__(self)
          self.image = pygame.transform.scale(platform_img, (200, 58))
          self.image.set_colorkey(WHITE)
          self.rect = self.image.get_rect()
          self.rect.x = posx
          self.rect.y = posy

class Platforms2(pygame.sprite.Sprite):
     def __init__(self, posx, posy):
          pygame.sprite.Sprite.__init__(self)
          self.image = pygame.transform.scale(platform_img2, (WIDTH, 55))
          self.image.set_colorkey(WHITE)
          self.rect = self.image.get_rect()
          self.rect.x = posx
          self.rect.y = posy


def score_output(surf, text, size, x, y):
     font_name = pygame.font.match_font('arial')
     font = pygame.font.Font(font_name, size)
     score_text = font.render(text + str(score), True, (BLUE))
     surf.blit(score_text, (x, y))
               
# Sprites group
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

mob = pygame.sprite.Group()
enemies = Enemies()
mob.add(enemies)
all_sprites.add(enemies)

plat = pygame.sprite.Group()
platforms = [Platforms(400, 500), Platforms2(0, HEIGHT - 58), Platforms(600, 350)]
for i in platforms:
     plat.add(platforms)
     all_sprites.add(platforms)

# Game loop
ver = 0
score = 0
running = True
while running:
     # Keep loop running at the right speed
     clock.tick(FPS)
    
     # Events in pygame
     for event in pygame.event.get():
          if event.type == pygame.QUIT:
               running = False
          elif event.type == pygame.KEYDOWN:
               if event.key == pygame.K_SPACE and player.on_ground():
                    player.jump = True

     # Update
     all_sprites.update()

     #Check for collision
     hits = pygame.sprite.spritecollide(player, mob, True)
     for hit in hits:
          score += 2
          m = Enemies()
          mob.add(m)
          all_sprites.add(m)
     if hits:
          collision.play()
          player.lives -= 1
          if player.lives == 0:
               running = False

          
          

     # Draw on window
     window.blit(background_img, (0, 0))
     score_output(window, "Score: ", 25, 1100, 20)
     all_sprites.draw(window)

     pygame.display.flip()
     
pygame.quit()
