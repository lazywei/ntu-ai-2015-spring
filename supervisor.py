import numpy as np
import random

from state import State
from state import Car

from AI import AI
# import Drawer

class Supervisor:
    # _map includes
    #    method for moving a car( e.g., map.moveCar(car, from, to) )
    # _cars includes the cars and it type, priority and speed
    def __init__(self, _numberOfCars):
        self.numberOfCars = _numberOfCars

        self.state = State()
        self.state.generateCars(5)
        self.map = self.state.getMap()
        self.cars = self.state.getCars()
        

        # AI
        self.ai = AI()

        # Initializing the remain moves of cars
        self.carMovesRemain = []
        for carID in range(numberOfCars):
            self.carMovesRemain.append(self.cars[carID].speed)
            

        # carList : a 'list' of 'car'
        # car :
        #    car.type : 'vehicle', 'taxi', 'ambulance'
        #    car.location : (x,y)
        #    car.start : (x,y)
        #    car.destination : (x,y)
        #    car.priority : 'high', 'medium', 'low'
        #    car.speed : 1, 2, 3
        #
        #    car.getNextLocation(gameState) : return next location of the car

    def start(self):
        
        # for car in cars:
        #     nextAction = AI.nextStep(car.id, state)
        #     state = state.getStateByAction(car.id, nextAction)
        #     Drawer.draw(state)
        

        # Start
        currCarIdx = 0
        nextAction = AI.nextStep(currCarIdx, state)
        state = state.getStateByAction(currCarIdx, nextAction)
        Drawer.draw(state)

        while(not state.isGoal()):
            nextCarIdx = self.getNextCarIdx(currCarIdx)
            nextAction = AI.nextStep(currCarIdx, state)
            state = state.getStateByAction(currCarIdx, nextAction)
            Drawer.draw(state)


    def isGoal(self):
        for carID in range(self.numberOfCars):
            if(self.state.isGoalState(carID)):
                return True
        return False

    def getNextCarIdx(self, currCarIdx):
        if(self.carMovesRemain[currCarIdx] > 0):
            nextCarIdx = currCarIdx
            self.carMovesRemain[nextCarIdx] = (self.carMovesRemain[nextCarIdx]
                                               - 1)
            return nextCarIdx
        else:
            self.carMovesRemain[currCarIdx] = self.carList[currCarIdx].speed
            nextCarIdx = (currCarIdx + 1) % len(self.carList)
            self.carMovesRemain[nextCarIdx] = (self.carMovesRemain[nextCarIdx]
                                               - 1)
            return nextCarIdx

    def getNextCarWithPriority():
        pass


    def showCarsInfo(self):
        if(len(self.cars) > 0):
            for car in self.cars:
                print '---------------'
                print 'ID: ', car.id_
                print 'type: ', car.type_
                print 'location: ', car.location
                print 'start: ', car.start
                print 'destination: ', car.destination
                print 'priority: ', car.priority
                print 'speed: ', car.speed
        else:
            print 'In showCarsInfo(): There is no any car!'

    

    #################################################################
    # Deprecated                                                    #
    #################################################################

    # def printMap(self):
    #     # map = self.map
    #     for row in self.map:
    #         for c in row:
    #             if c == -1:
    #                 print "  ",
    #             elif c == -2:
    #                 print "XX",
    #             else:
    #                 print '%2d'%c,
    #         print '\n',


    # def generateCars(self, numberOfCars):
    #     if(numberOfCars > 0):
    #         for carID in range(numberOfCars):
    #             while True:
    #                 sx = random.choice(np.arange(self.mapMaxX))
    #                 sy = random.choice(np.arange(self.mapMaxY))

    #                 dx = random.choice(np.arange(self.mapMaxX))
    #                 dy = random.choice(np.arange(self.mapMaxY))
    #                 if self.map[sx][sy]== -1:
    #                     break

    #             newCar = Car(carID, 'vehicle', (sx,sy), (sx,sy), (dx,dy), 0, 1)
    #             self.cars.append(newCar)
    #             self.map[sx][sy] = carID
    #     else:
    #         print
    #         'In generateCars(): Wrong argument: numberOfCars <-', numberOfCars



if __name__ == '__main__':
    numberOfCars = 5
    mSupervisor = Supervisor(numberOfCars)
    mState = mSupervisor.state
    mState.printMap()
    
    
    mAI = mSupervisor.ai

    counter = 0
    while not mSupervisor.isGoal() or counter < 100:
        nextAction = mAI.getNextAction(0, mState)
        if nextAction == []:
            print 'Empty array'
        mState = mState.getStateByAction(0, nextAction)
        counter = counter + 1

    mState.printMap()
    











