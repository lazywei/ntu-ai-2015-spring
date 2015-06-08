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
        print "{}, {}, {}, {}, {}, {}".format(
            self.type_, self.location, self.start,
            self.destination, self.priority, self.speed)

    def getId(self):
        return self.id_


class State(object):
    ######################
    #  In map
    #  -2...-n = obstacles
    #  -1 = road
    #  >=0 car
    ######################

    def __init__(self, width=40, height=40):
        self.currentMap = None
        self.mapMaxX = height
        self.mapMaxY = width
        self._generateMap(width, height)
        self.cars_ = {}

    def _generateMap(self, width, height):
        curMap = np.zeros((width, height)) - 2

        n_xs = int(height / 3)
        n_ys = np.random.randint(3, width / 3)

        xs = range(height / 3)
        np.random.shuffle(xs)
        xs = np.array(xs[:n_xs], dtype=int) * 3

        ys = range(width / 3)
        np.random.shuffle(ys)
        ys = np.array(ys[:n_ys], dtype=int) * 3

        curMap[xs, :] = -1
        curMap[:, ys] = -1

        self.currentMap = curMap
        self.mapMaxX = len(self.currentMap)
        self.mapMaxY = len(self.currentMap[0])
        '''
        curMap = curMap-1
        self.currentMap = curMap
        self.mapMaxX = height
        self.mapMaxY = width
        '''

    def getMap(self):
        return self.currentMap

    def getCars(self):
        return self.cars_

    def getCarById(self, carId):
        return self.cars_[carId]

    def getSucc(self, carId):
        actions = []

        directions = {
            'north': [-1, 0],
            'south': [1, 0],
            'west': [0, -1],
            'east': [0, 1]
        }

        for direction in directions:
            offset = directions[direction]
            nextX = self.cars_[carId].location[0] + offset[0]
            nextY = self.cars_[carId].location[1] + offset[1]

            # Check if the move is legal
            if (0 <= nextX < self.mapMaxX and 0 <= nextY < self.mapMaxY
                    and self.currentMap[nextX][nextY] == -1):

                actions.append(direction)

        return actions

    def getStateByAction(self, carId, action):
        new_state = copy.deepcopy(self)

        curCar = self.cars_[carId]
        curCarX = curCar.location[0]
        curCarY = curCar.location[1]

        dirDiff = {
            'north': [-1, 0],
            'south': [1, 0],
            'east': [0, 1],
            'west': [0, -1],
            'none': [0, 0],
        }

        xDiff = dirDiff[action][0]
        yDiff = dirDiff[action][1]

        new_state.currentMap[curCarX, curCarY] = -1
        new_state.currentMap[curCarX + xDiff, curCarY + yDiff] = carId
        new_state.cars_[carId].location = (
            new_state.cars_[carId].location[0] + xDiff,
            new_state.cars_[carId].location[1] + yDiff)

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
                if self.currentMap[sx][sy] and self.currentMap[dx][dy]  == -1:
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


