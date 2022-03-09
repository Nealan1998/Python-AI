import Constants
import Node
import pygame
import Vector

from pygame import *
from Vector import *
from Node import *
from enum import Enum

class SearchType(Enum):
	BREADTH = 0
	DJIKSTRA = 1
	A_STAR = 2
	BEST_FIRST = 3

class Graph():
	def __init__(self):
		""" Initialize the Graph """
		self.nodes = []			# Set of nodes
		self.obstacles = []		# Set of obstacles - used for collision detection

		# Initialize the size of the graph based on the world size
		self.gridWidth = int(Constants.WORLD_WIDTH / Constants.GRID_SIZE)
		self.gridHeight = int(Constants.WORLD_HEIGHT / Constants.GRID_SIZE)

		# Create grid of nodes
		for i in range(self.gridHeight):
			row = []
			for j in range(self.gridWidth):
				node = Node(i, j, Vector(Constants.GRID_SIZE * j, Constants.GRID_SIZE * i), Vector(Constants.GRID_SIZE, Constants.GRID_SIZE))
				row.append(node)
			self.nodes.append(row)

		## Connect to Neighbors
		for i in range(self.gridHeight):
			for j in range(self.gridWidth):
				# Add the top row of neighbors
				if i - 1 >= 0:
					# Add the upper left
					if j - 1 >= 0:		
						self.nodes[i][j].neighbors += [self.nodes[i - 1][j - 1]]
					# Add the upper center
					self.nodes[i][j].neighbors += [self.nodes[i - 1][j]]
					# Add the upper right
					if j + 1 < self.gridWidth:
						self.nodes[i][j].neighbors += [self.nodes[i - 1][j + 1]]

				# Add the center row of neighbors
				# Add the left center
				if j - 1 >= 0:
					self.nodes[i][j].neighbors += [self.nodes[i][j - 1]]
				# Add the right center
				if j + 1 < self.gridWidth:
					self.nodes[i][j].neighbors += [self.nodes[i][j + 1]]
				
				# Add the bottom row of neighbors
				if i + 1 < self.gridHeight:
					# Add the lower left
					if j - 1 >= 0:
						self.nodes[i][j].neighbors += [self.nodes[i + 1][j - 1]]
					# Add the lower center
					self.nodes[i][j].neighbors += [self.nodes[i + 1][j]]
					# Add the lower right
					if j + 1 < self.gridWidth:
						self.nodes[i][j].neighbors += [self.nodes[i + 1][j + 1]]

	def getNodeFromPoint(self, point):
		""" Get the node in the graph that corresponds to a point in the world """
		point.x = max(0, min(point.x, Constants.WORLD_WIDTH - 1))
		point.y = max(0, min(point.y, Constants.WORLD_HEIGHT - 1))

		# Return the node that corresponds to this point
		return self.nodes[int(point.y/Constants.GRID_SIZE)][int(point.x/Constants.GRID_SIZE)]

	def placeObstacle(self, point, color):
		""" Place an obstacle on the graph """
		node = self.getNodeFromPoint(point)

		# If the node is not already an obstacle, make it one
		if node.isWalkable:
			# Indicate that this node cannot be traversed
			node.isWalkable = False		

			# Set a specific color for this obstacle
			node.color = color
			for neighbor in node.neighbors:
				neighbor.neighbors.remove(node)
			node.neighbors = []
			self.obstacles += [node]

	def reset(self):
		""" Reset all the nodes for another search """
		for i in range(self.gridHeight):
			for j in range(self.gridWidth):
				self.nodes[i][j].reset()

	def buildPath(self, endNode):
		""" Go backwards through the graph reconstructing the path """
		path = []
		node = endNode
		while node is not 0:
			node.isPath = True
			path = [node] + path
			node = node.backNode

		# If there are nodes in the path, reset the colors of start/end
		if len(path) > 0:
			path[0].isPath = False
			path[0].isStart = True
			path[-1].isPath = False
			path[-1].isEnd = True
		return path

	def findPath_Breadth(self, start, end):
		""" Breadth Search """
		#print("Breadth")
		self.reset()

		return []

	def findPath_Djikstra(self, start, end):
		""" Djikstra's Search """
		#print("DJIKSTRA")
		self.reset()

		return []

	def findPath_AStar(self, start, end):
		""" A Star Search """
		#print("A_STAR")
		self.reset()

		return []

	def findPath_BestFirst(self, start, end):
		""" Best First Search """
		#print("BEST_FIRST")
		self.reset()
		
		# Set up everything
		startNode = self.getNodeFromPoint(start)
		endNode = self.getNodeFromPoint(end)
		curNode = startNode
		startNode.isVisited = True
		pqueue = [startNode]

		startNode.costFromStart = 0
		startNode.costToEnd = 0
		startNode.cost = 0


		while len(pqueue) != 0:
			# pop the currNode off
			curNode = pqueue.pop(0)
			curNode.isExplored = True
			# Check if node is endNode
			if curNode == endNode:
				return self.buildPath(curNode)
			# Check each neighbor
			for nextNode in curNode.neighbors:
				curDistance = (curNode.center - nextNode.center).length()
				# handle unvisited node
				if nextNode.isVisited == False:
					# Check cost from start
					nextNode.isVisited = True

					# Calculate Djikstra
					nextNode.costFromStart = curDistance + curNode.costFromStart
					nextNode.costToEnd = 0
					dCost = nextNode.costFromStart + nextNode.costToEnd

					# Calculate Best and add to Djikstra
					bCost = (nextNode.center - endNode.center).length()
					nextNode.cost = dCost + bCost
					nextNode.backNode = curNode
					pqueue.append(nextNode)
				# Handle visited node
				else:
					# Compare costs from start
					# Calculate Djikstra
					newCostFromStart = curNode.costFromStart + curDistance
					newCostToEnd = 0
					newDCost = newCostFromStart + newCostToEnd

					# Calculate Best and add to Djikstra
					newBCost = (nextNode.center + endNode.center).length()
					newCost = newDCost + newBCost
					if (newCost < nextNode.cost):
						nextNode.costFromStart = newCostFromStart
						nextNode.costToEnd = newCostToEnd
						nextNode.cost = newCost
						nextNode.backNode = curNode
			pqueue.sort(key=lambda x:x.cost)
		return []

	def draw(self, screen):
		""" Draw the graph """
		for i in range(self.gridHeight):
			for j in range(self.gridWidth):
				self.nodes[i][j].draw(screen)