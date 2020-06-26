'''
Nils Napp
Sliding Probelm for AI-Class
'''

import random
import time


class State:
    """ State of sliding number puzzle
        Contains array of values called 'board' to indicate
        tile positions, and the position of tile '0', which
        indicates the empty space on the board.         """

    boardSize = 3

    def __init__(self, s=None):

        if s == None:

            # tiles is an iterator holding numbers 0 to 9
            tiles = range(self.boardSize * self.boardSize).__iter__()

            # below line reads numbers 0-8 stored in tiles and store them in 2d array (list of lists)
            self.board = [[next(tiles) for i in range(self.boardSize)] for j in range(self.boardSize)]

            # keep track of empty position
            self.position = [0, 0]

        else:
            # copy the board
            self.board = []
            for row in s.board:
                self.board.append(list(row))

            # copy the positions
            self.position = list(s.position)

    # converts to readable string to print
    def __str__(self):
        rstr = ''
        for row in self.board:
            rstr += str(row) + '\n'
        return rstr

    # overload to allow comparison of lists and states with ==
    def __eq__(self, other):
        if isinstance(other, State):
            return self.board == other.board
        elif isinstance(other, list):
            return self.board == other
        else:
            return NotImplemented

    # turn into immutable ojbect for set lookup
    def toTuple(self):
        tpl = ()
        for row in self.board:
            tpl += (tuple(row),)
        return tpl

    # create board from a list or tuple
    def setBoard(self, brd):
        self.board = brd
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                if self.board[row][col] == 0:
                    self.position = [row, col]
                    return None
        # raise StandardError('Set board configuration does not have an empy spot!')
        print('Set board configuration does not have an empy spot!')


class Node:
    nodeCount = 0

    def __init__(self, p, a, c, s):

        # keep track of how many nodes were created
        self.__class__.nodeCount += 1
        self.nodeID = self.nodeCount

        self.parent = p
        self.cost = c
        self.action = a
        self.state = s

    # test equivalence Should be state

    def __str__(self):
        rstr = 'NodeID: ' + str(self.nodeID) + '\n'
        if self.parent != None:
            rstr += 'Parent: ' + str(self.parent.nodeID) + '\n'
        if self.action != None:
            rstr += 'Action: ' + self.action + '\n'
        rstr += 'Cost:   ' + str(self.cost) + '\n'
        rstr += 'State:\n' + str(self.state)
        return rstr


# creates and returns a new node which would be child of current node n being passed to the function
def childNode(n, action, problem):
    return Node(n, action, n.cost + 1, problem.apply(action, State(n.state)))


# problem
class Problem:
    """Class that defines a search problem"""

    def __init__(self):
        self.actions = ['U', 'L', 'D', 'R']
        self.initialState = 0
        self.goalState = 0

    def apply(self, a, s):

        # positions after move, still refers to s.position object
        post = s.position

        # make a copy
        pre = list(post)

        # compute post position
        if a == 'U':
            post[0] = max(pre[0] - 1, 0)
        elif a == 'L':
            post[1] = max(pre[1] - 1, 0)
        elif a == 'D':
            post[0] = min(pre[0] + 1, s.boardSize - 1)
        elif a == 'R':
            post[1] = min(pre[1] + 1, s.boardSize - 1)
        else:
            print('Undefined action: ' + str(a))
            # raise StandardError('Action not defined for this problem!')
            print('Action not defined for this problem!')

        # store the old tile to slide/swap the tiles
        tile = s.board[pre[0]][pre[1]]

        s.board[pre[0]][pre[1]] = s.board[post[0]][post[1]]
        s.board[post[0]][post[1]] = tile

        #       print (pre, ' ', post,' ',s.board[pre[0]][pre[1]] , '<--', s.board[post[0]][post[1]])

        return s

    def applicable(self, s):
        actionList = []

        # check if actions are applicable
        # Not in top row
        if s.position[0] > 0:
            actionList.append('U')

        # not in left most col
        if s.position[1] > 0:
            actionList.append('L')

        # not in bottom row
        if s.position[0] < (s.boardSize - 1):
            actionList.append('D')

        # not in right col
        if s.position[1] < (s.boardSize - 1):
            actionList.append('R')

        return actionList

    # test if currect state is goal state or not
    def goalTest(self, s):
        return self.goalState == s


def applyRndMoves(numMoves, s, p):
    for i in range(numMoves):
        p.apply(p.actions[random.randint(0, 3)], s)


def solution(node):
    ''' Returns actionList, cost of the solution generated from the node'''

    actions = []
    cost = node.cost

    while node.parent != None:
        actions.insert(0, node.action)
        node = node.parent

    return actions, cost


class Searches:

    def BFS(self, problem):
        root = Node(None, None, 0, problem.initialState)
        queue = []
        visited = []
        visited.append((root.state))
        queue.append(root)
        while len(queue) > 0:
            n = queue.pop(0)
            if problem.goalTest(n.state):
                return solution(n)
            else:
                appl = problem.applicable(n.state)
                for i in range(len(appl)):
                    p = childNode(n, appl[i], problem)
                    if p.state not in visited:
                        visited.append(p.state)
                        queue.append(p)
        return "FAILED TO FIND PATH"
        # WRITE YOUR CODE HERE

    def DFS(self, problem):
        root = Node(None, None, 0, problem.initialState)
        stack = []
        stateStack = set(())
        visited = set(())
        stack.append(root)
        stateStack.add(str(root.state))
        while len(stack) > 0:
            n = stack.pop(-1)
            visited.add(str(n.state))
            stateStack.remove(str(n.state))
            if problem.goalTest(n.state):
                return solution(n)
            appl = problem.applicable(n.state)
            for i in range(len(appl)):
                p = childNode(n, appl[i], problem)
                if problem.goalTest(p.state):
                    return solution(p)
                if not (str(p.state) in visited or str(p.state) in stateStack):
                    stack.append(p)
                    stateStack.add(str(p.state))
        return "FAILED TO FIND PATH"
# WRITE YOUR CODE HERE


if __name__ == '__main__':
    print("TEST")

    search = Searches()
    p = Problem()
    s = State()

    p.goalState = State(s)

    p.apply('R', s)
    p.apply('R', s)
    p.apply('D', s)
    p.apply('D', s)
    p.apply('L', s)

    p.initialState = State(s)

    print("Initial State \n", p.initialState)

### Uncommnet for testing BFS solution

    print('=== BFS  ===')
    startTime = time.clock()
    res=search.BFS(p)
    print(res)
    print("Time " + str(time.clock() - startTime))
    print("Explored Nodes: " + str(Node.nodeCount))


    print("Generating Random Position")
    si = State(s)
    applyRndMoves(15,si,p)
    p.initialState = si
    print(si)

    startTime = time.clock()

    print('=== BFS  ===')
    startTime = time.clock()
    res=search.BFS(p)
    print(res)
    print("Time " + str(time.clock() - startTime))
    print("Explored Nodes: " + str(Node.nodeCount))


### Uncommnet for testing DFS solution


    print(p.initialState)


    print('=== DFS  ===')
    startTime = time.clock()
    res = search.DFS(p)
    print(res)
    print("Time " + str(time.clock() - startTime))
    print("Explored Nodes: " + str(Node.nodeCount))


    print("Generating Random Position")
    si = State(s)
    applyRndMoves(15,si,p)
    p.initialState=si
    print(si)

    startTime = time.clock()

    print('=== DFS  ===')
    startTime = time.clock()
    res = search.DFS(p)
    print(res)
    print("Time " + str(time.clock() - startTime))
    print("Explored Nodes: " + str(Node.nodeCount))


