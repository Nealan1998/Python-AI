import pygame
import Constants
import random
from Vector import Vector
from Agent import Agent

class Player(Agent):

	def __init__(self, position, speed, size, color):
		super().__init__(position, speed, size, color)
		self.chasing = False
		self.currentEnemy = -1 #None
		self.currentEnemyNumber = -1
		self.boolTest = False


	def update(self, enemies):
		# Seek a New Enemy
		if self.chasing != True and len(enemies) > 0:
			self.SeekNew(enemies)
		
		# Check if the player is chasing
		if self.chasing == True:
			# Seek the enemy
			direction = enemies[self.currentEnemy].position - self.position
			self.velocity = direction.normalize()
			super().update()
			# Check for collisions and determine line color
			self.boolTest = super().CheckForCollision(enemies[self.currentEnemy])
			

		#If colliding with enemy, tag them
		if self.boolTest == True and self.chasing == True:
			del(enemies[self.currentEnemy])
			self.chasing = False

	def SeekNew(self, enemies):
		#Find out how many enemies there are
		numberInList = len(enemies)
		# If there are enemies in the lest, choose the enemy randomly
		if (numberInList != 0):
			self.currentEnemy = random.randrange(numberInList)
			self.target = enemies[self.currentEnemy]
			enemies[self.currentEnemy].target = self
			self.chasing = True
		# If there are no enemies, stop chasing
		else:
			self.currentEnemy = -1
			self.chasing = False
