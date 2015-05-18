class Supervisor:
	# _map includes
	#	method for moving a car( e.g., map.moveCar(car, from, to) )
	# _cars includes the cars and it type, priority and speed
	def __init__(self, gameState):
		self.gameState = gameState
		self.map = gameState.map
		self.carList = gameState.carList
		# carList : a 'list' of 'car'
		# car :
		# 	car.type : 'vehicle', 'taxi', 'ambulance'
		#	car.location : (x,y)
		#	car.start : (x,y)
		#	car.destination : (x,y)
		# 	car.priority : 'high', 'medium', 'low'
		# 	car.speed : 1, 2, 3
		#
		#	car.getNextLocation(gameState) : return next location of the car


	def start(self):
		# Initialization
		self.carMovesRemain = []
		for car in self.carList:
			self.carMovesRemain.append(car.speed)
		
		# Start
		currCarIdx = 0
		self.carList[currCarIdx].move()
		while( not self.isGoal() ):
			nextCarIdx = self.getNextCarIdx(currCarIdx)
			self.carList[nextCarIdx].move()


	def isGoal(self):
		for car in self.carList:
			if( car.location == car.destination ):
				return True
		return False


	def getNextCarIdx(self, currCarIdx):
		if( self.carMovesRemain[currCarIdx] > 0 ):
			nextCarIdx = currCarIdx
			self.carMovesRemain[nextCarIdx] = self.carMovesRemain[nextCarIdx] - 1
			return nextCarIdx
		else:
			self.carMovesRemain[currCarIdx] = self.carList[currCarIdx].speed
			nextCarIdx = (currCarIdx + 1) % len(self.carList)
			self.carMovesRemain[nextCarIdx] = self.carMovesRemain[nextCarIdx] - 1
			return nextCarIdx


	def getNextCarWithPriority():
		pass



if __name__ == '__main__':
	
	pass


