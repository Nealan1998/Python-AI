import pygame
import Constants
import random
from Vector import Vector
from Agent import Agent

class Sheep(Agent):
    
    def __init__(self, position, size, speed, image, turnSpeed):
        super().__init__(position, size, speed, image, turnSpeed)
        self.velocity = Vector(random.uniform(-1,1),random.uniform(-1,1))
        self.maxSpeed = speed
        self.isFleeing = False
        self.target = Vector(0,0)
        self.direction = self.velocity.normalize()
        self.weightToUse = Constants.SHEEP_WANDER_WEIGHT
        self.turningSpeed = Constants.SHEEP_TURN_SPEED

    def switchMode():
        if self.isFleeing == True:
            self.isFleeing = False
        else:
            self.isFleeing = False


    def calculateNeighborhood(self, herd):
        # Calculate the neighborhood
        self.neighborAmount = 0
        self.neighborhood = []
        self.boundaries = []

        for sheep in herd:
            if  sheep is not self:
                if(self.center - sheep.position).length() < 40:
                    self.neighborAmount += 1
                    self.neighborhood += [sheep]
    

    def calculateAlignment(self, herd):
        # Reset
        alignment = Vector(0,0)

        for sheep in self.neighborhood:
            alignment += sheep.velocity

        # In case of no neighbors
        if(self.neighborAmount == 0):
            return alignment
        else:
            return alignment.scale(1 / self.neighborAmount)

    def calculateCohesion(self, herd):
        cohesion = Vector(0,0)

        for sheep in self.neighborhood:
            cohesion += sheep.position
        
        if self.neighborAmount > 0:
            cohesion = cohesion.scale(1 / self.neighborAmount) - self.center

        return cohesion

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

    def update(self, bounds, player, clock, herd):
        
        self.calculateNeighborhood(herd)

        alignment = self.calculateAlignment(herd)
        alignment = alignment.normalize()

        cohesion = self.calculateCohesion(herd)
        cohesion = cohesion.normalize()

        direction = alignment.scale(Constants.SHEEP_ALIGNMENT_WEIGHT) + cohesion.scale(Constants.SHEEP_COHESION_WEIGHT)
        
        if abs(direction.x) < 0.001 and abs(direction.y) < 0.001:
            self.speed = 0
        else: 
            self.updateVelocity(direction)
            self.speed = self.maxSpeed
        # Find player
        #self.target = player.position
        #self.isPlayerClose()
        # Fleeing behavior
        #if self.isFleeing == True:
        #    self.direction = self.position - self.target
        # Wandering behavior
        #else:
        #    velPerp = Vector((self.velocity.y * -1), self.velocity.x).scale(.1)
        #    velPerp = velPerp.scale(random.uniform(-1,1))
        #    self.direction = self.velocity + velPerp
        super().update(bounds, clock)

    def draw(self, screen):
        if self.isFleeing == True:
            # Draw a line to the player in red
            pygame.draw.line(screen, (0,255,0), self.center.tuple() ,self.target.tuple(),1 )
        super().draw(screen)

    