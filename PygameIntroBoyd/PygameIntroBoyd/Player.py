import pygame
import Constants
from Vector import Vector

class Player:

	def __init__(self, position, speed, size, color):
		# Set defaults for this specific player
		self.position = position
		self.speed = speed
		self.velocity = Vector(0,0)
		self.size = size
		self.color = color
		self.center = self.getCenter()

	def __str__(self):
		return (f"Player Size: {str(self.size)}	Position: {str(self.position)}	Velocity: {str(self.velocity)}	Center: {str(self.center)}")

	def draw(self, screen):
		# Draw a square at the new position
		pygame.draw.rect(screen, self.color, 
				   pygame.Rect(self.position.x, self.position.y, self.size, self.size))
		
		# Drawl a line showing the expected velocity
		pygame.draw.line(screen, (0,0,255), self.center.tuple() ,(self.center + self.velocity.scale(5)).tuple(),3 )

	def update(self):
		# Get key input from user
		direction = Vector(0,0)
		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_a]: direction.x -= 1
		if pressed[pygame.K_d]: direction.x += 1
		if pressed[pygame.K_s]: direction.y += 1
		if pressed[pygame.K_w]: direction.y -= 1

		# Update information
		self.velocity = direction.normalize()
		self.position += self.velocity.scale(7)
		self.center = self.getCenter()#self.position + Vector(1,1).scale(self.size / 2)

	def getCenter(self):
		# Find the cetner of the object
		center = self.position + Vector(1,1).scale((self.size / 2))
		return center
