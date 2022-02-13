
import pygame
import Constants
from pygame.locals import *
import random

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

# Set enemies with random positions
Enemies= []
for enemy in range(10):
	Enemies.append(Enemy(Vector(random.randint(0, Constants.WORLD_WIDTH), random.randint(0, Constants.WORLD_HEIGHT)), Constants.ENEMY_SIZE, Constants.ENEMY_SPEED, Constants.ENEMY_COLOR))

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
	Player.update(Enemies)
	Player.draw(screen)
	
	## Update all enemies in list
	for enemy in Enemies:
		enemy.update(Player)
		enemy.draw(screen)
	
	## Flip screen and keep game at 60 frames a second
	pygame.display.flip()
	clock.tick(Constants.FRAME_RATE)