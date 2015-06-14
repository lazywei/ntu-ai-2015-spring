import numpy as np
import random
import copy
import sys

from state import State
from state import Car
from datetime import datetime

from interactive import RedisQueue
from AI import AI
import os
import time
import pickle

# import Drawer

class Supervisor:
    # _map includes
    #    method for moving a car( e.g., map.moveCar(car, from, to) )
    # _cars includes the cars and it type, priority and speed
    def __init__(self, _numberOfCars,_mapWidth,_mapHeight,_AIName):
        self.numberOfCars = _numberOfCars

        self.state = State(_mapWidth, _mapHeight)
        self.state.generateCars(_numberOfCars)
        self.map = self.state.getMap()
        self.cars = self.state.getCars()


        # AI
        self.ai = AI(_numberOfCars,_AIName)

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
    def setAI(self,_AIName):
        self.ai = AI(self.numberOfCars,_AIName)
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

    def printArrivedRatio(self,_mState):
        goal_counter = 0
        for carID in range(self.numberOfCars):
            if(_mState.isGoalState(carID)):
                goal_counter = goal_counter+1
        
        print 'Arrived Ratio : ',goal_counter , ' / ', self.numberOfCars


    def isGoal(self,_mState):
        goal_counter = 0
        for carID in range(self.numberOfCars):
            if(_mState.isGoalState(carID)):
                goal_counter = goal_counter+1
        
        #print goal_counter
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


    X=[]
    KGreedyAStarResult=[]
    AStarResult=[]
    BFSResult=[]

    StartSize=30
    
    EndSize =70
    
    CurrentSize =StartSize
    
    numberOfCars = 5
    
    while  CurrentSize<=EndSize:

        
        X.append(CurrentSize)
    
        mSupervisor_1 = Supervisor(numberOfCars,CurrentSize,CurrentSize,'KGreedyAStar')
        mSupervisor_2 = copy.deepcopy(mSupervisor_1)
        mSupervisor_2.setAI("AStar")
        mSupervisor_3 = copy.deepcopy(mSupervisor_1)
        mSupervisor_3.setAI("BFS")

#####################################################################################
        mState = mSupervisor_1.state
        mAI = mSupervisor_1.ai
        counter = 0
        maxTurns = numberOfCars  *  StartSize*2
        mapsForDrawer = []

        r = RedisQueue('key')
        r.flushall()

        now = datetime.now()
      
        while (not mSupervisor_1.isGoal(mState)) and (counter < maxTurns):
            for car_i in range(numberOfCars):
                # Progress bar
                sys.stdout.write('\r')
                i = int(round((20*(0.01+counter))/maxTurns))
                sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
                sys.stdout.flush()
                
                nextAction = mAI.getNextAction(car_i, mState)
                mState = mState.getStateByAction(car_i, nextAction)
                counter = counter + 1
            #print '\n***************************************************************'
            #mState.printMap()    
            mapsForDrawer.append(copy.deepcopy(mState.getMap().astype(int)))
            r.put(mapsForDrawer)
            mapsForDrawer = []
        print '\n',
        
        then = datetime.now()
        tdelta = then - now   
        seconds = tdelta.total_seconds()   
        print 'Running time of K-Greedy',seconds
        KGreedyAStarResult.append(seconds)
        
        mSupervisor_1.printArrivedRatio(mState)
        
    ###########################################################################################
        mState = mSupervisor_2.state
        mAI = mSupervisor_2.ai
        counter = 0
        maxTurns = numberOfCars*140
        mapsForDrawer = []

        r = RedisQueue('key')
        r.flushall()


        now = datetime.now()
        while (not mSupervisor_2.isGoal(mState)) and (counter < maxTurns):
            for car_i in range(numberOfCars):
                # Progress bar
                sys.stdout.write('\r')
                i = int(round((20*(0.01+counter))/maxTurns))
                sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
                sys.stdout.flush()

                nextAction = mAI.getNextAction(car_i, mState)
                mState = mState.getStateByAction(car_i, nextAction)
                counter = counter + 1
            #print '\n***************************************************************'
            #mState.printMap()    
            mapsForDrawer.append(copy.deepcopy(mState.getMap().astype(int)))
            r.put(mapsForDrawer)
            mapsForDrawer = []
        print '\n',
        
        then = datetime.now()
        tdelta = then - now   
        seconds = tdelta.total_seconds()   
        print 'Running time of AStar   ',seconds
        AStarResult.append(seconds)
        
        mSupervisor_2.printArrivedRatio(mState)
        
    ###########################################################################################
        mState = mSupervisor_3.state
        mAI = mSupervisor_3.ai
        counter = 0
        maxTurns = numberOfCars*140
        mapsForDrawer = []

        r = RedisQueue('key')
        r.flushall()


        now = datetime.now()
        while (not mSupervisor_3.isGoal(mState)) and (counter < maxTurns):
            for car_i in range(numberOfCars):
                # Progress bar
                sys.stdout.write('\r')
                i = int(round((20*(0.01+counter))/maxTurns))
                sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
                sys.stdout.flush()

                nextAction = mAI.getNextAction(car_i, mState)
                mState = mState.getStateByAction(car_i, nextAction)
                counter = counter + 1
            #print '\n***************************************************************'
            #mState.printMap()    
            mapsForDrawer.append(copy.deepcopy(mState.getMap().astype(int)))
            r.put(mapsForDrawer)
            mapsForDrawer = []
        print '\n',
        
        then = datetime.now()
        tdelta = then - now   
        seconds = tdelta.total_seconds()   
        print 'Running time of BFS     : ',seconds
        BFSResult.append(seconds)
        
        mSupervisor_3.printArrivedRatio(mState)
        
        
    ###########################################################################################  
        filename = './Results/3algo_'+str(numberOfCars)+'.out'
        f1=open(filename, 'w+')
          
        line = str(X).strip('[]')+'\n'+str(KGreedyAStarResult).strip('[]')+'\n'+str(AStarResult).strip('[]')+'\n'+str(BFSResult).strip('[]')+'\n**********************\n'
        f1.write(line)
        CurrentSize+=5
