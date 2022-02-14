import pygame
import Constants
import math
from Vector import Vector

class Agent:
    
    def __init__(self, position, size, speed, image):
        self.position = position
        self.size = size
        self.speed = speed
        self.image = image
        self.velocity = Vector(0,0)
        self.target = Vector(0,0)
        self.boundingRect = pygame.Rect(0,0,0,0)
        self.updateRect()
        self.updateCenter()
        self.angle =0
        self.upperLeft = Vector(0,0)
        self.surf = None

    def __str__(self):
        # Override string
        return (f"Player Size: {str(self.size)}	Position: {str(self.position)}	Velocity: {str(self.velocity)}	Center: {str(self.center)}")

    def updateVelocity(self, velocity):
        # Recieve new velocity and normalize it
        self.velocity = velocity.normalize()

    def updateRect(self):
        self.rect = self.boundingRect

    def updateCenter(self):
        # Find the center of the object
        #self.center = self.position + Vector(1,1).scale((self.size)/2)
        self.center = self.position + Vector((self.size / 2),(self.size /2))

    def isInCollision(self, agent):
        # Check if self is colliding with another agent
        if (agent.rect != None):
            return pygame.Rect.colliderect(self.rect, agent.rect)
        else:
            return False

    def update(self, bounds):

        if self.surf != None:
            self.boundingRect = self.surf.get_bounding_rect()
            self.boundingRect = self.boundingRect.move(self.center.x - Constants.AGENT_WIDTH /2, self.center.y - Constants.AGENT_HEIGHT /2)
        # Do not let the agent move outside of the world bounds
        if self.position.x <= 10: self.position.x = 10
        if self.position.x >= Constants.WORLD_WIDTH: self.position.x = Constants.WORLD_WIDTH - 10
        if self.position.y <= 10: self.position.y = 10
        if self.position.y >= Constants.WORLD_HEIGHT: self.position.y = Constants.WORLD_HEIGHT -10

        # Update position
        self.position += self.velocity.scale(self.speed)

        #self.updateRect()
        self.updateCenter()

    def draw(self, screen):
        if(self.surf != None):
            pygame.draw.rect(screen, (0, 0, 0), self.boundingRect, 2)

        # Draw Image
        self.angle = math.atan2(-self.velocity.x, -self.velocity.y)
        self.angle = math.degrees(self.angle)
        self.surf = pygame.transform.rotate(self.image, self.angle)
        upperLeft = Vector((self.center.x - self.surf.get_width() / 2), (self.center.y - self.surf.get_height() /2))
        # Draw a square at the new position
        screen.blit(self.surf, [upperLeft.x, upperLeft.y])

        # Draw a line showing the expected velocity
        pygame.draw.line(screen, (0,0,255), self.center.tuple() ,(self.center + self.velocity.scale(50)).tuple(),3 )
        
