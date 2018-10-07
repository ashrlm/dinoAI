#!/usr/bin/env python3

import random
import pygame
from pygame.locals import *

def play():
    size = (1350, 675)
    screen = pygame.display.set_mode(size)
    gravity = 2
    speed = 10

    class Entity():

        enemies = []

        def __init__(self, img_path, enemy=True):
            self.image = pygame.image.load(img_path)
            self.alive = True
            ## NOTE: Hitboxes are handled by self.__init__, as Xpos and Ypos are needed,
            ##       and they are not generated until then due to changing necessities

            if enemy:

                if self.__class__.instances != []: #Generate XPOS - YPOS HANDLED BY SELF CLASS
                    self.xpos = self.__class__.instances[-1].xpos + random.randint(100, 1000)
                else:
                    self.xpos = size[0]

                if random.random() >= 2: #Sometimes scale (70%)
                    size_x = self.image.get_size()[0]
                    size_y = self.image.get_size()[1]

                    new_x = abs(random.randint(size_x-50, size_x+300)) #size_x +500 to allow the equivilant of multiple cacti
                    new_y = abs(random.randint(size_y-50, size_y+50))

                    self.image = pygame.transform.scale(self.image, (new_x, new_y))
                    self.hitbox = self.image.get_rect()

                Entity.enemies.append(self) #Add self to list of enemies
                self.__class__.instances.append(self) #Add self to instances stored in instances (class variable)

        def update(self):
            if self.alive: #Only update if still alive
                self.xpos -= speed #Only update XPOS - Constant YPOS for all enemies
                self.hitbox.x = self.xpos
                if random.random() > .999: #Chance to generate an emeny of same type as self
                    self.__class__() #No need to assign, handled by __init__

            else: #If entity dead, remove them from list(s)
                Entity.enemies.remove(self)
                if type(self).__name__ == "Bird":
                    Bird.birds.remove(self)

            if random.random() > .999: #Very infrequently add enemies
                # NOTE: Edit the frequency later
                self.__class__()


    class Player(Entity):

        instances = []

        def __init__(self):
            super().__init__('assets/dino.png', enemy=False)
            self.xpos = 50
            self.ypos = size[1] - self.image.get_size()[1]
            self.hitbox = self.image.get_rect(topleft=(self.xpos, self.ypos))
            self.yvel = 0
            self.jumping = False
            self.ducking = False
            self.score = 0

        def jump(self):
            if not self.jumping:
                self.jumping = True
                self.yvel = 25 #Temp: CHNAGE LATER

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

                if self.ypos - self.yvel > size[1] - self.image.get_size()[1]:
                    self.ypos = size[1] - self.image.get_size()[1]
                    self.jumping = False

                else:
                    self.ypos -= self.yvel
                    self.yvel -= gravity
                    print(self.yvel)



    class Cactus(Entity):

        instances = []

        def __init__(self):
            super().__init__('assets/cactus.png')
            self.ypos = size[1] - self.image.get_size()[1]
            self.hitbox = self.image.get_rect(topleft=(self.xpos, self.ypos))

    class Bird(Entity):

        instances = []

        def __init__(self):
            self.type = random.randint(0,2) #High: 0, Mid: 1, Low: 2
            super().__init__('assets/bird.png')
            self.ypos = 100 + (50 * self.type)
            self.hitbox = self.image.get_rect(topleft=(self.xpos, self.ypos))

    #Generate initial enemies to work off of - Otherwise never created
    Bird()
    Cactus()

    curr_player = Player()
    clock = pygame.time.Clock()

    while curr_player.alive:

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quit()
            if event.type==pygame.KEYDOWN:
                print(1)
                curr_player.jump()


        screen.fill((255,255,255))

        screen.blit(curr_player.image, (curr_player.xpos, curr_player.ypos))

        for enemy in Entity.enemies:
            enemy.update()
            screen.blit(enemy.image, (enemy.xpos, enemy.ypos))
            if curr_player.hitbox.colliderect(enemy.hitbox):
                curr_player.alive = False
                break

        curr_player.update()

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    play()