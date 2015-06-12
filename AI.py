import random
from state import State
from state import Car
import math
import imp
class AI:
    AIName = 'randomWalk'
    KGreedyArray = []
    K =7
    def getNextAction(self,carId, state):
        """if state.cars.search=="UCS":"""
        #action = self.randomWalk(carId,state)
        #action = self.BFS(carId,state)
        #action = self.AStar(carId,state,self.hueristic_manDist)
        action = self.KGreedyAStar(carId,state,self.hueristic_manDist)
        if(self.AIName =='BFS'):
            action = self.BFS(carId,state)
        elif(self.AIName =='AStar'):
            action = self.AStar(carId,state,self.hueristic_manDist)
        elif(self.AIName =='KGreedyAStar'):
            action = self.KGreedyAStar(carId,state,self.hueristic_manDist)
        else:
            action = self.randomWalk(carId,state)
        return action

    def __init__(self,_numberOfCars,_AIName):
        self.AIName = _AIName
        for i in range(_numberOfCars):
            KGreedyQueue= imp.load_source('Queue', './AI_ref/util.py').Queue()
            KGreedyRegretQueue = imp.load_source('Queue', './AI_ref/util.py').Queue()
            self.KGreedyArray.append((KGreedyQueue,KGreedyRegretQueue))
        

    def randomWalk(self,carId,state):
        if len( state.getSucc(carId) ) ==0:
            return 'none'
        else :
            return random.sample(state.getSucc(carId),1)[0]

    def BFS(self,carId,state):



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
        #print "start point : ",; print coord
        #print "dest point : ",; print state.getCarById(carId).destination
        #"""

        while st.isEmpty()==False:
            tmp = st.pop()
            state = tmp[0]
            move = tmp[1]
            coord = state.getCarById(carId).location
            #print coord

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
                    #print "add %r"%(Ncoord,)
                elif exp[Ncoord]==1:
                    pass
                elif exp[Ncoord]==2:
                    pass
             
        if len( re ) ==0:
            return 'none'
        else:
            return re[0]
    def KGreedyAStar(self,carId,state,hueristic,ch=5,cc=3):

        foo = imp.load_source('PriorityQueue', './AI_ref/util.py')

        #import inspect
        #print inspect.getmembers(problem, predicate=inspect.ismethod)
        exp = {}
        # exp=1...added to queue, 2...poped from queue
        st = foo.PriorityQueue()
        
        re = []


        #state = problem.getStartState()
        coord = state.getCarById(carId).location
        st.push( (state,[]), hueristic(carId,state)*ch + 0*cc )
        exp[coord] = 1

        #"""
        #print "start   point : ",; print state.getCarById(carId).start
        #print "current point : ",; print coord
        #print "dest    point : ",; print state.getCarById(carId).destination
        #print '-----'
        #"""

        #if (self.KGreedyQueue.isEmpty()==True and self.KGreedyRegretQueue.isEmpty()==True):
        if (self.KGreedyArray[carId][0].isEmpty()==True ):

            while st.isEmpty()==False:
                tmp = st.pop()
                state = tmp[0]
                move = tmp[1]
                coord = state.getCarById(carId).location
                #print coord

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
                        st.push( (Nstate,tmpMove), hueristic(carId,Nstate)*ch + len(tmpMove)*cc )
                        exp[Ncoord] = 1
                        #print "add %r"%(Ncoord,)
                    elif exp[Ncoord]==1:
                        pass
                    elif exp[Ncoord]==2:
                        pass
            if len( re ) ==0:
                return 'none'
            else :
                for i in range (min(self.K,len(re))):             
                    if re[i] == 'north' : regretStep ='south'
                    if re[i] == 'south' : regretStep ='north'
                    if re[i] == 'west' : regretStep ='east'
                    if re[i] == 'east' : regretStep ='west'
                    self.KGreedyArray[carId][0].push(re[i]) 
                    self.KGreedyArray[carId][1].push (regretStep)
                #print carId,'\'s Consideration : ',re
                self.KGreedyArray[carId][0].pop() 
                self.KGreedyArray[carId][1].pop()
                return re[0]
            
        else:
            #print carId,'\'s Greedy  kstep : ',self.KGreedyArray[carId][0].list[::-1]
            #print carId,'\'s Greedy RGstep : ',self.KGreedyArray[carId][1].list[::-1]
            greedyStep = self.KGreedyArray[carId][0].pop()
            regretStep = self.KGreedyArray[carId][1].pop() 
            
            if(greedyStep in state.getSucc(carId)):
                return greedyStep
            #elif(regretStep in state.getSucc(carId)):
            #    return regretStep 
            else:
                KGreedyQueue= imp.load_source('Queue', './AI_ref/util.py').Queue()
                KGreedyRegretQueue = imp.load_source('Queue', './AI_ref/util.py').Queue()
                self.KGreedyArray[carId] = (KGreedyQueue,KGreedyRegretQueue)
                return self.KGreedyAStar(carId,state,hueristic,ch,cc)
                
                
                
    def AStar(self,carId,state,hueristic,ch=5,cc=3):



        foo = imp.load_source('PriorityQueue', './AI_ref/util.py')

        #import inspect
        #print inspect.getmembers(problem, predicate=inspect.ismethod)
        exp = {}
        # exp=1...added to queue, 2...poped from queue
        st = foo.PriorityQueue()
        re = []


        #state = problem.getStartState()
        coord = state.getCarById(carId).location
        st.push( (state,[]), hueristic(carId,state)*ch + 0*cc )
        exp[coord] = 1

        #"""
        #print "start point : ",; print coord
        #print "dest point : ",; print state.getCarById(carId).destination
        #"""

        while st.isEmpty()==False:
            tmp = st.pop()
            state = tmp[0]
            move = tmp[1]
            coord = state.getCarById(carId).location
            #print coord

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
                    st.push( (Nstate,tmpMove), hueristic(carId,Nstate)*ch + len(tmpMove)*cc )
                    exp[Ncoord] = 1
                    #print "add %r"%(Ncoord,)
                elif exp[Ncoord]==1:
                    pass
                elif exp[Ncoord]==2:
                    pass
             
        if len( re ) ==0:
            return 'none'
        else:
            return re[0]
    
    def hueristic_BFS(self,carId,state):
        return 0
    def hueristic_manDist(self,carId,state):
        car = state.getCarById(carId)
        x = car.location[0]
        y = car.location[1]
        dx = car.destination[0]
        dy = car.destination[1]
        dist = abs(dx-x)+abs(dy-y)
        return dist
    def hueristic_eucDist(self,carId,state):
        car = state.getCarById(carId)
        x = car.location[0]
        y = car.location[1]
        dx = car.destination[0]
        dy = car.destination[1]
        dist = math.sqrt( pow(dx-x,2)+pow(dy-y,2))
        return dist


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
    ai = AI()

    # ---------------------------------------------------------------------------
    # Lai, question1, how to generate cars ?

    choice = 3

    if choice==1:
    # choice 1, 1 block left, still could generate car
        a.currentMap[:,:] = -2
        a.currentMap[1,1] = -1
    elif choice==2:
    # choice 2, no block left, can't generate car
        a.currentMap[:,:] = -2

    # ---------------------------------------------------------------------------
    
    a.generateCars(n_cars)
    a.printMap()


    #TestIfGoal(a)
    print "0 in now at : ",; print a.getCarById(0).location
    
    action = ai.getNextAction(0, a)
    if action==[]:
        print "No route"
    else:
        print "Action: ",; print action
        print "0's turn, next state : ",; print a.getStateByAction(0,action).getCarById(0).location
    print "End of script"
    
    print a.getCarById(0).destination
    print "man= ",
    print ai.hueristic_manDist(0,a)
    print "euc= ",
    print ai.hueristic_eucDist(0,a)
    exit()

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







