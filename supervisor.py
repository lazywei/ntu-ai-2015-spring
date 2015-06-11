import numpy as np
import random
import copy
import sys
from state import State
from state import Car

from interactive import RedisQueue
from AI import AI
import os
import time


# import Drawer

class Supervisor:
    # _map includes
    #    method for moving a car( e.g., map.moveCar(car, from, to) )
    # _cars includes the cars and it type, priority and speed
    def __init__(self, _numberOfCars,_mapWidth,_mapHeight):
        self.numberOfCars = _numberOfCars

        self.state = State(_mapWidth, _mapHeight)
        self.state.generateCars(_numberOfCars)
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
        '''
        while(not state.isGoal()):
            nextCarIdx = self.getNextCarIdx(currCarIdx)
            nextAction = AI.nextStep(currCarIdx, state)
            state = state.getStateByAction(currCarIdx, nextAction)
            Drawer.draw(state)
        '''
    def calculateArrivedRatio(self):
        goal_counter = 0
        for carID in range(self.numberOfCars):
            print self.state.getCarById(carID).location
            print self.state.getCarById(carID).destination
            if (self.state.getCarById(carID).location == self.state.getCarById(carID).destination):
                print self.state.getCarById(carID).location
                print self.state.getCarById(carID).destination
                goal_counter+=1
            
        print 'Arrived Ratio : ',goal_counter,'/',self.numberOfCars

    def isGoal(self):
        goal_counter = 0
        for carID in range(self.numberOfCars):
            if (self.state.getCarById(carID).location == self.state.getCarById(carID).destination):
                #print self.getCarById(carId).location,' vs ',self.getCarById(carId).destination
                goal_counter+=1
                
        
        if  goal_counter == self.numberOfCars:
            return True
        else:
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
    mSupervisor = Supervisor(numberOfCars,20,20)
    mState = mSupervisor.state
    mAI = mSupervisor.ai
    counter = 0
    maxTurns = numberOfCars*100

    mapsForDrawer = []

    r = RedisQueue('key')
    r.flushall()

    mSupervisor.calculateArrivedRatio()
    while ((not mSupervisor.isGoal()) and (counter < maxTurns)):
        for car_i in range(numberOfCars):
            # Progress bar
            sys.stdout.write('\r')
            i = int(round((20*(0.01+counter))/maxTurns))
            sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
            sys.stdout.flush()
            
            nextAction = mAI.getNextAction(car_i, mState)
            mState = mState.getStateByAction(car_i, nextAction)
            
            counter = counter + 1


        mapsForDrawer.append(copy.deepcopy(mState.getMap().astype(int)))
        r.put(mapsForDrawer)
        mapsForDrawer = []
    print '\n'
    mSupervisor.calculateArrivedRatio()
    
