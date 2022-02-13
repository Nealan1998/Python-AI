import pygame
import Constants
import random
from Vector import Vector
from Agent import Agent

class Enemy(Agent):
    
    def __init__(self, position, size, speed, color):
        super().__init__( position, speed, size, color)
        self.direction = Vector(0,0)
        self.tagged = False
        self.wanderVector = Vector(random.uniform(-1.0,1.0), random.uniform(-1.0,1.0))
        self.changeDirection = Constants.FRAME_RATE * 5
    

    def update(self, player):
        # Get key input from user]
        playerDirection = self.position - player.position
        
        # Handle Chased players
        if playerDirection.length() < 200.0 and self.tagged == False:
            self.velocity = playerDirection.normalize()
        # Handle Enemies not being chased to wanter
        else:
            velPerp = Vector((self.velocity.y * -1), self.velocity.x).scale(.1)
            velPerp = velPerp.scale(random.uniform(-1,1))
            self.direction = self.velocity + velPerp#Vector((random.uniform(-1, 1)), (random.uniform(-1, 1)))
            self.velocity = self.direction.normalize()
        # Decide to change direction
        #if (self.changeDirection <= 0):
            #self.wanderVector = Vector(random.uniform(-1.0,1.0), random.uniform(-1.0,1.0))
            #self.changeDirection = Constants.FRAME_RATE * 5
        # Update Movement
        if (self.tagged == False):
            super().update()
        else:
            self.velocity = Vector(0,0)
            super().update()