import math

class Vector:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		# Override string data
		return('Vector (' + str(self.x) + ', ' + str(self.y) + ')')

	def __add__(self, anotherOne):
		# Override addition
		return Vector(self.x + anotherOne.x, self.y + anotherOne.y)

	def __sub__(self, anotherOne):
		# Override subtraction
		return Vector(self.x - anotherOne.x, self.y - anotherOne.y)

	def dot(self, anotherOne):
		# Determine using dot product
		return ((self.x * anotherOne.x) + (self.y * anotherOne.y))

	def scale(self, multiply):
		# Scale length of vector
		return Vector(self.x * multiply, self.y * multiply)

	def length(self):
		# Return length
		return (math.sqrt((self.x ** 2) + (self.y ** 2)))

	def normalize(self):
		# Normalize the vector
		l = self.length()
		if l == 0:
			return Vector(0,0)
		else:
			return Vector(self.x /l, self.y / l)

	def tuple(self):
		# Return tuple version
		return ((self.x, self.y))
