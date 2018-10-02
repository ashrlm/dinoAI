import pygame
from pygame.locals import *

screen = pygame.display.set_mode((1200, 800))

# TODO: Get images for enemies
# TODO: Create enemies
# TODO: Scale all

class Entity():

    enemies = []

    def __init__(self, img_path, enemy=True):
        self.image = pygame.image.load(img_path)
        self.hitbox = self.image.get_rect()

        if enemy:
            Entity.enemies.append(self)

    def update(self):
        self.xpos -= 0.1


class Player(Entity):
    def __init__(self):
        super().__init__('assets/dino.png', enemy=False)
        self.alive = True
        self.xpos = 50
        self.ypos = 600 - self.image.get_size()[1]
        self.yvel = 0
        self.jumping = False
        self.score = 0

    def update(self):
        self.xpos += 1
        self.score += 1

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

def play(networks):

    players = {}
    for network in networks:
        players[network] = Player()

    clock = pygame.time.Clock()
    gameover = False

    while True:

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quit()

        screen.fill((255,255,255))

        for network in networks:
            output = network.activate()
            try:
                if output.md=="jump":
                    network.jump()
                elif output.md=="duck":
                    network.duck()
            except:
                pass

        for network in networks:

            curr_player = players[network]
            screen.blit(curr_player.image, (curr_player.xpos, curr_player.ypos))

            for enemy in Entity.enemies:
                enemy.update()
                screen.blit(enemy, (enemy.xpos, enemy.ypos))
                if curr_player.hitbox.colliderect(enemy.hitbox):
                    gameover=True
                    break

            curr_player.update()

        if gameover:
            break

        pygame.display.flip()
        clock.tick(30)

    scores = {}
    for network in players:
        scores[network] = players[network].score

    return scores