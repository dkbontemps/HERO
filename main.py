import pygame, sys
from os import path
vector = pygame.math.Vector2

#Game class with all attributes
class Game():
     def __init__(self):
          pygame.init()
          self.width = 1000
          self.height = 700
          self.window = pygame.display.set_mode((self.width, self.height))
          self.caption = pygame.display.set_caption("HERO")
          self.clock = pygame.time.Clock()
          self.run = True
          self.BLACK = (0, 0, 0)
          self.WHITE = (255, 255, 255)
          self.BLUE = (0, 0, 255)
          self.GREEN = (0, 255, 0)
          self.RED = (255, 0, 0)
          self.YELLOW = (255, 255, 0)
          self.LIGHT_BLUE = (0, 195, 237)
          self.background = pygame.image.load(path.join(path.join(path.dirname(__file__), 'player'), 'bg2.jpg'))

     def running(self):
          self.playing = True
          while self.playing:
               self.clock.tick(60)
               self.events()
               self.update()
               self.draw()
          
     def new_game(self):
          self.score = 0
          self.sprites = pygame.sprite.Group()
          self.platform_s = pygame.sprite.Group()
          self.player = Player()
          platforms = [Platforms(90, 525, 300, 10), Platforms(0, self.height - 10, self.width, 10),
                                 Platforms(460, 525, 400, 10), Platforms(self.width / 2 - 200, 400, 400, 10),
                                 Platforms(100, 250, 200, 10)]
          for i in platforms:
               self.sprites.add(i)
               self.platform_s.add(i)
          
          self.sprites.add(self.player)
          
     def update(self):
          hits = pygame.sprite.spritecollide(self.player, self.platform_s, False)
          if self.player.vel.y > 0:
               if hits:
                    self.player.position.y = hits[0].rect.top
                    self.player.vel.y = 0
                    self.score += 1
          self.sprites.update()
          if self.player.rect.top > self.height:
               self.playing = False
               
                    
     def events(self):
          events = pygame.event.get()
          for event in events:
               if event.type == pygame.QUIT:
                    if self.playing:
                         self.playing = False
                    self.run = False
               if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                         self.player.jump()
               

     def draw(self):
          self.window.blit(self.background, (0, 0))
          self.sprites.draw(self.window)
          self.score_text("Score: " + str(self.score), 20, self.BLUE, self.width - 125, 15)
          pygame.display.flip()

     def start_screen(self):
          self.window.fill(self.BLACK)
          self.score_text("HERO", 60, self.WHITE, self.width / 1.89, self.height * 0.35)
          self.score_text("Movement: Arrow keys ", 30, self.WHITE, self.width / 1.9, self.height * 0.5)
          self.score_text("Jump: Space bar", 30, self.WHITE, self.width / 1.9, self.height * 0.6)
          pygame.display.flip()
          self.wait_until()
     
     def go_screen(self):
          if not self.run:
               return
          self.window.fill(self.BLACK)
          self.score_text("GAME OVER !", 50, self.WHITE, self.width / 2, self.height * 0.5)
          self.score_text("Press any key to continue", 30, self.WHITE, self.width / 2, self.height * 0.6)
          pygame.display.flip()
          self.wait_until()

     def wait_until(self):
          waiting = True
          while waiting:
               self.clock.tick(60)
               events = pygame.event.get()
               for event in events:
                    if event.type == pygame.QUIT:
                         waiting = False
                         self.run = False
                    if event.type == pygame.KEYUP:
                         waiting =False

     def score_text(self, text, size, color, x, y):
          self.font_name = pygame.font.match_font("roboto")
          self.font = pygame.font.Font(self.font_name, size)
          self.score_surf = self.font.render(text, True, color)
          self.rect = self.score_surf.get_rect()
          self.rect.centerx = x
          self.rect.centery = y
          self.window.blit(self.score_surf, self.rect)

#Class player
class Player(pygame.sprite.Sprite):
     def __init__(self):
          pygame.sprite.Sprite.__init__(self)
          self.walking = False
          self.jumping = False
          self.last_update = 0
          self.current_frame = 0
          self.load_image()
          self.image = self.stand
          self.rect = self.image.get_rect()
          self.rect.x = game.width / 2
          self.rect.y = game.height - 200
          self.position = vector(game.width / 2, game.height - 400)
          self.vel = vector(0, 0)
          self.acc = vector(0, 0)

     def load_image(self):
          self.stand = pygame.transform.scale(spritesheet.image_load(68, 294, 66, 92), (50, 70))

          self.walk_right = [pygame.transform.scale(spritesheet.image_load(0, 294, 68, 93), (50, 70)),
                                        pygame.transform.scale(spritesheet.image_load(0, 100, 70, 96), (50, 70))]
          for i in self.walk_right:
               i.set_colorkey(game.BLACK)

          self.walk_left = []
          for frames in self.walk_right:
               self.walk_left.append(pygame.transform.flip(frames, True, False))
               frames.set_colorkey(game.BLACK)

          self.jmp = pygame.transform.scale(spritesheet.image_load(69, 196, 66, 93), (50, 70))

     def jump(self):
          self.rect.bottom += 1
          hits = pygame.sprite.spritecollide(self, game.platform_s, False)
          self.rect.bottom -= 1
          if hits:
               self.vel.y = -16

     def update(self):
          self.acc = vector(0, 0.8)
          self.animate()
          game.window.blit(self.image, (0, 0))
          keys = pygame.key.get_pressed()
          if keys[pygame.K_RIGHT]:
               self.acc.x = 0.5
          if keys[pygame.K_LEFT]:
               self.acc.x = -0.5

          self.acc.x += self.vel.x * -0.1
          self.vel += self.acc
          self.position += self.vel + 0.5 * self.acc
          
          self.rect.midbottom = self.position

          if self.position.x > game.width - 25:
               self.position.x = game.width - 25
          if self.position. x < 25:
               self.position.x = 25
          if abs(self.vel.x) < 0.3:
               self.vel.x = 0
               self.image = self.stand

     def animate(self):
          now = pygame.time.get_ticks()               
          if not self.walking:
               if now - self.last_update > 200:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % 2
                    if self.vel.x > 0:
                         self.image = self.walk_right[self.current_frame]
                    elif self.vel.x < 0:
                         self.image = self.walk_left[self.current_frame]

class Spritesheets():
     def __init__(self):
          self.dirname = path.dirname(__file__)
          self.img = path.join(self.dirname, 'Spritesheets')
          self.img_load = pygame.image.load(path.join(self.img, 'alienBeige.png')).convert()

     def image_load(self, posx, posy, width, height):
          self.img_surf = pygame.surface.Surface((width, height))
          self.img_surf.blit(self.img_load, (0, 0), (posx, posy, width, height))
          self.img_surf.set_colorkey(game.BLACK)
          return self.img_surf
          
class Platforms(pygame.sprite.Sprite):
     def __init__(self, posx, posy, sizewidth, sizeheight):
          pygame.sprite.Sprite.__init__(self)
          self.image = pygame.surface.Surface((sizewidth, sizeheight))
          self.image.fill(game.BLUE)
          self.rect = self.image.get_rect()
          self.rect.x = posx
          self.rect.y = posy
               
game = Game()
spritesheet = Spritesheets()
game.start_screen()
#Main game loop
while game.run:
     game.new_game()
     game.running()
     game.go_screen()   

pygame.quit()
