# myAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from game import Agent
from game import Actions
from game import Directions
from searchProblems import PositionSearchProblem

import game
import util
import time
import search

"""
Version2.1:全新策略
调参，目前最佳
普通人的init             self.init = 3
skip = 0的人的init       self.init = SKIPCOEF // 2
开始转战的系数            SKIPCOEF = (m // 2 // (maxIndex - minIndex))+1
开始后转战步数            skip = m // 2 // self.pacmanNumber
最高得分：1190.6690497116244
"""

"""
IMPORTANT
`agent` defines which agent you will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent
"""
def createAgents(num_pacmen, agent='MyAgent'):
    return [eval(agent)(index=i) for i in range(num_pacmen)]


class MyAgent(Agent):
    """
    Implementation of your agent.
    """

    def getAction(self, state):
        """
        Returns the next action the agent will take
        """
        "*** YOUR CODE HERE ***"

        if self.goal is not None:
            x, y = self.goal
            if not state.hasFood(x, y) and len(self.actions) > 0:
                if self.init > 0:
                    self.actions = []
                    self.goal = None
                    # print("Agent:", self.index, self.init)
                else:
                    m = state.getNumFood()
                    skip = m // 2 // self.pacmanNumber
                    if skip == 0:
                        skip = m - 1
                    problem = SkipFoodSearchProblem(state, self.index, skip)
                    self.actions, self.goal = bfs(problem)
                    # self.goal = None
        if len(self.actions) > 0:
            action = self.actions[0]
            del self.actions[0]
            return action
        else:
            problem = AnyFoodSearchProblem(state, self.index)
            self.actions, self.goal = bfs(problem)
            self.init -= 1
            return self.getAction(state)

    def initialize(self):
        """
        Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank
        """
        "*** YOUR CODE HERE"
        self.init = 4
        self.actions = []
        self.goal = None


    def registerInitialState(self, state):
        n = state.getNumAgents()
        self.pacmanNumber = n
        if n == 1:
            return
        problem = AgentsSearchProblem(state, self.index)
        nearbyPacmen = breadthFirstSearchCountLimited(problem, 7)
        nearbyPacmenNumber = len(nearbyPacmen)
        if nearbyPacmenNumber == 1:
            return
        pacmanPositions = state.getPacmanPositions()
        m = state.getNumFood()
        pacmanIndexes = {}
        for i in range(n):
            pacmanIndexes[pacmanPositions[i]] = i
        # myPosition = pacmanPositions[self.index]
        # print("Agent:", self.index, pacmanPositions)
        # print(nearbyPacmenNumber)
        minIndex = self.index
        maxIndex = self.index
        for pacman in nearbyPacmen:
            tmp = pacmanIndexes[pacman]
            if tmp < minIndex:
                minIndex = tmp
            elif tmp > maxIndex:
                maxIndex = tmp
        # for i in range(n):
        #     # if pacmanPositions[i] == myPosition:
        #     if pacmanPositions[i][0] and pacmanPositions[i][1]
        #         nearbyPacmen.append(i)
        # print("Agent:", self.index, 'NearbyPacman:', len(nearbyPacmen))
        SKIPCOEF = (m // 2 // (maxIndex - minIndex))+1
        # print("SKIPCOEF", SKIPCOEF)
        rank = self.index - minIndex
        skip = rank * SKIPCOEF
        # if skip == 0:
        #     self.init = SKIPCOEF // 2 - 1
        if skip == 0:
            self.init = SKIPCOEF // 2 - 1
        else:
            self.init = SKIPCOEF // 2**(rank+2)
        # print("Agent:", self.index, 'Skip:', skip)
        problem = SkipFoodSearchProblem(state, self.index, skip)
        self.actions, state = bfs(problem)


"""
Put any other SearchProblems or search methods below. You may also import classes/methods in
search.py and searchProblems.py. (ClosestDotAgent as an example below)
"""


def bfs(problem):
    closed = []
    queue = util.Queue()
    queue.push((problem.getStartState(), []))
    while 1:
        if queue.isEmpty():
            return [], None
        current_node = queue.pop()
        current_location = current_node[0]
        current_actions = current_node[1]
        if problem.isGoalState(current_location):
            return current_actions, current_actions
        if current_location not in closed:
            closed.append(current_location)
            for successor in problem.getSuccessors(current_location):
                queue.push((successor[0], current_actions + [successor[1]]))

'''
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    closed_set = set([])
    from util import Queue
    fringes = Queue()
    state = problem.getStartState()
    node = (state, None)
    temp_fringe = [node]
    fringes.push(temp_fringe)
    while not fringes.isEmpty():
        fringe = fringes.pop()
        state = fringe[-1][0]
        if problem.isGoalState(state):
            actions = []
            for node in fringe[1:]:
                actions.append(node[1])
            return actions, state
        if state not in closed_set:
            closed_set.add(state)
            successors = problem.getSuccessors(state)
            for successor in successors:
                # if successor[0] == state:
                #     continue
                node = (successor[0], successor[1])
                temp_fringe = fringe.copy()
                temp_fringe.append(node)
                fringes.push(temp_fringe)
    # print('Not found!')
    return [], None
'''

def bfsDepth(problem, depth):
    closed = []
    queue = util.Queue()
    queue.push((problem.getStartState(), []))
    while 1:
        if queue.isEmpty():
            return [], None
        current_node = queue.pop()
        current_location = current_node[0]
        current_actions = current_node[1]
        if problem.isGoalState(current_location):
            return current_actions, current_actions
        if current_location not in closed:
            closed.append(current_location)
            if len(current_actions) == depth:
                continue
            for successor in problem.getSuccessors(current_location):
                queue.push((successor[0], current_actions + [successor[1]]))

'''
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # count = 0
    goals = []
    closed_set = set([])
    from util import Queue
    fringes = Queue()
    state = problem.getStartState()
    node = state
    temp_fringe = [node]
    fringes.push(temp_fringe)
    while not fringes.isEmpty():
        fringe = fringes.pop()
        state = fringe[-1]
        # if problem.isGoalState(state):
        #     actions = []
        #     for node in fringe[1:]:
        #         actions.append(node[1])
        #     return actions
        if state not in closed_set:
            closed_set.add(state)
            if problem.isGoalState(state):
                goals.append(state)
            successors = problem.getSuccessors(state)
            for successor in successors:
                # if successor[0] == state:
                #     continue
                node = successor[0]
                temp_fringe = fringe.copy()
                temp_fringe.append(node)
                if len(temp_fringe) > limit:
                    continue
                fringes.push(temp_fringe)
    return goals
'''

class SkipFoodSearchProblem(PositionSearchProblem):
    def __init__(self, gameState, agentIndex, skip):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()
        self.skip = skip
        self.skipedFood = set([])

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        x, y = state
        if not self.food[x][y]:
            return False
        if state in self.skipedFood:
            return False
        if self.skip > 0:
            self.skip -= 1
            self.skipedFood.add(state)
            return False
        return True


class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState, agentIndex):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()
        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.costFn = lambda x: 1
        self.startState = gameState.getPacmanPosition(agentIndex)
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        return self.food[state[0]][state[1]]
        # util.raiseNotDefined()

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
            For a given state, this should return a list of triples, (successor,
            action, stepCost), where 'successor' is a successor to the current
            state, 'action' is the action required to get there, and 'stepCost'
            is the incremental cost of expanding to that successor
        """
        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append((nextState, action, cost))

        self._expanded += 1 # DO NOT CHANGE
        return successors


class AgentsSearchProblem(PositionSearchProblem):
    def __init__(self, gameState, agentIndex):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.agents = gameState.getPacmanPositions()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        return state in self.agents

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
            For a given state, this should return a list of triples, (successor,
            action, stepCost), where 'successor' is a successor to the current
            state, 'action' is the action required to get there, and 'stepCost'
            is the incremental cost of expanding to that successor
        """
        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append((nextState, action, cost))

        self._expanded += 1 # DO NOT CHANGE
        return successors