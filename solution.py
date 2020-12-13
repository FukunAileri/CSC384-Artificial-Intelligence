#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os #for time functions
from search import * #for search engines
from sokoban import SokobanState, Direction, PROBLEMS #for Sokoban specific classes and problems

def sokoban_goal_state(state):
  '''
  @return: Whether all boxes are stored.
  '''
  for box in state.boxes:
    if box not in state.storage:
      return False
  return True

def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #We want an admissible heuristic, which is an optimistic heuristic.
    #It must never overestimate the cost to get from the current state to the goal.
    #The sum of the Manhattan distances between each box that has yet to be stored and the storage point nearest to it is such a heuristic.
    #When calculating distances, assume there are no obstacles on the grid.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.

    #basic manhattan distance
    hval = 0
    for box in state.boxes:
        mindist = state.height * state.width
        for goals in state.storage:
            if abs(box[0] - goals[0]) + abs(box[1] - goals[1]) < mindist:
                mindist = abs(box[0] - goals[0]) + abs(box[1] - goals[1])
        hval += mindist
    return hval


#SOKOBAN HEURISTICS
def trivial_heuristic(state):
  '''trivial admissible sokoban heuristic'''
  '''INPUT: a sokoban state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
  count = 0
  for box in state.boxes:
    if box not in state.storage:
        count += 1
  return count

def heur_alternate(state):
#IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #heur_manhattan_distance has flaws.
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.

    #manhattan distance
    hval = 0

    # later use for when box stuck on a wall, check if a storage is there
    upwall = False
    downwall = False
    leftwall = False
    rightwall = False
    completegoal = []
    for goals in state.storage:
        completegoal.append(False)

    for box in state.boxes:
        mindist = state.height * state.width
        robotdist = 0
        counter = 0
        for goals in state.storage:
            if (goals[1]+1 == state.height):
                upwall = True
            if (goals[1] - 1 == -1):
                downwall = True
            if (goals[0] + 1 == state.width):
                rightwall = True
            if (goals[0] - 1 == -1):
                leftwall = True

            if completegoal[counter] == True:
                counter += 1
                continue

            if abs(box[0] - goals[0]) + abs(box[1] - goals[1]) < mindist:
                mindist = abs(box[0] - goals[0]) + abs(box[1] - goals[1])

            if abs(box[0] - goals[0]) + abs(box[1] - goals[1]) == 0:
                completegoal[counter] = True

            counter += 1


        #if a box isn't in the goal, the robot has to be beside it to push it
        if mindist != 0:

            #check if stuck in corner
            updownblock = (((box[0], box[1]+1) in state.obstacles) or ((box[0], box[1]-1) in state.obstacles) or
                           (box[1]-1 == -1) or (box[1]+1 == state.height))
            leftrightblock = (((box[0]+1, box[1]) in state.obstacles) or ((box[0]-1, box[1]) in state.obstacles) or
                              (box[0]+1 == state.width) or (box[0]-1 == -1))
            if updownblock and leftrightblock:
                return float("inf")

            #check if stuck on wall and no storage on it or 2 boxes together
            #up
            upedge = box[1]+1 == state.height
            if (((box[0], box[1]+1) in state.obstacles) or upedge):
                if ((((box[0]+1, box[1]) in state.boxes) and (((box[0]+1, box[1]+1) in state.obstacles)or upedge)
                ) or (((box[0]-1, box[1]) in state.boxes) and (((box[0]-1, box[1]+1) in state.obstacles)or upedge))):
                    return float("inf")
                if upedge:
                    if upwall == False:
                        return float("inf")
            #down
            downedge = box[1]-1 == -1
            if (((box[0], box[1]-1) in state.obstacles) or downedge):
                #if (((box[0]+1, box[1]) in state.boxes) or ((box[0]-1, box[1]) in state.boxes)):
                if ((((box[0] + 1, box[1]) in state.boxes) and (
                        ((box[0] + 1, box[1] - 1) in state.obstacles) or downedge)
                ) or (((box[0] - 1, box[1]) in state.boxes) and (
                        ((box[0] - 1, box[1] - 1) in state.obstacles) or downedge))):
                    return float("inf")
                if downedge:
                    if downwall == False:
                        return float("inf")
            #right
            rightedge = box[0]+1 == state.width
            if (((box[0]+1, box[1]) in state.obstacles) or rightedge):
                #if (((box[0], box[1]+1) in state.boxes) or ((box[0], box[1]-1) in state.boxes)):
                if ((((box[0], box[1]+1) in state.boxes) and (
                        ((box[0] + 1, box[1] + 1) in state.obstacles) or rightedge)
                ) or (((box[0], box[1]-1) in state.boxes) and (
                        ((box[0] + 1, box[1] - 1) in state.obstacles) or rightedge))):
                    return float("inf")
                if rightedge:
                    if rightwall == False:
                        return float("inf")
            #left
            leftedge = box[0]-1 == -1
            if (((box[0]-1, box[1]) in state.obstacles) or leftedge):
                #if (((box[0], box[1]+1) in state.boxes) or ((box[0], box[1]-1) in state.boxes)):
                if ((((box[0], box[1] + 1) in state.boxes) and (
                        ((box[0] - 1, box[1] + 1) in state.obstacles) or leftedge)
                ) or (((box[0], box[1] - 1) in state.boxes) and (
                        ((box[0] - 1, box[1] - 1) in state.obstacles) or leftedge))):
                    return float("inf")
                if leftedge:
                    if leftwall == False:
                        return float("inf")

            robotdist = state.height * state.width
            for robot in state.robots:
                if abs(robot[0] - box[0]) + abs(robot[1] - box[1]) < robotdist:
                    robotdist = abs(robot[0] - box[0]) + abs(robot[1] - box[1]) - 1
                    if abs(robot[0] - box[0]) == 1 and abs(robot[1] - box[1]) == 1:
                        robotdist = abs(robot[0] - box[0]) + abs(robot[1] - box[1]) - 2
        hval += mindist + robotdist
    return hval

def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return sN.gval + weight * sN.hval

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
#IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''
    timebound = timebound - 0.05
    inittime = os.times()[0]
    # initiate search engine
    se = SearchEngine('custom', 'full')
    wrapped_fval_function = (lambda sN : fval_function(sN,weight))
    se.init_search(initial_state, goal_fn=sokoban_goal_state, heur_fn=heur_fn, fval_function=(wrapped_fval_function))

    endtime = os.times()[0]
    remainder = timebound - (endtime - inittime)

    # search
    endstate = se.search(timebound=remainder)
    endtime = os.times()[0]
    remainder = timebound - (endtime - inittime)

    # check if no solution found
    if endstate == False:
        return False

    # while search doesn't exceed the timebound, continue searching until a search exceeds it
    while remainder > 0:
        # check if new end state found a better solution, if so, replace endstate
        costbound = endstate.gval
        #from fval function, this costbound has become the fval
        newend = se.search(timebound=remainder, costbound=(float("inf"), float("inf"), costbound))

        if newend == False:
            return endstate
        else:
            endtime = os.times()[0]
            remainder = timebound - (endtime - inittime)
            endstate = newend
            weight = weight - (weight/20)

    return endstate

def anytime_gbfs(initial_state, heur_fn, timebound = 10):
#IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''
    timebound = timebound - 0.05
    inittime = os.times()[0]
    #initiate search engine
    se = SearchEngine('best_first', 'full')
    se.init_search(initial_state, goal_fn=sokoban_goal_state, heur_fn=heur_fn)

    endtime = os.times()[0]
    remainder = timebound - (endtime - inittime)

    #search
    endstate = se.search(timebound=remainder)
    endtime = os.times()[0]

    #check if no solution found
    if endstate == False:
        return endstate

    #while search doesn't exceed the timebound, continue searching until a search exceeds it
    remainder = timebound - (endtime - inittime)
    while remainder > 0:
        #check if new end state found a better solution, if so, replace endstate
        costbound = endstate.gval
        newend = se.search(timebound=remainder, costbound=(costbound, float("inf"), float("inf")))

        if newend == False:
            return endstate
        else:
            endtime = os.times()[0]
            remainder = timebound - (endtime - inittime)
            endstate = newend

    return endstate
