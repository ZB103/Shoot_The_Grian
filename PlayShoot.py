#Simple shooter game where GoodTimesWithScar HoTgUys Grian
# https://youtube.com/playlist?list=PLU2851hDb3SEbbc0Zx5KTD6-heWGGaKrb Grian's Hermitcraft season 9
# https://youtu.be/ybMNoh3jr7w GoodTimesWithScar hOtGuY-ing people
#################################################
import pygame
from pygame import mixer
from random import randint, choice
from Constants import *
from time import sleep

#Add sound

class ScarSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = WIDTH/2
        self.y = HEIGHT - (HEIGHT/6)
        self.image = pygame.image.load("Hotguy.png")
        self.width = self.image.get_width()
    
    def getPosition(self):
        return (self.x, self.y)
    
    #moves Scar to the left
    def goLeft(self, amount=1):
        if(self.x >= 0):
            self.x -= amount
    
    #moves Scar to the right
    def goRight(self, amount=1):
        if(self.x <= WIDTH - self.width):
            self.x += amount
    
    def process(self, pK):
        if pK[K_LEFT]:
            self.goLeft()
        if pK[K_RIGHT]:
            self.goRight()
        if pK[K_SPACE]:
            if (len(projectiles) <= 20):
                projectiles.append(Projectile())
                sleep(.01)
   
class GrianSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.setRandomPosition()
        self.image = pygame.image.load("Cuteguy.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    
    #position (X & y)
    def setRandomPosition(self):
        self.x = randint(0, WIDTH)
        self.y = randint(0, HEIGHT/2)
    
    def getPosition(self):
        return (self.x, self.y)
    
    def moveGrian(self):
        direction = randint(0, 1)
        if(direction == 0):
            if(grian.x < WIDTH - self.width):
                self.x += 10
        else:
            if(grian.x >= 0):
                self.x -= 10
    
    #When Grian is hit with a projectile, this will be called. It makes Grian disappear
    #and resets him elsewhere at a random position
    def grianBooped(self):
        global score
        hawkeye.play()
        self.image = pygame.image.load("noCuteguy.png")
        self.setRandomPosition()
        self.image = pygame.image.load("Cuteguy.png")
        score += 1
        for i in range(len(projectiles)):
            projectiles[0].killProjectile()

class Projectile(pygame.sprite.Sprite):
    def __init__(self):
        self.x = scar.x + 5
        self.y = scar.y
        
    def draw(self):
        pygame.draw.circle(screen, BLACK, (self.x, self.y), 5)
    
    def update(self):
        #if projectile's y is between grian's y and grian's y + width and projectile's  is grian's x
        if(self.x >= grian.x and self.x <= (grian.x + grian.width) and self.y <= grian.y and self.y >= (grian.y - grian.height)):
            self.killProjectile()
            grian.grianBooped()
        if(self.y <= 0):
            self.killProjectile()
        else:
            self.y -= 1
            self.draw()
        
    def killProjectile(self):
        global projectiles
        try:
            del projectiles[0]
        except:
            pass
    
####MAIN####
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#create sprite objects - Scar = "wizard"; Grian = "spider"
scar = ScarSprite()
grian = GrianSprite()
projectiles = []

#Establish scoring system
score = 0
myFont = pygame.font.Font("Hhenum-Regular.otf", 30)

#Sound
mixer.init()
hawkeye = mixer.Sound("Hawkeye.mp3")
music = mixer.music.load("Howling.mp3")
mixer.music.set_volume(1)
mixer.music.play(-1)

RUNNING = True
while(RUNNING):
    for event in pygame.event.get():
        #Check if game has been quit
        if(event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE)):
            RUNNING = False
        
    screen.fill(WHITE)
    #Otherwise, process what has been pressed and move Scar
    pressedKeys = pygame.key.get_pressed()
    scar.process(pressedKeys)
    for shooty in projectiles:
        shooty.update()
        
    
    #Move Grian and projectiles
    grian.moveGrian()
    
    text = myFont.render('Score: ' + str(score), 1, BLACK)
    
    #Establish screen
    screen.blit(scar.image, scar.getPosition())
    screen.blit(grian.image, grian.getPosition())
    screen.blit(text, (700, 10))
    pygame.display.flip()