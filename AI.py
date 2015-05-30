class Supervisor:
  #state = new State
  #cars = state.getCars()

  """for car in cars:
    nextAction = AI.nextStep(car.id, state)
    state = state.getStateByAction(car.id, nextAction)
    Drawer.draw(state)"""

from state import State
from state import Car
"""
class State:
  #- map: a static or dynamic matrix indicating the world
  #- cars: including cars position

  def getMap():
    #return current map matrix
      pass

  def getCars():
    #return all cars
      pass

  def getSucc(carId):
    #return possible actions
      pass

  def getStateByAction(carId, action):
    #move carId according to the action
    # dynamics happen here
    #return a new State
      pass
"""

class Drawer:
  def draw(state):
    #draw according to
      #- state.getMap()
      #- state.getCars()
      pass



class AI:
    def getNextAction(self,carId, state):
        """if state.cars.search=="UCS":"""
        action = self.BFS(carId,state)
        return action
    def __init__(self):
        pass
    def BFS(self,carId,state):
        """Search the node of least total cost first."""
        "*** YOUR CODE HERE ***"

        import imp
        
        foo = imp.load_source('PriorityQueue', './AI_ref/util.py')
        
        #from AI_ref/util import PriorityQueueWithFunction
        #from AI_ref/util import PriorityQueue

        #import inspect
        #print inspect.getmembers(problem, predicate=inspect.ismethod)
        exp = {}
        # exp=1...added to queue, 2...poped from queue
        st = foo.PriorityQueue()
        re = []


        #state = problem.getStartState()
        coord = state.getCarById(carId).location
        st.push( (state,[]), 0 )
        exp[coord] = 1

        #"""
        print "start point : ",; print coord
        print "dest point : ",; print state.getCarById(carId).destination
        #"""
        
        while st.isEmpty()==False:
            tmp = st.pop()
            state = tmp[0]
            move = tmp[1]
            coord = state.getCarById(carId).location
            print coord
            
            exp[coord] = 2

            if state.isGoalState(carId)==True:
                re = move
                break

            adj = state.getSucc(carId)
            for it in adj:
                Nstate = state.getStateByAction(carId, it)
                Ncoord = Nstate.getCarById(carId).location
                if ( Ncoord in exp ) == False:
                    tmpMove = list(move)
                    tmpMove.append(it)
                    #st.push( (Nstate,tmpMove), state.getCostOfActions(tmpMove) )
                    st.push( (Nstate,tmpMove), len(tmpMove) )
                    exp[Ncoord] = 1
                    print "add %r"%(Ncoord,)
                elif exp[Ncoord]==1:
                    pass
                elif exp[Ncoord]==2:
                    pass
        else:
            #print "No route found"
            #exit()
            return []

        return re[0]


"""-----------------------------------------------------------------------------
temporary function for AI.py testing
-----------------------------------------------------------------------------"""
def TestIfGoal(state):
    print state.getCarById(0).location
    print state.getCarById(0).destination
    state.getCarById(0).location = state.getCarById(0).destination
    print state.getCarById(0).location
    print state.getCarById(0).destination
    if state.getCarById(0).location==state.getCarById(0).destination:
        print True
    else:
        print False
    print state.isGoalState(0)


"""-----------------------------------------------------------------------------
simple test code for my script
emulate the supervisor

-----------------------------------------------------------------------------"""
if __name__ == '__main__':
    n_cars = 2
    a = State()
    a.generateCars(n_cars)
    a.printMap()

    ai = AI()

    #TestIfGoal(a)
    action = ai.getNextAction(0, a)
    if action==[]:
        print "No route"
    else:
        print "Action: ",; print action
        print "0's turn, next state : ",; print a.getStateByAction(0,action).getCarById(0).location
    print "End of script"
    
"""
    for carId in range(len(a.getCars())):
        print 'carid ', carId
        actions = a.getSucc(carId)
        for action in actions :
            print 'step :' ,action
            a.getStateByAction(carId,action).printMap()
"""





"""-----------------------------------------------------------------------------



-----------------------------------------------------------------------------"""







