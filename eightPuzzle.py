import queue #used for search algorithm
import itertools #used for tiebreaker between nodes with equal costs, turns it into FIFO for ties
import random #used to select a random index (difficulty) in defaultPuzzlez
'''
0 1 2
3 4 5
6 7 8
'''
defaultPuzzlez = [[1,2,3,4,5,6,7,0,8],
		  [1,2,3,7,4,5,8,0,6],
		  [1,3,6,4,5,2,7,0,8],
		  [4,1,3,0,2,6,7,5,8],
		  [8,6,7,2,5,4,3,0,1],#<- this is is at diameter depth (31)
		  [1,8,2,0,4,3,7,6,5],
		  [3,2,5,1,0,7,4,8,6],
		  [0,1,2,4,5,8,7,6,3],
		  [1,5,6,7,4,2,8,3,0],
		  [4,1,3,7,0,6,5,2,8],
		  [3,5,0,2,1,8,6,4,7],
		  [1,2,3,4,0,6,7,5,8],
		  [7,2,8,4,3,5,0,1,6],
		  [6,4,3,0,5,8,2,1,7],
		  [5,0,8,7,1,4,6,3,2],
		  [7,5,8,6,1,0,3,2,4]] 

#for comparison to goal state
goal = [1,2,3,4,5,6,7,8,0]

#to make priority queue FIFO when there is a tie on priority number
tiebreaker = itertools.count()
nodesExpanded = 0
maxNodesInQueue = 0
goalDepth = 0

def main():
	#prompt user for puzzle choice and store decision
	print("Welcome to Robert Colvin's 8-puzzle solver.")
	puzChoice = input('Type "1" to use a default puzzle, or "2" to enter your own puzzle.\n')
	#randomly pick one of five default puzzles of varying difficulty
	if puzChoice == "1":
		puzzle = defaultPuzzlez[random.randint(0,len(defaultPuzzlez)-1)]
	#if user wants to create puzzle, call function for that
	elif puzChoice == "2":
		puzzle = userGeneratePuzzle()
	else:
		print("Invalid input. Default puzzle inbound.\n")
		puzzle = defaultPuzzlez[random.randint(0,len(defaultPuzzlez)-1)]
	#prompt for algorithm choice
	print("Now, choose your algorithm to solve")
	print("1. Uniform Cost Search")
	print("2. A* with Misplaced Tile heuristic")
	print("3. A* with Manhattan distance heuristic")
	#store algorithm decision
	algChoice = input()
	print("\n")
	
	if algChoice == "1":
		generalSearch(puzzle, algChoice)	
	elif algChoice == "2":
		generalSearch(puzzle, algChoice)
	elif algChoice == "3":
		generalSearch(puzzle, algChoice)
	else:
		print("invalid input, uniform cost search inbound\n")
		generalSearch(puzzle, uniformCost, "1")	

	print("To solve this problem the search algorithm expanded a total of " + str(nodesExpanded) + " nodes")
	print("The maximum number of nodes in the queue at any one time was " + str(maxNodesInQueue))
	print("The depth of the goal was " + str(goalDepth))
	return

#finds where blank is in list
def getBlankIndex(p): 
	for i in range(len(p)):
		if p[i] == 0:
			return i

#takes a puzzle state (list) as parameter, checks if operation can be performed on that state and returns (state after operation, cost of operator) if so
#returns original state if operation is not possible
def moveBlankUp(p, initialCost):
	#set cost in operator functions to keep it general
	cost = 1
	#first check if the blank can be moved up on the simulated square game board
	blankIndex = getBlankIndex(p)
	#if moving the blank up would put it above the board, return the current puzzle state
	if (blankIndex - 3) < 0:
		return (p,cost)
	#else, return a copy of the board where the blank (0) has been swapped with the number above it
	newPuzzle = p.copy()
	newPuzzle[blankIndex] = newPuzzle[blankIndex-3]
	newPuzzle[blankIndex-3] = 0
	return (newPuzzle, cost + initialCost)
	#logic is the same for other moveBlank operators

def moveBlankDown(p, initialCost):
	cost = 1
	blankIndex = getBlankIndex(p)
	if (blankIndex + 3) >= len(p):
		return (p,cost)
	blankIndex = getBlankIndex(p)	
	newPuzzle = p.copy()
	newPuzzle[blankIndex] = newPuzzle[blankIndex+3]
	newPuzzle[blankIndex+3] = 0
	return (newPuzzle, cost + initialCost)

def moveBlankRight(p, initialCost):
	cost = 1
	blankIndex = getBlankIndex(p)
	if (blankIndex % 3) == 2:
		return (p,cost)
	blankIndex = getBlankIndex(p)
	newPuzzle = p.copy()
	newPuzzle[blankIndex] = newPuzzle[blankIndex+1]
	newPuzzle[blankIndex+1] = 0
	return (newPuzzle, cost + initialCost)

def moveBlankLeft(p, initialCost):
	cost = 1
	blankIndex = getBlankIndex(p)
	if (blankIndex % 3) == 0:
		return (p,cost)
	blankIndex = getBlankIndex(p)
	newPuzzle = p.copy()
	newPuzzle[blankIndex] = newPuzzle[blankIndex-1]
	newPuzzle[blankIndex-1] = 0
	return (newPuzzle, cost + initialCost)

#checks if current puzzle state is the goal state
def isGoalState(p):
	if p == goal:
		return True
	return False

#takes a node of form (cost, tiebreaker value, puzzle state) and returns list of tuples of (puzzle states, cost of operator) -- these tuples are not the same type of tuples used in queue
def expand(node):
	expansion = [ moveBlankUp(node[2], node[3]), moveBlankDown(node[2], node[3]), moveBlankRight(node[2], node[3]), moveBlankLeft(node[2], node[3])]
	global nodesExpanded
	nodesExpanded += 1
	return expansion

#takes queue of nodes, list of nodes that were just expanded, and set of visited states
#if states in expansion have never been visited, enqueue them based on operator cost and return new queue
#may not be needed, due to aStar function
def uniformCost(nodes, expansion, visited):
	for state in expansion:
		if tuple(state[0]) not in visited:
			nodes.put( (state[1], next(tiebreaker), state[0]) )

	return nodes

#counts number of tiles not in the correct position, excluding blank (0)
#may not be needed, due to aStar function
def misplacedTile(nodes, expansion, visited): 
	for state in expansion:
		numMisplaced = 0
		for i in range(len(state[0])):
			if (state[0])[i] != i+1:
				if (state[0])[i] != 0:
					numMisplaced += 1
		if tuple(state) not in visited:
			nodes.put( (numMisplaced, next(tiebreaker), state[0]) )

	return nodes
#counts number of tiles not in the correct position, excluding blank (0)
#returns number of misplaced tiles for aStar to use as heuristic
def mt(p):
	numMisplaced = 0
	for i in range(len(p)):
		if p[i] != i+1:
			if p[i] != 0:
				numMisplaced += 1
	return numMisplaced
	
#this code was found at the following URL:
#https://stackoverflow.com/questions/39759721/calculating-the-manhattan-distance-in-the-eight-puzzle
#may not be needed due to aStar function
def manhattanDist(nodes, expansion, visited):
	for state in expansion:
		if tuple(state[0]) not in visited:
			manDist = sum(abs((val-1)%3 - i%3) + abs((val-1)//3 - i//3)
				for i, val in enumerate(state[0]) if val)
			nodes.put( (manDist, next(tiebreaker), state[0]) )

	return nodes

#this code was found at the following URL:
#https://stackoverflow.com/questions/39759721/calculating-the-manhattan-distance-in-the-eight-puzzle
#returns sum of manhattan distances for each puzzle piece for aStar to use as heuristic
def md(p):
	manDist = sum(abs((val-1)%3 - i%3) + abs((val-1)//3 - i//3)
		for i, val in enumerate(p) if val)
	return manDist

#this search algorithm encompasses all three options
def aStar(nodes, expansion, visited, choice):
	#A* combines cost to reach this state with heuristic evaluation so g(n) + h(n)
	#with h(n) = 0 then it reduces to uniform cost search
	hn = 0
	#look at all new states and generate priority number based on user selected algorithms and enqueue node for that state
	#if user selects UCS then priority number is determined in operator functions
	for state in expansion:
		if tuple(state[0]) not in visited:
			gn = state[1]
			if choice == "2":
				hn = mt(state[0])
			elif choice == "3":
				hn = md(state[0])
			nodes.put( (gn + hn, next(tiebreaker), state[0], gn, hn) )
			global maxNodesInQueue
			maxNodesInQueue = max(maxNodesInQueue,nodes.qsize())
	
	return nodes

def generalSearch(p, choice):
	#a queue for nodes to expand
	nodes = queue.PriorityQueue()
	#priority queue containing elements of the pattern (priority_number, tiebreaker, puzzle, g(n), h(n)
	nodes.put((0,-1,p,0,0))
	global maxNodesInQueue 
	maxNodesInQueue= max(maxNodesInQueue,nodes.qsize())
	print("Expanding state")
	#a set for visited nodes because ordering doesn't matter and there is no need for it to hold duplicates
	visited = set()
	#while loop goes forever but actually until queue is empty or goal is found
	while True:
		#if queue ends up empty, we've processed entire tree with no solution found
		if nodes.empty():
			print("Failed -- puzzle unsolvable")
			return 
		#grab node at head of queue
		node = nodes.get()
		print("The best state to expand with a g(n) = " + str(node[3]) + " and h(n) = " + str(node[4]) + " is...")
		printPuzzle(node[2])
		print("Expanding this node...\n")
		#mark this puzzle state as visited
		visited.add(tuple(node[2]))
		#if we've found goal state, notify user and return
		if isGoalState(node[2]):
			print("Goal!!")
			printPuzzle(node[2])
			global goalDepth
			goalDepth = node[3]
			return
#		print("This state is not the goal state\n\n")
		#if there's more nodes and we haven't found goal yet, expand curr node and enqueue using aStar algorithm
		nodes = aStar(nodes, expand(node), visited, choice)

def printPuzzle(puzzle):
	for i in range(len(puzzle)):
		if i % 3 == 0 and i > 0:
			print()
		if puzzle[i] == 0:
			print("b" + " ", end="")
		else:
			print(str(puzzle[i]) + " ", end='')
	print()

def userGeneratePuzzle():
	#prompt for user input
	print("Enter your puzzle, using zero to represent the blank and enter to represent end of a row")
	row1 = input("\nEnter 1st row, with space/tab between numbers\t")
	row2 = input("\nEnter 2nd row, with space/tab between numbers\t")
	row3 = input("\nEnter 3rd row, with space/tab between numbers\t")
	#concatenate all input strings
	p = row1 + " " + row2 + " " + row3
	#split concatenated string into a list and convert all entries to integers
	p = p.split()
	for i in range(len(p)):
		p[i] = int(p[i])

	return p

if __name__ == '__main__':
	main()
