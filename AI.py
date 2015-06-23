import random
from state import State
from state import Car
import math
import sys
import imp

from collections import deque
import numpy
import math

class Graph:
    def __init__(self):
        self.V=[]
    def Add(self,v):
        self.V.append(v)
    def Clear(self):
        self.V.clear()
    def PrintEdge(self):
        for u in self.V:
            print u.name + " -> ",
            for (v,e) in u.p:
                if v!=None:
                    print "("+v.name+","+str(e)+")",
                else:
                    print "("+"None"+","+str(e)+")",
            print
    def _PrintChild(self,root,indent):
        #v = self.V[root]
        for (u,e) in root.p:
            for i in range(indent): print "\t",
            print "%s, %f"%(u.name,e)
            self._PrintChild(u,indent+1)
    def Print(self,root):
        print "%s"%(root.name)
        self._PrintChild(root,1)

class Node:
    def __init__(self,name):
        self.name=name
        self.p=[]
    def AddEdge(self,v,e=0):
        self.p.append((v,e))
    def Adj(self):
        return [ v for (v,e) in self.p ]

def BFS_sub(root,exp):
    q=deque()

    q.append(root)
    exp[root]=1

    while len(q) != 0:
        t=q.pop()
        print t.name + ", ",
        exp[t]=2

        for (v,e) in t.p:
            if v not in exp:
                q.append(v)
                exp[v]=1
        exp[t]=3
def BFS(G,root):
    exp={}
    BFS_sub(root,exp)
    for v in G.V:
        if v not in exp:
            BFS_sub(v,exp)
    print




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
        elif(self.AIName =='hueristic'):
            action = self.PureHueristic()
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
def BC(x,y):
    if x>=0 and x<30 and y>=0 and y<30:
        return True
    else:
        return False
def CR(map,x,y):
    r=0
    if x-1<0 or map[x-1][y]==-1 or map[x-1][y]>=0:
        r+=1
    if x+1>=30 or map[x+1][y]==-1 or map[x+1][y]>=0:
        r+=1
    if y-1<0 or map[x][y-1]==-1 or map[x][y-1]>=0:
        r+=1
    if y+1>=30 or map[x][y+1]==-1 or map[x][y+1]>=0:
        r+=1
    return r
def TR(map,x,y,dir,Vdic):
    ofx={ "up":-1, "down":1, "right":0, "left":0 }
    ofy={ "up":0, "down":0, "right":1, "left":-1 }
    dis=0
    x=x+ofx[dir]; y=y+ofy[dir]
    while BC( x,y ) and map[x][y]!=-2:
        dis=dis+1
        if (x,y) in Vdic: return (dis,Vdic[(x,y)])
        x=x+ofx[dir]; y=y+ofy[dir]
    return (dis,None)
def MapToGraph(map):
    G=Graph()
    # build all nodes
    Vdic={}
    for x in range(h):
        for y in range(w):
            if CR(map,x,y)==4:
                v=Node( str((x,y)) )
                Vdic[ (x,y) ] = v
                G.Add(v)
    # build edge
    for x in range(h):
        for y in range(w):
            if (x,y) in Vdic:
                v=Vdic[ (x,y) ]
                dirs=["up", "down", "right", "left"]
                for dir in dirs:
                    (e,u) = TR(map,x,y,dir,Vdic)
                    if u!=None:
                        #print v.name
                        v.AddEdge(u,e-1)
                    else:
                        u=Node( dir )
                        G.Add(u)
                        v.AddEdge(u,e)
    return (G,Vdic)
def CarEdge(G,Vdic,state):
    Edic={}; Cdic={}
    map=a.currentMap
    for i in range(len(state.getCars())):
        car=state.getCarById(i)
        (x,y) = car.location
        dirs=["up", "down", "right", "left"]
        con=[]
        for dir in dirs:
            (e,v)=TR(map,x,y,dir,Vdic)
            con.append( (e,v,dir) )
        if (x,y) in Vdic:
            # Dirty ################################
            con.sort(); con.reverse()
            v=Vdic[(x,y)]; u=con[0][1]
            if u==None:
                for u in v.Adj():
                    if u.name==con[0][2]: break
            pass
        elif con[0][1]!=None or con[1][1]!=None:
            v=con[0][1]; u=con[1][1]
            if u==None:
                for u in v.Adj():
                    if u.name==con[1][2]: break
            if v==None:
                for v in u.Adj():
                    if v.name==con[0][2]: break
            pass
        elif con[2][1]!=None or con[3][1]!=None:
            v=con[2][1]; u=con[3][1]
            if u==None:
                for u in v.Adj():
                    if u.name==con[3][2]: break
            if v==None:
                for v in u.Adj():
                    if v.name==con[2][2]: break
            pass
        Cdic[i]=(v,u)
        if (v,u) not in Edic: Edic[(v,u)]=[]
        Edic[(v,u)].append(i)
        if (u,v) not in Edic: Edic[(u,v)]=[]
        Edic[(u,v)].append(i)
    return (Edic,Cdic)
def IfSave(Edic,Cdic):
    dirs=["up", "down", "right", "left"]
    f=True
    for (v,u) in Edic:
        cap=0
        for (p,e) in v.p:
            if p!=u: cap=cap+e-len(Edic[(v,p)])
        for (p,e) in u.p:
            if p!=v: cap=cap+e-len(Edic[(u,p)])
        if cap<=len(Edic[(v,u)]): f=False
    return f

if __name__ == '__main__':
    n_car=120
    w=30; h=30
    a = State(30,30)
    ai = AI(n_car,"KGreedyAStar")
    a.generateCars(n_car)
    #a.printMap()
    
    """
    for x in range(h):
        for y in range(w):
            if a.currentMap[x][y]==-2:
                sys.stdout.write("\219\219")
            elif a.currentMap[x][y]==-1:
                sys.stdout.write("  ")
            elif a.currentMap[x][y]>=0:
                sys.stdout.write("OO")
            #sys.stdout.write( "%2d"%(int(a.currentMap[x][y])) )
        sys.stdout.write("\n")
    """
    (G,Vdic) = MapToGraph(a.currentMap)
    (Edic,Cdic) = CarEdge(G,Vdic,a)
    #G.PrintEdge()
    """
    for i in range(len(a.getCars())):
        print Cdic[i]
        """
    
    for v in Vdic.itervalues():
        for u in v.Adj():
            if (v,u) not in Edic:
                Edic[(v,u)]=[]
                Edic[(u,v)]=[]
    """
    for v in Vdic.itervalues():
        for u in v.Adj():
            if (v,u) in Edic:
                print len(Edic[(v,u)]),
    print
    """
    print IfSave(Edic,Cdic)
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







