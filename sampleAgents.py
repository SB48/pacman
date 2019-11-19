# sampleAgents.py
# parsons/07-oct-2017
#
# Version 1.1
#
# Some simple agents to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
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

# The agents here are extensions written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
from game import Actions
import api
import random
import game
import util
import unittest

# RandomAgent
#
# A very simple agent. Just makes a random pick every time that it is
# asked for an action.
class RandomAgent(Agent):

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Random choice between the legal options.
        return api.makeMove(random.choice(legal), legal)

# RandomishAgent
#
# A tiny bit more sophisticated. Having picked a direction, keep going
# until that direction is no longer possible. Then make a random
# choice.
class RandomishAgent(Agent):

    # Constructor
    #
    # Create a variable to hold the last action
    def __init__(self):
         self.last = Directions.STOP
    
    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # If we can repeat the last action, do it. Otherwise make a
        # random choice.
        if self.last in legal:
            return api.makeMove(self.last, legal)
        else:
            pick = random.choice(legal)
            # Since we changed action, record what we did
            self.last = pick
            return api.makeMove(pick, legal)

# SensingAgent
#
# Doesn't move, but reports sensory data available to Pacman
class SensingAgent(Agent):

    def getAction(self, state):

        # Demonstrates the information that Pacman can access about the state
        # of the game.

        # What are the current moves available
        legal = api.legalActions(state)
        print "Legal moves: ", legal

        # Where is Pacman?
        pacman = api.whereAmI(state)
        print "Pacman position: ", pacman

        # Where are the ghosts?
        print "Ghost positions:"
        theGhosts = api.ghosts(state)
        for i in range(len(theGhosts)):
            print theGhosts[i]

        # How far away are the ghosts?
        print "Distance to ghosts:"
        for i in range(len(theGhosts)):
            print util.manhattanDistance(pacman,theGhosts[i])

        # Where are the capsules?
        print "Capsule locations:"
        print api.capsules(state)
        
        # Where is the food?
        print "Food locations: "
        print api.food(state)

        # Where are the walls?
        print "Wall locations: "
        print api.walls(state)
        
        # getAction has to return a move. Here we pass "STOP" to the
        # API to ask Pacman to stay where they are.
        return api.makeMove(Directions.STOP, legal)





class MDPAgent(Agent):

    def __init__(self):
        pass

    def buildMap(self, state, directions):
        gameMap = {}
        corners = api.corners(state)
        for x in range(corners[0][0], corners[1][0] +1):
            for y in range(corners[2][0], corners[3][1] +1):
                coord = (x,y)
                gameMap[coord] = (-0.04,0)
        walls = api.walls(state)

        for wall in walls:
            gameMap[wall] = (-1000, 0) 
        largeOrSmall = True
        if corners[1][0] < 10 and corners[3][1] < 10:
            largeOrSmall = False
        return self.updateMap(state, gameMap, directions, largeOrSmall)
    

    def updateMap(self, state, gameMap, directions, largeOrSmall):
        food = api.food(state)
        capsules = api.capsules(state)
        pacman = api.whereAmI(state)
        """
        #method 3 - food reward based on going column by column
        # [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (2, 1), (2, 5), (2, 9), 
        # (3, 1), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 9), (4, 1), (4, 2), (4, 3), (4, 5), (4, 7), 
        # (4, 8), (4, 9), (5, 3), (5, 5), (5, 7), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), 
        # (6, 8), (6, 9), (7, 1), (7, 3), (7, 7), (7, 9), (8, 1), (8, 3), (8, 7), (8, 9), (9, 3), (9, 7), 
        # (9, 9), (10, 1), (10, 3), (10, 7), (10, 9), (11, 1), (11, 3), (11, 7), (11, 9), (12, 1), (12, 3), 
        # (12, 7), (12, 9), (13, 1), (13, 2), (13, 3), (13, 4), (13, 5), (13, 6), (13, 7), (13, 8), (13, 9),
        #  (14, 3), (14, 5), (14, 7), (15, 1), (15, 2), (15, 3), (15, 5), (15, 7), (15, 8), (15, 9), (16, 1), 
        # (16, 3), (16, 4), (16, 5), (16, 6), (16, 7), (16, 9), (17, 1), (17, 5), (17, 9), (18, 2), (18, 3), 
        # (18, 4), (18, 5), (18, 6), (18, 7), (18, 8), (18, 9)]
        1--> 5
        2-->20 10
        3-->30 20

        ...
        9-->90
        10-->1-->10
        """
        
        
        if (largeOrSmall==True):
            for f in food:
                # if f[0] > 9:
                #     foodReward = (f[0]/10)
                #     foodReward = (foodReward * 5) +5
                # else:
                #     foodReward = (f[0] * 5)+5
                foodReward = (f[0] * 5)+5
                gameMap[f] = (foodReward,0)
        else: 
            for f in food:
                gameMap[f] = (10, 0)

        #method 2 - food reward based on distance to pacman
        # if (largeOrSmall==True):
        #     for f in food:
        #         foodDistance = (util.manhattanDistance(pacman,f))
        #         foodReward = (10 / foodDistance)
        #         gameMap[f] = (foodReward, 0)
        #         print food
        # else: 
        #     for f in food:
        #         gameMap[f] = (10, 0)

        #Method 1 = if there's nothing near the food
        # if (largeOrSmall== True) and (len(food) < size[2])
        #     for f in food:
        #         #gameMap[f] = (10, 0)
        #         foodNeighbours = [Actions.getSuccessor(food, move) for move in directions]
        #         empty = 0
        #         for neighbour in foodNeighbours:
        #             empty+= gameMap[neighbour][0]
        #         if empty < 11
        #             gameMap[f] = (20,0)
        for capsule in capsules:
            gameMap[capsule] = (50, 0)
        if largeOrSmall == True: 
            ghostTimer = api.ghostStatesWithTimes(state)
            for ghost in ghostTimer:
                #in case ghost is in location .5
                ghostLoc = (int(round(ghost[0][0])), int(round(ghost[0][1])))
                ghostNeighbours = [Actions.getSuccessor(ghostLoc, move) for move in directions]
                if ghost[1] < 3:
                    if (util.manhattanDistance(pacman,ghostLoc) < 5):
                        #if ghost is 5 away from pacman, set all ghost neighbours reward lower
                        gameMap[ghostLoc] = (-150, 0)
                        for ghostN in ghostNeighbours:
                            gameMap[ghostN] = (-100, 0)
                    else:
                        gameMap[ghostLoc] = (-200, 0) # was 100
                else: # if ghost is edible
                    gameMap[ghostLoc] = (5, 0)
        else:  #if in a smaller grid
            ghosts = api.ghosts(state)
            for ghost in ghosts:
                ghostLoc = (int(round(ghost[0])), int(round(ghost[1])))
                gameMap[ghostLoc] = (-100, 0)
        
        pacman = api.whereAmI(state)
        gameMap[pacman] = (-0.04,0)
        
        return gameMap

    def getOpposite(self, direction):
        if direction == Directions.NORTH:
            return Directions.SOUTH
        elif direction == Directions.SOUTH:
            return Directions.NORTH
        elif direction == Directions.EAST:
            return Directions.WEST
        elif direction == Directions.WEST:
            return Directions.EAST

    #Runs through all neighbours and returns a dictionary of direction pointing to associated utility of new space
    #however if the move is not legal then it will return the utility of position without moving
    def returnExpUtilities(self, directions, position, gameMap):
        directionValues = {}
        for d in directions:
            coord = [Actions.getSuccessor(position, d)][0]
            if coord in gameMap:
                rewardUtility = gameMap[coord]
                if rewardUtility[0]<-999:
                    #if it is a wall, pacman does not move here
                    coord = position
            else: 
                #if it is outside of the map, pacman will not move
                coord = position

            #Using reward not utility, reward is index 0 and utility is index 1
            directionValues[d] = gameMap[coord][1]
        return directionValues

    def calcOptimum(self, state, directions, position, gameMap):
        directionValues = self.returnExpUtilities(directions, position, gameMap)
        greatestMove = [Directions.NORTH, -500, 0]
        legal = api.legalActions(state)
        for move in directions:

            opposite = self.getOpposite(move)

            totalValue = 0
            for (key, value) in directionValues.items():
                if key == opposite:
                    pass
                elif key == move:
                    totalValue += (value*0.8)
                else:
                    totalValue += (value*0.1)
            if totalValue > greatestMove[1]:
                greatestMove[1] = (totalValue)
            if move in legal and totalValue > greatestMove[2]:
                greatestMove[2] = (totalValue)
                greatestMove[0] = move

        return greatestMove

    def valueIteration(self, state, directions, gameMap):
        loop = 0
        loopBreak = True
        discountFactor = 0.9
        while loopBreak == True and loop < 50:
            loop += 1
            gameMapCopy = gameMap.copy()
            for key, value in gameMapCopy.items():
                if value[0] > -999:
                    reward = value[0]
                    #prevous utility initialises at 0
                    prevUtility = value[1]
                    #returns maximum utility move from position
                    optimumPolicy = self.calcOptimum(state, directions, key, gameMapCopy)
                    nextUtilityCalc = discountFactor*optimumPolicy[1]
                    nextUtility = reward + nextUtilityCalc
                    difference = abs(nextUtility - prevUtility)
                    #print difference
                    if difference < 0.05 and difference > 0 and loop > 1:
                        loopBreak = False
                        # print "oof @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
                        # print " "
                    gameMap[key] = (reward, nextUtility)
                    # if key == (2,1) and loop>1:
                    #     print "loop", loop
                    #     print "difference", difference
                    #     print "optimum", optimumPolicy 
                    #     print "prev", prevUtility
                    #     print "next", nextUtility
                    #     print " "
        return gameMapCopy

    
    def getAction(self, state):
        pacman = api.whereAmI(state)
        directions = (Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST)

        gameMap = self.buildMap(state, directions)

        # if not gameMap:
        #     gameMap = self.buildMap(state)
        # else: 
        #     gameMap = self.updateMap(state, gameMap)

        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        #Bellman Equation
        gameMapCopy = self.valueIteration(state, directions, gameMap)
        
        #Once all utilities calculated for all states using Bellman equation, pick nearest neighbour with highest utility
        greatestValue = self.calcOptimum(state, directions, pacman, gameMapCopy)

        # for move in directions:
        #     successor = [Actions.getSuccessor(pacman, d) for d in directions]
        #     #print "successor", successor
        #     #print "ghost", api.ghosts(state)
        #     ghosts = api.ghostStates(state)
        #     ghost0 = ghosts[0]
        #     ghost1 = ghosts[1]
        #     ghost2 = (int(round(ghost0[0])), int(round(ghost0[1])))
        #     ghost3 = (int(round(ghost1[0])), int(round(ghost1[1])))
        #     ghostList = [ghost0, ghost1, ghost2, ghost3]
        #     for ghost in ghostList:
        #         if ghost in successor:
        #             greatestValue = self.calcOptimum(state, directions, pacman, gameMapCopy, True)
        #             print greatestValue
        #             print ""
        #         else:
        #             greatestValue = self.calcOptimum(state, directions, pacman, gameMapCopy, False)

        #print "selecting new move", greatestValue

        #greatestValue returns a direction as well as a value, here we pick the direction
        #print greatestValue
        pick = greatestValue[0] 
        return api.makeMove(pick, legal)    

        


"""
cd C:\Users\sophi\Dropbox\King's\Year3\AI\pacmanApi6FoodAloneChange
python pacman.py --pacman MDPAgent
python pacman.py -q -n 10 -p MDPAgent -l smallGrid
python pacman.py -q -n 5 -p MDPAgent -l mediumClassic
python pacman.py -q -n 10 -p MDPAgent -l mediumClassic
python pacman.py -q -n 20 -p MDPAgent -l mediumClassic
python pacman.py -q -n 10 -p MDPAgent -l smallMDPGrid

python pacman.py --pacman MDPAgent --layout smallMDPGrid
python pacman.py --pacman MDPAgent -l mediumClassic
python pacman.py --pacman MDPAgent --layout smallGrid
python pacman.py --pacman MyGreedyAgent --layout mediumMDPNoGhosts
"""



