class Supervisor:
  #state = new State
  #cars = state.getCars()

  """for car in cars:
    nextAction = AI.nextStep(car.id, state)
    state = state.getStateByAction(car.id, nextAction)
    Drawer.draw(state)"""

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


class Drawer:
  def draw(state):
    #draw according to
      #- state.getMap()
      #- state.getCars()
      pass



class AI:
    def getNextAction(carId, state):
        """if state.cars.search=="UCS":"""
        action = self.BFS(carId,state)
        return action
    def __init__(self):
        pass
    def BFS(self,carId,state):
        """Search the node of least total cost first."""
        "*** YOUR CODE HERE ***"

        from util import PriorityQueueWithFunction
        from util import PriorityQueue

        #import inspect
        #print inspect.getmembers(problem, predicate=inspect.ismethod)
        exp = {}
        # exp=1...added to queue, 2...poped from queue
        st = PriorityQueue()
        re = []


        #state = problem.getStartState()
        st.push( (state,[]), 0 )
        exp[state] = 1
        
        while st.isEmpty()==False:
            tmp = st.pop()
            state = tmp[0]
            move = tmp[1]
            #print problem.getCostOfActions(move)
            
            exp[state] = 2

            if state.isGoalState(carId)==True:
                re = move
                break

            adj = state.getSucc(carId)
            for it in adj:
                Nstate = state.getStateByAction(carId, it)
                if ( Nstate in exp ) == False:
                    tmpMove = list(move)
                    tmpMove.append(it)
                    #st.push( (Nstate,tmpMove), state.getCostOfActions(tmpMove) )
                    st.push( (Nstate,tmpMove), len(tmpMove) )
                    exp[Nstate] = 1
                elif exp[Nstate]==1:
                    pass
                elif exp[Nstate]==2:
                    pass
        else:
            print "No route found"
            return []

        return re
















