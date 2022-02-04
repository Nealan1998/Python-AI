import pygame
from Vector import Vector

class Player:

	def __init__(self, position, velocity, size):
		# Set defaults for this specific player
		self.position = position
		self.velocity = velocity
		self.size = size
		self.center = position + Vector(1,1).scale(size / 2)

	def draw(self, screen):
		# Draw a square at the new position
		pygame.draw.rect(screen, (247,108,155), 
				   pygame.Rect(self.position.x, self.position.y, self.size, self.size))
		
		# Drawl a line showing the expected velocity
		pygame.draw.line(screen, (59,28,255), self.center.tuple() ,(self.center + self.velocity.scale(50)).tuple(),3 )

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
		self.center = self.position + Vector(1,1).scale(self.size / 2)
