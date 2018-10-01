import pygame
from pygame.locals import *

screen = pygame.display.set_mode((1200, 800))

class Entity():

    enimies = []

    def __init__(self, img_path, enemy=True):
        self.image = pygame.image.load(img_path)
        self.hitbox = self.image.get_rect()

        if enemy:
            Entity.enemies.append(self)


class Player(Entity):
    def __init__(self):
        super().__init__('assets/dino.png', enemy=False)
        self.alive = True
        self.xpos = 50
        self.ypos = 600 - self.image.get_size()[1]
        self.yvel = 0
        self.jumping = False

    def play(network):
        results = {}
        score = 0
        while self.alive:
            network_activation = network.activate

            if network_activation.md == "jump":
                self.jumping = True
                self.yvel = 100
            elif network_activation.md == "duck":
                super().__init__('assets/dino_duck.png')

            elif network_activation.md = "still":
                pass

            else:
                print("This should never happen. Fix NOW!!")
                quit()

            for obstacle in Entity.enemies:
                if self.hitbox.colliderect(obstacle.hitbox):
                    self.alive = False

            score += 1

        return score

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

player = Player()

# TODO: FIX PLAY FUNCTION

def play(networks):
    pass

'''def play(network):

    clock = pygame.time.Clock()
    score = 0
    gameover = False

    while True:

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quit()

        output = network.activate()

        if output.md == "jump":
            player.jump()
        elif output.md == "duck":
            player.duck()

        screen.blit(player.image, (player.x, player.y))

        for enemy in Cactus.cacti + Bird.birds:
            screen.blit(enemy, (enemy.xpos, enemy.ypos))
            if player.hitbox.colliderect(enemy.hitbox):
                gameover=True

        if gameover:
            break
        else:
            score += 1
            clock.tick(30)

    return score'''