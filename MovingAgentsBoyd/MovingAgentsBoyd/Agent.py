import pygame
import Constants
from Vector import Vector

class Agent:
    def __init__(self, position, speed, size, color):
        self.position = position
        self.speed = speed
        self.size = size
        self.color = color
        self.velocity = Vector(0,0)
        self.foundSquare = False
        self.target = None
        self.rect = None
        self.center = self.updateCenter()

    def __str__(self):
        # Override string
        return (f"Player Size: {str(self.size)}	Position: {str(self.position)}	Velocity: {str(self.velocity)}	Center: {str(self.center)}")

    def draw(self, screen):
        # Draw a square at the new position
        pygame.draw.rect(screen, self.color, 
            pygame.Rect(self.position.x, self.position.y, self.size, self.size))
        
        # Draw a line showing the expected velocity
        pygame.draw.line(screen, (0,0,255), self.center.tuple() ,(self.center + self.velocity.scale(5)).tuple(),3 )

        # Draw a line to the player / tagged enemy
        if(self.target != None):
            pygame.draw.line(screen, (255,0,0), self.center.tuple() ,self.target.center.tuple(),3 )

    

    def wallCollision(self):
        # Do not let the agent move outside of the world bounds
        if self.position.x <= 0: self.position.x = 10
        if self.position.x >= Constants.WORLD_WIDTH: self.position.x = Constants.WORLD_WIDTH - 10
        if self.position.y <= 0: self.position.y = 10
        if self.position.y >= Constants.WORLD_HEIGHT: self.position.y = Constants.WORLD_HEIGHT -10

    def update(self):
        # Update position
        self.position += self.velocity.scale(self.speed)
        self.wallCollision()
        self.center = self.updateCenter()
        self.rect = pygame.Rect(self.position.x, self.position.y, self.size, self.size)

    def updateCenter(self):
        # Find the center of the object
        center = self.position + Vector(1,1).scale((self.size)/2)
        return center

    def updateRect(self):
        a = 0

    def CheckForCollision(self, foe):
        # Check if self is colliding with another agent
        if (foe.rect != None):
            return pygame.Rect.colliderect(self.rect, foe.rect)
        else:
            return False
