import pygame
import Constants
from pygame.locals import *

# Import Assets
from Vector import Vector
from Player import Player
from Enemy import Enemy

## Initialize and set window
pygame.init()
screen = pygame.display.set_mode((Constants.WORLD_WIDTH, Constants.WORLD_HEIGHT))
x = 100
y = 100

# Set the player with a position
Player = Player(Constants.SCREEN_SIZE.scale(1/2), Constants.PLAYER_SPEED, Constants.PLAYER_SIZE, Constants.PLAYER_COLOR)

# Set player
Enemy = Enemy(Vector(100, 100), Constants.ENEMY_SIZE, Constants.ENEMY_SPEED)
# Set clock to use constant frames per second
clock = pygame.time.Clock()

while True:
	## Searches for events
	for event in pygame.event.get():
		## If quit event takes place, quit game
		if event.type == QUIT:
			pygame.quit()
			quit()
	
	## Update cornflower screen and regularly update the player's position and design
	screen.fill(Constants.BACKGROUND_COLOR)
	Player.update()
	Player.draw(screen)
	Enemy.update()
	Enemy.draw(screen)
	#print(Player)

	## Flip screen and keep game at 60 frames a second
	pygame.display.flip()
	clock.tick(Constants.FRAME_RATE)