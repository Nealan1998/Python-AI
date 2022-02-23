import pygame
import Constants
import random
import datetime
from Vector import Vector
from Agent import Agent

class Player(Agent):

    def __init__(self, position, size, speed, image, turnSpeed):
        super().__init__(position, size, speed, image, turnSpeed)
        self.targetAgent = None
        self.direction = Vector(0,0)
        self.weightToUse = Constants.PLAYER_WEIGHT
        self.turningSpeed = Constants.PLAYER_TURN_SPEED

    def update(self, bounds, shaunAndFriends, clock):
        # Choose target randomly
        if self.targetAgent == None:
            self.targetAgent = random.choice(shaunAndFriends)
        self.target = self.targetAgent.position
        self.direction = self.target - self.position
        # Change target
        test = super().isInCollision(self.targetAgent)
        if test == True:
           self.targetAgent = None
        # Call update
        super().update(bounds, clock, [self] + [shaunAndFriends])

    def draw(self, screen):
        pygame.draw.line(screen, (255,0,0), self.center.tuple() ,self.target.tuple(),3 )
        super().draw(screen)