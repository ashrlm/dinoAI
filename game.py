import pygame
from pygame.locals import *

screen = pygame.display.set_mode((1200, 800))

class Entity():
    def __init__(self, img_path):
        self.img_path = img_path
        self.hitbox = self.image.get_rect()

class Player(Entity):
    def __init__(self):
        super().__init__('assets/dino.png')
        self.alive = True
        self.xpos = 50
        self.ypos = 600 - self.image.get_size()[1]
        self.yvel = 0
        self.jumping = False
    
    def jump(self):
        pass
    
    def duck(self):
        pass
    
    def play(network):
        results = {}
        score = 0
        while self.alive:
            network_activation = network.activate
            if network_activation.md == "jump":
                self.jump()
            elif network_activation.md == "duck":
                self.duck()
            else:
                print("This should never happen. Fix NOW!!")
                quit()

class Cactus(Entity):

    cacti = []

    def __init__(self):
        super().__init__('assets/cactus.png')
        self.xpos = Cactus.cacti[-1] + random.randint(150, 750)
        self.ypos = 600 - self.image.get_size()[1]

class Bird(Entity):

    birds = []

    def __init__(self):
        self.type = random.randint(0,2) #Low, mid, high
        super().__init__('assets/bird.png')
        self.ypos = (
            550 - self.image.get_size()[1] - (self.type * 50)
        )
        Bird.birds.append(self)
        if Bird.birds == []:
            self.xpos = Bird.birds[-1].xpos + random.randint(150, 750)
        else:
            self.xpos = 1200