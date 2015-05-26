import numpy as np
import random
class car :
    #car.type : 'vehicle', 'taxi', 'ambulance'
    #car.location : (x,y)
    #car.start : (x,y)
    #car.destination : (x,y)
    #car.priority : 'high', 'medium', 'low'
    #car.speed : 1, 2, 3
    type = 'vehicle'
    location = (0,0)
    start = (0,0)
    destination = (0,0)
    priority = 0
    speed = 1
    def __init__(self,new_type,new_location,new_start,new_destination,new_priority,new_speed):
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
    
    ###Need a function to read from map and decide, now hard coded.
    mapMaxY = 20
    mapMaxX = 30
    def __init__(self):
        print '__init__(self)'

    def loadMap(self):
        self.currentMap = np.loadtxt('map.out')
    def getMap(self):
        return self.currentMap

    def getCars(self):
        return self.cars

    def getSucc(carId):
        print 'getSucc(carId)'
        #return possible actions

    def getStateByAction(carId, action):
        print 'getStateByAction(carId, action)'
        #move carId according to the action
        # dynamics happen here
        #return a new State
        
   #################################################################
   # Temporary function, just for testing State.py's functionality #
   #################################################################
    def generateCars(self,n_cars):
        
        for i in range( n_cars):
            sx = random.choice(np.arange(self.mapMaxX)) 
            sy = random.choice(np.arange(self.mapMaxY)) 
            
            dx = random.choice(np.arange(self.mapMaxX)) 
            dy = random.choice(np.arange(self.mapMaxY))
        
            self.cars.append(  car(  'vehicle',(sx,sy)  ,  (sx,sy)   ,  (dx,dy)  , 0 , 1)  )
   
    def printMap(self,map):
        for row in map:
            for c in row:
                if c == 0:
                    print "  ",
                if c == -1:
                    print "XX",
            print '\n',
            
            
##Just my testing script vvvvvv
if __name__ == '__main__':

    a = State()
    a.loadMap()
    map = a.getMap()
    a.printMap(map)
    a.generateCars(10)
    for c in a.getCars():
        c.toString()
