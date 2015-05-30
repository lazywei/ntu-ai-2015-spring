import numpy as np
import random
import copy


class Car(object):
    # car.type : 'vehicle', 'taxi', 'ambulance'
    # car.location : (x,y)
    # car.start : (x,y)
    # car.destination : (x,y)
    # car.priority : 'high', 'medium', 'low'
    # car.speed : 1, 2, 3

    id_ = 0
    type_ = 'vehicle'
    location = (0, 0)
    start = (0, 0)
    destination = (0, 0)
    priority = 0
    speed = 1

    def __init__(self, new_id, new_type, new_location, new_start,
                 new_destination, new_priority, new_speed):
        self.id_ = new_id
        self.type_ = new_type
        self.location = new_location
        self.start = new_start
        self.destination = new_destination
        self.priority = new_priority
        self.speed = new_speed
        # print '###LOG### : A car has been constructed'

    def toString(self):
        print self.type,',',self.location,',',self.start,',',self.destination,',',self.priority,',',self.speed

    def getId(self):
        return self.id_


class State(object):
    ######################
    #  In map
    #  -2...-n = obstacles
    #  -1= road
    #  >=0 car
    ######################

    def __init__(self, width=20, height=20):
        print '__init__(self)'
        self.currentMap = None
        self.mapMaxX = 0
        self.mapMaxY = 0
        self._generateMap(width, height)
        self.cars_ = {}

    def _generateMap(self, width, height):
        self.currentMap = np.loadtxt('map.out')
        self.mapMaxX = self.currentMap.shape[0]
        self.mapMaxY = self.currentMap.shape[1]

    def getMap(self):
        return self.currentMap

    def getCars(self):
        return self.cars_

    def getCarById(self, carId):
        return self.cars_[carId]

    #Done
    def getSucc(self, carId):
        actions = []
        ##north
        nextX = self.cars_[carId].location[0]-1
        nextY = self.cars_[carId].location[1]
        if nextX >=0 :
            if self.currentMap[nextX][nextY] == -1 :
                actions.append('north')
        ##south
        nextX = self.cars_[carId].location[0]+1
        nextY = self.cars_[carId].location[1]
        if nextX < self.mapMaxX:
            if self.currentMap[nextX][nextY] == -1 :
                actions.append('south')
        ##west
        nextX = self.cars_[carId].location[0]
        nextY = self.cars_[carId].location[1]-1
        if nextY >=0 :
            if self.currentMap[nextX][nextY] == -1 :
                actions.append('west')
        ##east
        nextX = self.cars_[carId].location[0]
        nextY = self.cars_[carId].location[1]+1
        if nextY <self.mapMaxY :
            if self.currentMap[nextX][nextY] == -1 :
                actions.append('east')


        return actions

    def getStateByAction(self,carId, action):
        new_state = copy.deepcopy(self)
        curCar = self.cars_[carId]
        if action is 'north':
            new_state.currentMap[ curCar.location[0] ][ curCar.location[1]  ] = -1
            new_state.currentMap[ curCar.location[0]-1 ][ curCar.location[1]  ]   = carId
            new_state.cars_[carId].location = ( new_state.cars_[carId].location[0]-1, new_state.cars_[carId].location[1] )    # Lai, change car position as well ?
        if action is 'south':
            new_state.currentMap[ curCar.location[0] ][ curCar.location[1]  ] = -1
            new_state.currentMap[ curCar.location[0]+1 ][ curCar.location[1]  ]   = carId
            new_state.cars_[carId].location = ( new_state.cars_[carId].location[0]+1, new_state.cars_[carId].location[1] )    # Lai, change car position as well ?
        if action is 'east':
            new_state.currentMap[ curCar.location[0] ][ curCar.location[1]  ] = -1
            new_state.currentMap[ curCar.location[0] ][ curCar.location[1]+1  ]   = carId
            new_state.cars_[carId].location = ( new_state.cars_[carId].location[0], new_state.cars_[carId].location[1]+1 )    # Lai, change car position as well ?
        if action is 'west':
            new_state.currentMap[ curCar.location[0] ][ curCar.location[1]  ] = -1
            new_state.currentMap[ curCar.location[0] ][ curCar.location[1]-1  ]   = carId
            new_state.cars_[carId].location = ( new_state.cars_[carId].location[0], new_state.cars_[carId].location[1]-1 )    # Lai, change car position as well ?
        return new_state
        #print 'getStateByAction(carId, action)'
        #move carId according to the action
        # dynamics happen here
        #return a new State

   #################################################################
   # Temporary function, just for testing State.py's functionality #
   #################################################################
    def generateCars(self,n_cars):

        for i in range(n_cars):
            while True:
                sx = random.choice(np.arange(self.mapMaxX))
                sy = random.choice(np.arange(self.mapMaxY))

                dx = random.choice(np.arange(self.mapMaxX))
                dy = random.choice(np.arange(self.mapMaxY))
                if self.currentMap[sx][sy]== -1:
                    break

            newCar = Car(  i,'vehicle',(sx,sy)  ,  (sx,sy)   ,  (dx,dy)  , 0 , 1)

            self.cars_[newCar.getId()] = newCar
            self.currentMap[sx][sy] = i

    def printMap(self):
        map = self.currentMap
        for row in map:
            for c in row:
                if c == -1:
                    print "  ",
                elif c == -2:
                    print "XX",
                else:
                    print '%2d'%c,
            print '\n',

   #################################################################
   # Temporary function, help add for AI.py ??                     #
   #################################################################
    def isGoalState(self,carId):
        """
        print "inside isGoalState"
        print "carId = "; print carId
        print self.getCarById(carId).location
        print self.getCarById(carId).destination
        """
        if self.getCarById(carId).location == self.getCarById(carId).destination:
            return True
        else:
            return False


#Just my testing script down below
#Simulating the supervisor
if __name__ == '__main__':
    n_cars = 2
    a = State()
    a.generateCars(n_cars)
    a.printMap()

    for carId, car in enumerate(a.getCars()):
        print 'carid ', carId
        actions = a.getSucc(carId)
        for action in actions :
            print 'step :' ,action
            a.getStateByAction(carId,action).printMap()

    #for c in a.getCars():
    #    c.toString()
