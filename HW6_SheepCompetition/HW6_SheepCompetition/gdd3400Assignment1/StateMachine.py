from Constants import *
from pygame import *
from random import *
from Vector import *
from Agent import *
from Sheep import *
from Dog import *
from Graph import *
from Node import *
from GameState import *

class StateMachine:
	""" Machine that manages the set of states and their transitions """

	def __init__(self, startState):
		""" Initialize the state machine and its start state"""
		self.__currentState = startState
		self.__currentState.enter()

	def getCurrentState(self):
		""" Get the current state """
		return self.__currentState

	def update(self, gameState):
		""" Run the update on the current state and determine if we should transition """
		nextState = self.__currentState.update(gameState)

		# If the nextState that is returned by current state's update is not the same
		# state, then transition to that new state
		if nextState != None and type(nextState) != type(self.__currentState):
			self.transitionTo(nextState)

	def transitionTo(self, nextState):
		""" Transition to the next state """
		self.__currentState.exit()
		self.__currentState = nextState
		self.__currentState.enter()

	def draw(self, screen):
		""" Draw any debugging information associated with the states """
		self.__currentState.draw(screen)

class State:
	def enter(self):
		""" Enter this state, perform any setup required """
		print("Entering " + self.__class__.__name__)
		
	def exit(self):
		""" Exit this state, perform any shutdown or cleanup required """
		print("Exiting " + self.__class__.__name__)

	def update(self, gameState):
		""" Update this state, before leaving update, return the next state """
		print("Updating " + self.__class__.__name__)

	def draw(self, screen):
		""" Draw any debugging info required by this state """
		pass

			   
class FindSheepState(State):
	""" This is an example state that simply picks the first sheep to target """

	def update(self, gameState):
		""" Update this state using the current gameState """
		super().update(gameState)
		dog = gameState.getDog()

		# Pick a random sheep
		dog.setTargetSheep(gameState.getHerd()[0] )

		# You could add some logic here to pick which state to go to next
		# depending on the gameState
		newCenter = dog.getTargetSheep().center
		newCenter = newCenter + dog.additionVector
		dog.calculatePathToNewTarget(newCenter)# + self.additionVector)


		return Idle()

class Idle(State):
	""" This is an idle state where the dog does nothing """

	def update(self, gameState):
		super().update(gameState)
		
		# Do nothing
		if len(gameState.getHerd()) > 0:
			return DetermineDirectionState()
		else:
			return Idle()

class DetermineDirectionState(State):

	def update(self, gameState):
		super().update(gameState)
		dog = gameState.getDog()
		dog.additionVector = Vector(0,0)

		centerToCheck = dog.getTargetSheep().center;

		penMinX = Constants.PEN[0][0][0]
		penMaxX = Constants.PEN[0][1][0]
		penCenter = (penMinX + penMaxX) / 2
		penY = Constants.PEN[0][0][1]
		
		# If sheep is below the gate
		if centerToCheck.y > penY:
			dog.additionVector = Vector(0, Constants.SHEEP_HEIGHT)
		# If sheep is left of gate
		elif centerToCheck.y < penY and centerToCheck.x < penMinX:
			dog.additionVector = Vector(Constants.SHEEP_WIDTH * -1, 0)#Constants.SHEEP_HEIGHT )
		# If sheep is right of gate
		elif centerToCheck.y < penY and centerToCheck.x > penMaxX:
			dog.additionVector = Vector(Constants.SHEEP_WIDTH, 0)# Constants.SHEEP_HEIGHT )
		# If sheep is above gate on left side
		elif centerToCheck.y < penY and centerToCheck.x > penMinX and centerToCheck.x < penCenter:
			dog.additionVector = Vector(Constants.SHEEP_WIDTH * -2, Constants.SHEEP_HEIGHT *-2)
		# If sheep is above gate on right side
		elif centerToCheck.y < penY and centerToCheck.x < penMaxX and centerToCheck.x > penCenter:
			dog.additionVector = Vector(Constants.SHEEP_WIDTH * 2 , Constants.SHEEP_HEIGHT * -2)


		return FindSheepState()