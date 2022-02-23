import pygame
import Constants
import math
from Vector import Vector

class Agent:
    
    def __init__(self, position, size, speed, image, turnSpeed):
        self.position = position
        self.size = size
        self.speed = speed
        self.image = image
        self.turnSpeed = turnSpeed
        self.velocity = Vector(0,0)
        self.target = Vector(0,0)
        self.boundingRect = pygame.Rect(0,0,0,0)
        self.updateRect()
        self.updateCenter()
        self.angle =0
        self.upperLeft = Vector(0,0)
        self.surf = None
        self.boundryForces = Vector(0, 0)
        self.boundryList = []
        self.weightToUse = 1
        self.currentDirection =  Vector(0,0)

    def __str__(self):
        # Override string
        return (f"Player Size: {str(self.size)}	Position: {str(self.position)}	Velocity: {str(self.velocity)}	Center: {str(self.center)}")

    def calculateSurface(self):
        self.surf = pygame.transform.rotate(self.image, self.angle)
        self.upperLeft = self.center - Vector(self.surf.get_width(), self.surf.get_height()).scale(.5)
        self.boundingRect = self.surf.get_bounding_rect().move(self.upperLeft.x, self.upperLeft.y)


    def updateVelocity(self, velocity):
        # Recieve new velocity and normalize it
        #self.velocity = velocity.normalize()
        self.targetVelocity = velocity.normalize()

    def moveTowardsTarget(self):
        velocityDifference = self.targetVelocity - self.velocity
        if (velocityDifference.length() < self.turnSpeed):
            self.velocity = self.targetVelocity
        else:
            self.velocity += velocityDifference.normalize().scale(self.turnSpeed)
        self.velocity = self.velocity.normalize()

    def updateRect(self):
        self.rect = self.boundingRect

    def updateCenter(self):
        # Find the center of the object
        self.center = self.position + Vector((self.size / 2),(self.size /2))

    def isInCollision(self, agent):
        # Check if self is colliding with another agent
        if (agent.rect != None):
            return pygame.Rect.colliderect(self.boundingRect, agent.boundingRect)
        else:
            return False

    def update(self, bounds, clock):
        self.moveTowardsTarget()
        self.center = self.center + self.velocity.scale(self.speed)
        
        self.center.x = max(self.boundingRect.width * .5, min(self.center.x,  bounds.x - self.boundingRect.width * .5))
        self.center.y = max(self.boundingRect.height * .5, min(self.center.y, bounds.y - self.boundingRect.height * .5))
        self.calculateSurface()
        ## Debug for no surface
        #if self.surf != None:
        #    self.boundingRect = self.surf.get_bounding_rect()
        #    self.boundingRect = self.boundingRect.move(self.center.x - Constants.AGENT_WIDTH /2, self.center.y - Constants.AGENT_HEIGHT /2)

        ## Add direction force and boundry force
        #self.getBorderForce()
        #self.direction = self.modifyForce(self.direction, self.weightToUse)
        #self.boundryForces = self.modifyForce(self.boundryForces, Constants.BOUNDRY_WEIGHT)
        #targetDirection = self.direction + self.boundryForces
        #if clock.get_time() != 0:
        #    targetDirection = targetDirection.scale(clock.get_time() / 100)
        #targetDirection = targetDirection.scale(self.speed)

        #self.finalPosition(targetDirection)
        #self.updateCenter()

    def draw(self, screen):
        if(self.surf != None):
            pygame.draw.rect(screen, (0, 0, 0), self.boundingRect, 2)

        # Draw Image
        self.angle = math.atan2(-self.velocity.x, -self.velocity.y)
        self.angle = math.degrees(self.angle)
        self.surf = pygame.transform.rotate(self.image, self.angle)
        upperLeft = Vector((self.center.x - self.surf.get_width() / 2), (self.center.y - self.surf.get_height() /2))
        screen.blit(self.surf, [upperLeft.x, upperLeft.y])

        if Constants.DEBUG_VELOCITY:
        # Draw a line showing the expected velocity Blue
            pygame.draw.line(screen, (0,0,255), self.center.tuple() ,(self.center + self.velocity.scale(20)).tuple(),Constants.DEBUG_LINE_WIDTH )

        # Draw each boundry force line Fuchia
        for force in self.boundryList:
            pygame.draw.line(screen, (255, 0, 255), self.center.tuple(), force.tuple(), 3)
    
    def modifyForce(self, appliedForce, weight):
        # modify force
        appliedForce = appliedForce.normalize()
        appliedForce = appliedForce.scale(weight)
        appliedForce = appliedForce.scale(self.speed)
        return appliedForce

    def getBorderForce(self):
         # Do not let the agent move outside of the world bounds
        self.boundryList = []
        xForce = 0
        yForce = 0
        # Set boundries for left side
        if self.position.x <= Constants.BOUNDRY_RADIUS:
            self.boundryList.append(Vector(self.center.x  - Constants.BOUNDRY_RADIUS, self.center.y))
            xForce = Constants.BOUNDRY_RADIUS - self.position.x
        # Set Boundries for right side
        if self.position.x >= Constants.WORLD_WIDTH - Constants.BOUNDRY_RADIUS:
            self.boundryList.append(Vector(self.center.x + Constants.BOUNDRY_RADIUS, self.center.y))
            xForce = Constants.WORLD_WIDTH - Constants.BOUNDRY_RADIUS - self.position.x
        # Set Boundries for top side
        if self.position.y <= Constants.BOUNDRY_RADIUS: 
            self.boundryList.append(Vector(self.center.x, self.center.y - Constants.BOUNDRY_RADIUS))
            yForce = Constants.BOUNDRY_RADIUS - self.position.y
        # Set Boundries for bottom side
        if self.position.y >= Constants.WORLD_HEIGHT - Constants.BOUNDRY_RADIUS: 
            self.boundryList.append(Vector(self.center.x, self.center.y + Constants.BOUNDRY_RADIUS))
            yForce = Constants.WORLD_HEIGHT - Constants.BOUNDRY_RADIUS - self.position.y

        self.boundryForces = Vector(xForce, yForce)

    def finalPosition(self, targetDirection):
        # Determine rotation
        difference = targetDirection.normalize() - self.direction.normalize()
        #
        if difference.length() < self.turningSpeed:
            self.velocity = targetDirection
        else:
            difference = difference.normalize()
            difference = difference.scale(self.turningSpeed)
            self.direction += difference
            self.velocity = self.direction.normalize()
        
        # Set position and modify as last resort
        self.position += self.velocity
        if self.position.x < 0:
            self.position.x = 0
        if self.position.x > Constants.WORLD_WIDTH:
            self.position.x = Constants.WORLD_WIDTH
        if self.position.y < 0:
            self.position.y = 0
        if self.position.y > Constants.WORLD_HEIGHT:
            self.position.y = Constants.WORLD_HEIGHT