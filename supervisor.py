import State
import Drawer

class Supervisor:
    # _map includes
    #    method for moving a car( e.g., map.moveCar(car, from, to) )
    # _cars includes the cars and it type, priority and speed
    def __init__(self):
        self.state = new State
        self.cars = state.getCars()

        # Initializing the remain moves of cars
        self.carMovesRemain = []
        for car in self.carList:
            self.carMovesRemain.append(car.speed)


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
        for car in self.carList:
            if(car.location == car.destination):
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


if __name__ == '__main__':
    pass
