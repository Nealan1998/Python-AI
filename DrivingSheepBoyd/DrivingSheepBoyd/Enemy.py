import pygame
import Constants
import random
from Vector import Vector
from Agent import Agent

class Enemy(Agent):
    
    def __init__(self, position, size, speed, image):
        super().__init__(position, size, speed, image)
        self.velocity = Vector(random.uniform(-1,1),random.uniform(-1,1))
        self.isFleeing = False
        self.target = Vector(0,0)

    def switchMode():
        if self.isFleeing == True:
            self.isFleeing = False
        else:
            self.isFleeing = False

    def isPlayerClose(self):
        # Check if the player is within distance
        playerDirection = self.position - self.target
        # Set enemy to flee
        if playerDirection.length() < Constants.MIN_ATTACK_DIST:
            self.isFleeing = True
            return True
        # Set enemy to wander
        else:
            self.isFleeing = False
            return False

    def calcTrackingVelocity(self, newTarget):
        self.target = newTarget

    def update(self, bounds, player):
        #self.calcTrackingVelocity(player.position)
        #self.isPlayerClose()
        if self.isFleeing == True:
            playerDirection = self.position - self.target
            super().updateVelocity(playerDirection)
        else:
            velPerp = Vector((self.velocity.y * -1), self.velocity.x).scale(.1)
            velPerp = velPerp.scale(random.uniform(-1,1))
            direction = self.velocity + velPerp
            super().updateVelocity(direction)
        super().update(bounds)

    def draw(self, screen):
        if self.isFleeing == True:
            # Draw a line to the player / tagged enemy
            pygame.draw.line(screen, (255,0,0), self.center.tuple() ,self.target.center.tuple(),3 )
        super().draw(screen)