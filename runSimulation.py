from gravitySimulator import *
from time import sleep

def test():
	newWorld = World("hi", 2000, 2000)
	newWorld.showWorld()

	# while (True):
	# 	point = newWorld.checkMouse()
	# 	if (point is not None):
	#  		mass = Mass(newWorld.getWindow(), 1000, point)
	#  		newWorld.addMass(mass)


	mass1 = Mass(newWorld.getWindow(), 400, Point(0, 0))
	mass2 = Mass(newWorld.getWindow(), 300, Point(-7, 1))
	mass3 = Mass(newWorld.getWindow(), 200, Point(6, -3))
	mass4 = Mass(newWorld.getWindow(), 100, Point(9, 14))
	#print 400*300/(newWorld.pythagorean(Point(0,0), Point(2, 5)))**2
	#print newWorld.gravitationalForce(mass1, mass2)
	newWorld.addMass(mass1)
	newWorld.addMass(mass2)
	#newWorld.addMass(mass3)
	#newWorld.addMass(mass4)

	newWorld.computeForces()

def testMomentumConservation():
	newWorld = World("hi", 1000, 1000)
	newWorld.showWorld()

	mass1 = Mass(newWorld.getWindow(), 800, Point(200, 300), 9, 0)
	mass2 = Mass(newWorld.getWindow(), 300, Point(600, 300), -2, 0)

	newWorld.addMass(mass1)
	newWorld.addMass(mass2)

	while (True):
		sleep(0.01)
		newWorld.computeForces()
		newWorld.updateVelocity()
		newWorld.translateMass()
		newWorld.mergeCheck()



def main():
	#test()
	#testMomentumConservation()
	newWorld = World("Hello!", 1000, 1000)
	newWorld.showWorld()
	newWorld.displaySettingsButton()

	massInput = 100
	vxInput = 0
	vyInput = 0
	timeStep = 0.001

	while (True):

		sleep(timeStep)
		point = newWorld.checkMouse()
		if (point is not None):
			x1, x2, y1, y2 = newWorld.getSettingsCoordinateRanges()
			if point.x < x2 and point.x > x1:
				if point.y < y2 and point.y > y1:
					massInput = input("What mass would you like? Please enter an integer: ")
					vxInput = input("What should the velocity in the horizontal direction be? Please enter an integer: ")
					vyInput = input("What should the velocity in the vertical direction be? Please enter an integer: ")
					print "Okay!"
					continue
			mass = Mass(newWorld.getWindow(), massInput, point, vxInput, vyInput)
			newWorld.addMass(mass)
		newWorld.computeForces()
		newWorld.updateVelocity()
		newWorld.translateMass()
		newWorld.mergeCheck()


main()


