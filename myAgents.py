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

        if self.target is not None:
            x, y = self.target
            if not state.hasFood(x, y) and len(self.actions) > 0:
                if self.num > 0:
                    self.actions = []
                    self.target = None
                else:
                    m = state.getNumFood()
                    skip = m // self.pacmanNumber
                    if skip == 0:
                        skip = m - 1
                    problem = SkipFoodSearchProblem(state, self.index, skip)
                    self.actions, self.target = bfs(problem)
        if len(self.actions) > 0:
            action = self.actions[0]
            del self.actions[0]
            return action
        else:
            problem = AnyFoodSearchProblem(state, self.index)
            self.actions, self.target = bfs(problem)
            self.num -= 1
            return self.getAction(state)

    def initialize(self):
        """
        Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank
        """
        "*** YOUR CODE HERE"
        self.num = 4
        self.actions = []
        self.target = None

    def registerInitialState(self, state):
        n = state.getNumAgents()
        self.pacmanNumber = n


"""
Put any other SearchProblems or search methods below. You may also import classes/methods in
search.py and searchProblems.py. (ClosestDotAgent as an example below)
"""

def bfs(problem):
    closed = set([])
    queue = util.Queue()
    queue.push((problem.getStartState(), []))
    while 1:
        if queue.isEmpty():
            return [], None
        current_node = queue.pop()
        current_location = current_node[0]
        current_actions = current_node[1]
        if problem.isGoalState(current_location):
            return current_actions, current_location
        if current_location not in closed:
            closed.add(current_location)
            for successor in problem.getSuccessors(current_location):
                queue.push((successor[0], current_actions + [successor[1]]))


def bfsDepth(problem, depth):
    closed = set([])
    queue = util.Queue()
    queue.push((problem.getStartState(), []))
    res = []
    while 1:
        if queue.isEmpty():
            return res
        current_node = queue.pop()
        current_location = current_node[0]
        current_actions = current_node[1]
        if current_location not in closed:
            if problem.isGoalState(current_location):
                res.append(current_location)
            closed.add(current_location)
            if len(current_actions) == depth:
                continue
            for successor in problem.getSuccessors(current_location):
                queue.push((successor[0], current_actions + [successor[1]]))


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
        if self.food[x][y]:
            if self.skip == 0 and state not in self.skipedFood:
                return True
            if self.skip > 0:
                self.skip -= 1
                self.skipedFood.add(state)
        return False

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
        self.agents = set(gameState.getPacmanPositions())

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