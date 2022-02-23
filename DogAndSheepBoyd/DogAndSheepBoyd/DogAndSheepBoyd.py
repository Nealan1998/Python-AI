
import pygame
import Constants
from pygame.locals import *
import random

# Import Assets
from Vector import Vector
from Player import Player
from Sheep import Sheep

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
hankTheCowdog = Player(Constants.SCREEN_SIZE.scale(1/2), Constants.PLAYER_SIZE, Constants.PLAYER_SPEED, dogImage, Constants.PLAYER_TURN_SPEED)

# Set enemies with random positions
shaunAndFriends = []
for shaun in range(20):
	shaunAndFriends.append(Sheep(Vector(random.randint(0, Constants.WORLD_WIDTH), random.randint(0, Constants.WORLD_HEIGHT)), Constants.ENEMY_SIZE, Constants.ENEMY_SPEED, sheepImage, Constants.SHEEP_TURN_SPEED))

clock = pygame.time.Clock()

def handleDebugging():        
    # Handle the Debugging for Forces
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYUP:

            # Toggle Dog Influence
            if event.key == pygame.K_1:
                Constants.ENABLE_DOG = not Constants.ENABLE_DOG
                print("Toggle Dog Influence", Constants.ENABLE_DOG)

            # Toggle Alignment Influence
            if event.key == pygame.K_2: 
                Constants.ENABLE_ALIGNMENT = not Constants.ENABLE_ALIGNMENT
                print("Toggle Alignment Influence", Constants.ENABLE_ALIGNMENT)

            # Toggle Separation Influence
            if event.key == pygame.K_3: 
                Constants.ENABLE_SEPARATION = not Constants.ENABLE_SEPARATION
                print("Toggle Separation Influence", Constants.ENABLE_SEPARATION)

            # Toggle Cohesion Influence
            if event.key == pygame.K_4: 
                Constants.ENABLE_COHESION = not Constants.ENABLE_COHESION
                print("Toggle Cohesion Influence", Constants.ENABLE_COHESION)

            # Toggle Boundary Influence
            if event.key == pygame.K_5: 
                Constants.ENABLE_BOUNDARIES = not Constants.ENABLE_BOUNDARIES
                print("Toggle Boundary Influence", Constants.ENABLE_BOUNDARIES)

            # Toggle Dog Influence Lines
            if event.key == pygame.K_6: 
                Constants.DEBUG_DOG_INFLUENCE = not Constants.DEBUG_DOG_INFLUENCE
                print("Toggle Dog Influence Lines", Constants.DEBUG_DOG_INFLUENCE)
    
            # Toggle Velocity Lines
            if event.key == pygame.K_7: 
                Constants.DEBUG_VELOCITY = not Constants.DEBUG_VELOCITY
                print("Toggle Velocity Lines", Constants.DEBUG_VELOCITY)

            # Toggle Neighbor Lines
            if event.key == pygame.K_8: 
                Constants.DEBUG_NEIGHBORS = not Constants.DEBUG_NEIGHBORS
                print("Toggle Neighbor Lines", Constants.DEBUG_NEIGHBORS)

            # Toggle Boundary Force Lines
            if event.key == pygame.K_9: 
                Constants.DEBUG_BOUNDARIES = not Constants.DEBUG_BOUNDARIES
                print("Toggle Boundary Force Lines", Constants.DEBUG_BOUNDARIES)

            # Toggle Bounding Box Lines
            if event.key == pygame.K_0: 
                Constants.DEBUG_BOUNDING_RECTS = not Constants.DEBUG_BOUNDING_RECTS
                print("Toggle Bounding Box Lines", Constants.DEBUG_BOUNDING_RECTS)

while hasQuit == False:
	handleDebugging();
    
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
		shaun.update(screen, hankTheCowdog, clock, shaunAndFriends)
		shaun.draw(screen)
	
	## Flip buffers and keep game at 60 frames a second
	pygame.display.flip()
	clock.tick(Constants.FRAME_RATE)
