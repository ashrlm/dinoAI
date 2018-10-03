import pygame
from pygame.locals import *

screen = pygame.display.set_mode((1800, 900))
gravity = 9.81

# TODO: Get images for enemies
# TODO: Create enemies
# TODO: Scale all
# TODO: Fix the movement

class Entity():

    enemies = []

    def __init__(self, img_path, enemy=True):
        self.image = pygame.image.load(img_path)
        self.hitbox = self.image.get_rect()
        self.alive = True

        if enemy:
            Entity.enemies.append(self)

    def update(self):
        if self.alive:
            self.xpos -= 1
            if random.random() > .999: #Chance to generate an emeny of same type as self
                self.__class__() #No need to assign, handled by __init__

        else: #If entity dead, remove them from list(s)
            Entity.enemies.remove(self)
            if type(self).__name__ == "Bird":
                Bird.birds.remove(self)


class Player(Entity):
    def __init__(self):
        super().__init__('assets/dino.png', enemy=False)
        self.xpos = 50
        self.ypos = 600 - self.image.get_size()[1]
        self.yvel = 0
        self.jumping = False
        self.ducking = False
        self.score = 0

    def jump(self):
        self.jumping = True
        self.yvel = 100 #Temp: CHNAGE LATER

    def duck(self):
        self.ducking = True

    def update(self):
        self.score += 1

        if self.ducking:
            self.image = pygame.image.load('assets/dinoduck.png')
            self.hitbox = self.image.get_rect()

        if self.jumping:
            self.ducking = False
            self.image = pygame.image.load('assets/dino.png')
            self.hitbox = self.image.get_rect() #Stop ducking when network wants to jump

            if self.ypos + self.yvel < 600 - self.image.get_size()[1]:
                self.ypos = 600 - self.image.get_size()[1]

            else:
                self.ypos += self.yvel
                self.yvel =- gravity



class Cactus(Entity):

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

        if Bird.birds != []:
            self.xpos = Bird.birds[-1].xpos + random.randint(150, 750)
        else:
            self.xpos = 1800

def play(networks):

    scores = {}
    players = {}
    for network in networks:
        players[network] = Player()

    clock = pygame.time.Clock()

    while True:

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quit()

        screen.fill((255,255,255))

        for network in networks:

            curr_player = players[network]

            if curr_player.alive:
                output = network.activate()
                try:
                    if output.md=="jump":
                        curr_player.jump()
                    else:
                        players[network].duck()
                except:
                    pass

            screen.blit(curr_player.image, (curr_player.xpos, curr_player.ypos))

            for enemy in Entity.enemies:
                enemy.update()
                screen.blit(enemy, (enemy.xpos, enemy.ypos))
                if curr_player.hitbox.colliderect(enemy.hitbox):
                    curr_player.alive = False
                    break

            if not curr_player.alive: #Check if the current player is dead
                scores[network] = curr_player.score #Add score to scores
                del players[network] #Remove from list of avaliable players

            curr_player.update()

        pygame.display.flip()
        clock.tick(30)

    for network in players:
        scores[network] = players[network].score #Get score for each network

    return scores