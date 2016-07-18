from graphics import *
from time import sleep
from math import *

class World(object):
	# This class creates the world object, which holds the mass objects. 
	# The world object does all of the mathematical computation, such as 
	# determing the resultant gravitational forces as well as the velocity
	# vectors for each mass object. It also determines if two masses are 
	# close enough to merge into a bigger mass that is the sum of its two
	# constituent masses. It also accounts for momentum conservation. 

	# The world is run by using a time scale determined by the timeStep, which
	# the user decides. The user can also change the default mass and velocity
	# for each of the mass objects by clicking on the settings button.

	def __init__(self, name, width, height, numMass = 0, timeStep = 0.1):
		self.name = name
		self.width = width
		self.height = height
		self.numMass = numMass
		self.timeStep = timeStep

		self.massList = []
		self.window = None
		self.button = None
		self.settings = None

	def addMass(self, mass):
		# Adds a mass object to the world

		self.numMass = self.numMass + 1
		self.massList.append(mass)

	def removeMass(self, mass):
		# Removes a mass object from the world

		self.numMass = self.numMass - 1
		mass.body.undraw()
		self.massList.remove(mass)

	def showWorld(self):
		# Creates and displays the world

		self.window = GraphWin(self.name, self.width, self.height)

	def displaySettingsButton(self):
		# Displays the setting button which the user can click to change default mass and velocity

		point1 = Point(self.width - 100 - 10, 10)
		point2 = Point(self.width - 10, 10 + 30)

		self.button = Rectangle(point1, point2)
		self.button.draw(self.window)

		anchorPoint = Point((point1.x + point2.x)/2, (point1.y + point2.y)/2)

		self.settings = Text(anchorPoint, "Settings")
		self.settings.draw(self.window)

	def getSettingsCoordinateRanges(self):
		# Returns the coordinates of settings button

		x1 = self.button.getP1().getX()
		y1 = self.button.getP1().getY()
		x2 = self.button.getP2().getX()
		y2 = self.button.getP2().getY()

		return x1, x2, y1, y2

	def checkMouse(self):
		# Returns the point that was clicked on by user

		return self.window.checkMouse()

	def getWindow(self):
		# Returns window object 

		return self.window

	def pythagorean(self, point1, point2):
		# Computes distance between two points

		return sqrt((point1.x-point2.x)**2 + (point1.y-point2.y)**2)

	def gravitationalForce(self, mass1, mass2):
		# Returns the force vector between two masses in ordered set notation
		# Be careful. The "direction" variable gives the angle of the vector 
		# drawn starting at mass1 and ending at mass2 with respect to the horizontal axis
		point1 = Point(mass1.x*1.0, mass1.y*1.0)
		point2 = Point(mass2.x*1.0, mass2.y*1.0)

		magnitude = 0

		# Error checking in case user creates two masses at exact same point to avoid
		# infinite force
		if (abs(point1.x - point2.x) < 0.01):
			if (abs(point1.y - point2.y) < 0.01):
				magnitude = 0
		else:
			magnitude = (mass1.mass*mass2.mass)/(self.pythagorean(point1, point2))**2

		# Computing the angle of the vector with respect to the horizontal axis
		delta_x = mass2.x - mass1.x
		delta_y = mass2.y - mass1.y
		direction = atan2(delta_y, delta_x)

		return [magnitude*cos(direction), magnitude*sin(direction)]

	def vectorAddition(self, vector1, vector2):
		# Adds two vectors together
 
		return [vector1[0]+vector2[0], vector1[1]+vector2[1]]

	def computeForces(self):
		# This method computes the total force by each mass object in the world's massList

		totalForce = [0, 0]

		# If there are 0 or 1 mass object, then no force should be felt.
		if len(self.massList) < 2:
			for mass in self.massList:
				mass.force = [0, 0]
		# Else, the forces must be calculated. 
		else:
			for i in range(len(self.massList)):
				# Finds the force between mass i and every other mass and uses vector addition to find resultant force
				for j in range(len(self.massList)):
					if (i is j):
						continue
					else:
						totalForce = self.vectorAddition(totalForce, self.gravitationalForce(self.massList[i], self.massList[j]))
				self.massList[i].force = totalForce
				totalForce = [0, 0]

	def updateVelocity(self):
		# This method updates the velocity vector of each mass object by taking
		# account the acceleration from the total force

		for mass in self.massList:
			mass.vx = mass.vx + self.timeStep*mass.force[0]/mass.mass
			mass.vy = mass.vy + self.timeStep*mass.force[1]/mass.mass

	def translateMass(self):
		# This method tells each mass object how much to translate

		for mass in self.massList:
			mass.translate(mass.vx*self.timeStep, mass.vy*self.timeStep)

	def mergeCheck(self):
		# Checks if any two masses need to merge

		for mass1 in self.massList:

			# If mass is -1, that means that it must be removed from the world.
			if (mass1.mass is -1):
				continue 

			for mass2 in self.massList:
				if (mass1 is mass2):
					continue

				if (mass2.mass is -1):
					continue

				distance = self.pythagorean(Point(mass1.x, mass1.y), Point(mass2.x, mass2.y))

				# If the center of one mass enters the body of the other, then the two masses will merge
				if (distance < mass1.radius) or (distance < mass2.radius):

					# The location of the bigger mass will be the location of the merged mass
					if (mass1.mass > mass2.mass):
						self.merge(mass2, mass1)
					else:
						self.merge(mass1, mass2)

		# Removes all mass that have mass of -1
		for mass in self.massList:
			if (mass.mass is -1):
				self.removeMass(mass)

	def merge(self, toRemove, toReplace):
		# This method merges two masses together

		# The "center" variable is the location of the bigger mass
		center = Point(toReplace.x, toReplace.y)

		# The velocity of the merged mass is determined from momentum conservation
		vx, vy = self.momentumConservation(toRemove, toReplace)

		mass = Mass(self.window, toRemove.mass+toReplace.mass, center, vx, vy)

		# The merged mass is placed in the world massList using the index of the 
		# bigger constituent mass. This is to preserve the integrity of the 
		# nested for loop in mergeCheck. 
		self.massList.insert(self.massList.index(toReplace), mass)
		self.numMass = self.numMass + 1
		self.removeMass(toReplace)

		# Mass that must be removed is marked as -1 so as not to ruin the inner for loop
		# If a mass is removed prematurely, then an index error will occur. So, the mass
		# is removed after the loop is finished. 
		toRemove.mass = -1


	def momentumConservation(self, mass1, mass2):
		# Computes the velocity of the merged mass
		vx = (mass1.mass*mass1.vx + mass2.mass*mass2.vx)/(mass1.mass+mass2.mass)
		vy = (mass1.mass*mass1.vy + mass2.mass*mass2.vy)/(mass1.mass+mass2.mass)
		return vx, vy


class Mass(object):
	# This class creates the mass object, which has position, velocity, and acceleration (according 
	# to the force vector). It is told how much to translate by the world class. 

	def __init__(self, world, mass, point, vx = 0, vy = 0):
		self.world = world
		self.mass = mass
		self.radius = 2*sqrt(mass)
		self.point = point
		self.body = Circle(self.point, self.radius)
		self.x = self.point.x
		self.y = self.point.y
		self.body.draw(self.world)
		self.vx = vx
		self.vy = vy
		self.force = [0, 0]

	def translate(self, dx, dy):
		self.x = self.x + dx
		self.y = self.y + dy
		self.body.move(dx, dy)