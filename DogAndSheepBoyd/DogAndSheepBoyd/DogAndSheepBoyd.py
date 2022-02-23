
import pygame
import Constants
from pygame.locals import *
import random

# Import Assets
from Vector import Vector
from Player import Player
from Enemy import Enemy

# Import images
dogImage = pygame.image.load('dog.png')
sheepImage = pygame.image.load('sheep.png')

## Initialize and set window
pygame.init()
screen = pygame.display.set_mode((Constants.WORLD_WIDTH, Constants.WORLD_HEIGHT))
hasQuit = False
x = 100
y = 100

# Set the player with a position
hankTheCowdog = Player(Constants.SCREEN_SIZE.scale(1/2), Constants.PLAYER_SIZE, Constants.PLAYER_SPEED, dogImage)

# Set enemies with random positions
shaunAndFriends = []
for shaun in range(5):
	shaunAndFriends.append(Enemy(Vector(random.randint(0, Constants.WORLD_WIDTH), random.randint(0, Constants.WORLD_HEIGHT)), Constants.ENEMY_SIZE, Constants.ENEMY_SPEED, sheepImage))

clock = pygame.time.Clock()

while hasQuit == False:
	## Searches for events
	for event in pygame.event.get():
		## If quit event takes place, quit game
		if event.type == QUIT:
			hasQuit = True
	
	## Update cornflower screen and regularly update the player's position and design
	screen.fill(Constants.BACKGROUND_COLOR)
	hankTheCowdog.update(screen, shaunAndFriends, clock)
	hankTheCowdog.draw(screen)
	
	## Update all enemies in list
	for shaun in shaunAndFriends:
		shaun.update(screen, hankTheCowdog, clock)
		shaun.draw(screen)
	
	## Flip buffers and keep game at 60 frames a second
	pygame.display.flip()
	clock.tick(Constants.FRAME_RATE)
