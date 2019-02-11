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

        if 'actionIndex' not in dir(self):
            self.actionIndex = 0
            problem = AnyFoodSearchProblem(state, self.index)
            search_result = uniformCostSearch(problem)
            self.actions = search_result[0]
            self.target = search_result[1]

        if self.target[0] == -1:
            return Directions.STOP

        '''
        if not state.getFood()[self.target[0]][self.target[1]]:
            problem = AnyFoodSearchProblem(state, self.index)
            search_result = uniformCostSearch(problem)
            self.actions = search_result[0]
            self.target = search_result[1]
            self.actionIndex = 0
        '''

        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            problem = AnyFoodSearchProblem(state, self.index)
            search_result = uniformCostSearch(problem)
            self.actions = search_result[0]
            self.target = search_result[1]
            self.actionIndex = 1
            return self.actions[0]

        # raise NotImplementedError()

    def initialize(self):
        """
        Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank
        """
        "*** YOUR CODE HERE"
        # raise NotImplementedError()


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
        self.agents = gameState.getPacmanPositions()
        self.index = agentIndex
        # self.width = gameState.getWidth()
        # self.height = gameState.getHeight()
        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.costFn = self.getCostOfAction
        self.startState = gameState.getPacmanPosition(agentIndex)
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x, y = state
        return self.food[x][y]
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
        for action in [Directions.NORTH, Directions.WEST, Directions.EAST, Directions.SOUTH]:
            x, y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState, action)
                successors.append((nextState, action, cost))

        self._expanded += 1 # DO NOT CHANGE
        return successors

    def getCostOfAction(self, state, action):
        x, y = state

        if (x, y) in self.agents:
            return 30

        if action == Directions.NORTH:
            return len([agent for agent in self.agents if agent[1] > y]) + 1
            # return len([agent for agent in self.agents if agent[1] > y and abs(agent[0] - x) <= self.width // 5]) + 1
        elif action == Directions.SOUTH:
            return len([agent for agent in self.agents if agent[1] < y]) + 1
            # return len([agent for agent in self.agents if agent[1] < y and abs(agent[0] - x) <= self.width // 5]) + 1
        elif action == Directions.WEST:
            return len([agent for agent in self.agents if agent[0] < x]) + 1
            # return len([agent for agent in self.agents if agent[0] < x and abs(agent[1] - y) <= self.height // 5]) + 1
        elif action == Directions.EAST:
            return len([agent for agent in self.agents if agent[0] > x]) + 1
            # return len([agent for agent in self.agents if agent[0] > x and abs(agent[1] - y) <= self.height // 5]) + 1
        '''
        if action == Directions.NORTH:
            return len([agent for agent in self.agents if agent[1] > y]) + 1
        elif action == Directions.SOUTH:
            return len([agent for agent in self.agents if agent[1] < y]) + 1
        elif action == Directions.WEST:
            return len([agent for agent in self.agents if agent[0] < x]) + 1
        elif action == Directions.EAST:
            return len([agent for agent in self.agents if agent[0] > x]) + 1
        '''


def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    closed = []
    p_queue = util.PriorityQueue()
    p_queue.push((problem.getStartState(), [], 0), 0)
    # total = 0
    while 1:
        if p_queue.isEmpty():
            return [Directions.STOP], (-1, -1)
        current_node = p_queue.pop()
        current_location = current_node[0]
        current_actions = current_node[1]
        current_cost = current_node[2]

        if problem.isGoalState(current_location):
            return current_actions, current_location
        if current_location not in closed:
            closed.append(current_location)
            for successor in problem.getSuccessors(current_location):
                p_queue.push((successor[0], current_actions + [successor[1]], current_cost + successor[2]),
                             current_cost + successor[2])
                # total += 1
                # if total > 1000:
                #    return [Directions.STOP], (-1, -1)
