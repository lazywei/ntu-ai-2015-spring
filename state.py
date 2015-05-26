import numpy as np
import random
class car :
    #car.type : 'vehicle', 'taxi', 'ambulance'
    #car.location : (x,y)
    #car.start : (x,y)
    #car.destination : (x,y)
    #car.priority : 'high', 'medium', 'low'
    #car.speed : 1, 2, 3
    id = 0
    type = 'vehicle'
    location = (0,0)
    start = (0,0)
    destination = (0,0)
    priority = 0
    speed = 1
    def __init__(self,new_id,new_type,new_location,new_start,new_destination,new_priority,new_speed):
        self.id  = new_id
        self.type = new_type
        self.location = new_location
        self.start = new_start
        self.destination = new_destination
        self.priority = new_priority
        self.speed = new_speed
        #print '###LOG### : A car has been constructed'
    def toString(self):
        print self.type,',',self.location,',',self.start,',',self.destination,',',self.priority,',',self.speed
    
class State:
    #- map: a static or dynamic matrix indicating the world
    #- cars: including cars position
    currentMap = []
    cars = []
    mapMaxX = 0
    mapMaxY = 0
    
    ######################
    #  In map 
    #  0 = road
    #  -1= obstacle
    #  >=1 car
    ######################

    def __init__(self):
        print '__init__(self)'
    
    
    def loadMap(self):
        self.currentMap = np.loadtxt('map.out')
        self.mapMaxX = len(self.currentMap)
        self.mapMaxY = len(self.currentMap[0])

    
    #Done
    def getMap(self):
        return self.currentMap
    #Done
    def getCars(self):
        return self.cars
    
    #Not yet QQ
    def getSucc(self,carId):
        actions = []        
        ##north
        nextX = self.cars[carId].location[0]-1
        nextY = self.cars[carId].location[1]
        if nextX >=0 :
            if self.currentMap[nextX][nextY] ==0 : 
                actions.append('north')
        ##south
        nextX = self.cars[carId].location[0]+1
        nextY = self.cars[carId].location[1]
        if nextX <self.mapMaxX :
            if self.currentMap[nextX][nextY] ==0 : 
                actions.append('south')
        ##west
        nextX = self.cars[carId].location[0]
        nextY = self.cars[carId].location[1]-1
        if nextY >=0 :
            if self.currentMap[nextX][nextY] ==0 : 
                actions.append('west')
        ##east
        nextX = self.cars[carId].location[0]
        nextY = self.cars[carId].location[1]+1
        if nextY <self.mapMaxY :
            if self.currentMap[nextX][nextY] ==0 : 
                actions.append('east')
                
                      
        return actions

    def getStateByAction(self,carId, action):
        print 'getStateByAction(carId, action)'
        #move carId according to the action
        # dynamics happen here
        #return a new State
        
   #################################################################
   # Temporary function, just for testing State.py's functionality #
   #################################################################
    def generateCars(self,n_cars):
        
        for i in range( n_cars+1):
            sx = random.choice(np.arange(self.mapMaxX)) 
            sy = random.choice(np.arange(self.mapMaxY)) 
            
            dx = random.choice(np.arange(self.mapMaxX)) 
            dy = random.choice(np.arange(self.mapMaxY))
            self.cars.append(  car(  i+1,'vehicle',(sx,sy)  ,  (sx,sy)   ,  (dx,dy)  , 0 , 1)  )

            self.currentMap[sx][sy] = i+1
    def printMap(self,map):
        for row in map:
            for c in row:
                if c == 0:
                    print "  ",
                elif c == -1:
                    print "XX",
                else:
                    print '%2d'%c,
            print '\n',
            
            
##Just my testing script vvvvvv
if __name__ == '__main__':

    a = State()
    a.loadMap()
    map = a.getMap()
    a.generateCars(50)
    a.printMap(map)
    for i in range(50):
        print a.getSucc(i)
    #for c in a.getCars():
    #    c.toString()
