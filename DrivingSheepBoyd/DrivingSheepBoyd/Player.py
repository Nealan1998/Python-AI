import pygame
import Constants
import random
import datetime
from Vector import Vector
from Agent import Agent

class Player(Agent):

    def __init__(self, position, size, speed, image):
        super().__init__(position, size, speed, image)
        self.targetAgent = None
        self.direction = Vector(0,0)

    def update(self, bounds, shaunAndFriends, clock):
        # Choose target randomly
        if self.targetAgent == None:
            self.targetAgent = random.choice(shaunAndFriends)
            self.direction = self.targetAgent.position - self.position
        # Change target
        test = super().isInCollision(self.targetAgent)
        if test == True:
           self.targetAgent = None
        # Call update
        #appliedForce = self.modifyForce()
        super().updateVelocity(self.direction)
        super().update(bounds)

    def modifyForce(self, clock):
        # Set to be a force pushed on player
        appliedForce = self.direction.normalize()
        appliedForce = appliedForce.scale(Constants.PLAYER_WEIGHT)
        appliedForce = appliedForce.normalize()
        if clock.get_time() != 0:
            appliedForce = appliedForce.scale(clock.get_time() / 1000)
        appliedForce = appliedForce.scale(self.speed)
        return appliedForce