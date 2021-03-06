import pygame
import Constants
import random
from Vector import Vector
from Agent import Agent

class Sheep(Agent):
    
    def __init__(self, position, size, speed, image, turnSpeed):
        super().__init__(position, size, speed, image, turnSpeed)

    def switchMode():
        if self.isFleeing == True:
            self.isFleeing = False
        else:
            self.isFleeing = False


    def calculateNeighborhood(self, herd):
        # Map the neighborhood
        self.neighborAmount = 0
        self.neighborhood = []
        self.boundaries = []

        # Add sheep to neighborhood
        for sheep in herd:
            if  sheep is not self:
                if(self.center - sheep.position).length() < Constants.SHEEP_NEIGHBOR_RADIUS:
                    self.neighborAmount += 1
                    self.neighborhood += [sheep]
    

    def calculateAlignment(self, herd):
        # Reset
        alignment = Vector(0,0)

        # Have sheep replicate each other's velocity
        for sheep in self.neighborhood:
            alignment += sheep.velocity

        # In case of no neighbors
        if self.neighborAmount > 0:
            return alignment.scale(1 / self.neighborAmount)
        
        return alignment

    def calculateCohesion(self, herd):
        # Reset
        cohesion = Vector(0,0)

        # Have sheep try to join in groups
        for sheep in self.neighborhood:
            cohesion += sheep.position
        
        # if more than 0
        if self.neighborAmount > 0:
            cohesion = cohesion.scale(1 / self.neighborAmount) - self.center

        return cohesion

    def calculateSeperation(self, herd):
        # Reset
        seperation = Vector(0,0)

        # Don't let sheep overlap
        for sheep in self.neighborhood:
            seperation += self.center - sheep.position

        # if more than 0
        if self.neighborAmount > 0:
            return seperation.scale(1 / self.neighborAmount)
        
        return seperation

    def calculatePlayerFlee(self, player):
        # Flee from player
        newVector = self.center - player.center
        self.target = player

        # Only do so when in range
        if newVector.length() < Constants.MIN_ATTACK_DIST:
            self.isFleeing = True
            return newVector
        else:
            self.isFleeing = False
        return Vector(0,0)

    def calculateBoundaries(self, bounds):
        # reset
        boundsStrength = Vector(0,0)
        self.boundaries = []

        # Calculate x bounds
        if self.center.x < Constants.BOUNDRY_RADIUS:
            boundsStrength -= Vector(0 - self.center.x, 0)
            self.boundaries += [Vector(0, self.center.y)]
        if self.center.x > bounds.x - Constants.BOUNDRY_RADIUS:
            boundsStrength -= Vector(bounds.x - self.center.x, 0)
            self.boundaries += [Vector(bounds.x, self.center.y)]

        # Calculate y bounds
        if self.center.y < Constants.BOUNDRY_RADIUS:
            boundsStrength -= Vector(0, 0 - self.center.y)
            self.boundaries += [Vector(self.center.x, 0)]
        if self.center.y > bounds.y - Constants.BOUNDRY_RADIUS:
            boundsStrength -= Vector(0, bounds.y - self.center.y)
            self.boundaries += [Vector(self.center.x, bounds.y)]

        return boundsStrength

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
        # Check the current neighborhood
        self.calculateNeighborhood(herd)

        # Normalize each force
        dogStrength = self.calculatePlayerFlee(player)
        dogStrength = dogStrength.normalize()

        boundaryStrength = self.calculateBoundaries(bounds)
        boundaryStrength = boundaryStrength.normalize()

        alignment = self.calculateAlignment(herd)
        alignment = alignment.normalize()

        cohesion = self.calculateCohesion(herd)
        cohesion = cohesion.normalize()

        seperation = self.calculateSeperation(herd)
        seperation = seperation.normalize()

        # Add all forces, scaled
        direction = dogStrength.scale(Constants.SHEEP_DOG_WEIGHT * Constants.ENABLE_DOG) + boundaryStrength.scale(Constants.SHEEP_BOUNDARY_WEIGHT * Constants.ENABLE_BOUNDARIES) \
            + alignment.scale(Constants.SHEEP_ALIGNMENT_WEIGHT * Constants.ENABLE_ALIGNMENT) + cohesion.scale(Constants.SHEEP_COHESION_WEIGHT * Constants.ENABLE_COHESION) \
            + seperation.scale(Constants.SHEEP_SEPERATION_WEIGHT * Constants.ENABLE_SEPARATION)
        
        # Normalize and update
        direction = direction.normalize()
        self.updateVelocity(direction)
        
        super().update(bounds, clock, [player] + [herd])

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

    def draw(self, screen):
        if self.isFleeing == True and Constants.DEBUG_DOG_INFLUENCE:
            # Draw a line to the player in red
            pygame.draw.line(screen, (255, 0, 0), (self.center.x, self.center.y),
                             (self.target.center.x, self.target.center.y), Constants.DEBUG_LINE_WIDTH)
            #pygame.draw.line(screen, (0,255,0), self.center.tuple() ,self.target.tuple(),1 )

        if Constants.DEBUG_NEIGHBORS:
            # Draw a line to the neighbors
            for sheep in self.neighborhood:
                pygame.draw.line(screen, (0,0,255), (self.center.x, self.center.y),
                                 (sheep.center.x, sheep.center.y), Constants.DEBUG_LINE_WIDTH)

        if Constants.DEBUG_BOUNDARIES:
            # Draw a line to the boundaries
            for boundary in self.boundaries:
                pygame.draw.line(screen, (255, 0, 255), (self.center.x, self.center.y),
                                 (boundary.x, boundary.y), Constants.DEBUG_LINE_WIDTH)
        super().draw(screen)

    