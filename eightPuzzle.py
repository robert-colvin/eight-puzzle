import queue #used for search algorithm
import itertools #used for tiebreaker between nodes with equal costs, turns it into FIFO for ties
'''
0 1 2
3 4 5
6 7 8
'''
defaultPuzzle = [[1,2,3],
		 [4,5,6],
		 [7,0,8]]

defaultPuzzle2 = [1,2,3,4,5,6,7,0,8]

goal = [1,2,3,4,5,6,7,8,0]
tiebreaker = itertools.count()
def main():
	#prompt user for puzzle choice and store decision
	print("Welcome to Robert Colvin's 8-puzzle solver.")
	puzChoice = input('Type "1" to use a default puzzle, or "2" to enter your own puzzle.\n')
	if puzChoice == "1":
		puzzle = defaultPuzzle2
	#if user wants to create puzzle, call function for that
	elif puzChoice == "2":
		puzzle = userGeneratePuzzle2()
	#else statement for the jerks
	else:
		print("Invalid input. Default puzzle inbound.\n")
		puzzle = defaultPuzzle2

	#prompt for algorithm choice
	print("Now, choose your algorithm to solve")
	print("1. Uniform Cost Search")
	print("2. A* with Misplaced Tile heuristic")
	print("3. A* with Manhattan distance heuristic")
	algChoice = input()
	
	if algChoice == "1":
		generalSearch(puzzle, uniformCost)
	
	elif algChoice == "2":
		generalSearch(puzzle, misplacedTile)
	elif algChoice == "3":
		generalSearch(puzzle, manhattanDist)
	else:
		print("invalid input, uniform cost search inbound\n")
		generalSearch(puzzle, uniformCost)	
	return
def getBlankIndex(p):
	for i in range(len(p)):
		if p[i] == 0:
			return i

def moveBlankUp(p):
	#first check if the blank can be moved up on the simulated square game board
	blankIndex = getBlankIndex(p)
	#if moving the blank up would put it above the board, return the current puzzle state
	if (blankIndex - 3) < 0:
		return p
	#else, return a copy of the board where the blank (0) has been swapped with the number above it
	newPuzzle = p.copy()
	newPuzzle[blankIndex] = newPuzzle[blankIndex-3]
	newPuzzle[blankIndex-3] = 0
	return newPuzzle
	#logic is the same for other moveBlank operators

def moveBlankDown(p):
	if (blankIndex + 3) > len(p):
		return p
	blankIndex = getBlankIndex(p)
	
	newPuzzle = p.copy()
	newPuzzle[blankIndex] = newPuzzle[blankIndex+3]
	newPuzzle[blankIndex+3] = 0
	return newPuzzle

def moveBlankRight(p):
	if (blankIndex % 3) == 2:
		return p
	blankIndex = getBlankIndex(p)
	newPuzzle = p.copy()
	newPuzzle[blankIndex] = newPuzzle[blankIndex+1]
	newPuzzle[blankIndex+1] = 0
	return newPuzzle

def moveBlankLeft(p):
	if (blankIndex % 3) == 0:
		return p
	blankIndex = getBlankIndex(p)
	newPuzzle = p.copy()
	newPuzzle[blankIndex] = newPuzzle[blankIndex-1]
	newPuzzle[blankIndex-1] = 0
	return newPuzzle

def isGoalState(p):
	if p == [[1,2,3],[4,5,6],[7,8,0]]:
		return True
	return False

def isGoalState2(p):
	if p == [1,2,3,4,5,6,7,8,0]:
		return True
	return False

#takes a node of form (value, puzzle state) and returns list of puzzle states (not nodes) for each operator
def expand(node):
	expansion = [moveBlankUp(node[1]),moveBlankDown(node[1]),moveBlankRight(node[1]),moveBlankLeft(node[1])]
	return expansion

		

def uniformCost(nodes, expansion):
	for state in expansion:
		nodes.put((1,state))

	return nodes

#counts number of tiles not in the correct position, excluding blank (0)
def misplacedTile(p): 
	numMisplaced = 0
	for i in range(len(p)):
		if p[i] != i+1:
			if p[i] != 0:
				numMisplaced += 1
	return numMisplaced

#this code was found at the following URL:
#https://stackoverflow.com/questions/39759721/calculating-the-manhattan-distance-in-the-eight-puzzle
def manhattanDist(p):
	manDist = sum(abs((val-1)%3 - i%3) + abs((val-1)//3 - i//3)
		for i, val in enumerate(p) if val)

	return manDist


def generalSearch(p, queueingFunc):
	#a queue for nodes to expand
	nodes = queue.PriorityQueue()
	#priority queue containing elements of the pattern (priority_number, tiepuzzle)
	nodes.put((0,-1,p)
	#a set for visited nodes because ordering doesn't matter and there is no need for it to hold duplicates
	visited = set()
	while True:
		if nodes.empty():
			return "failure"
		node = nodes.get()
		visited.add(node[2])
		if isGoalState(node):
			return node
		nodes = queueingfunc(nodes, expand(node))

#this function is directly copied from sample report
def printPuzzle(puzzle):
	for i in range(3):
		print(puzzle[i])
	print('\n')
def printPuzzle2(puzzle):
	for i in range(len(puzzle)):
		if i % 3 == 0:
			print()
		print(str(puzzle[i]) + " ", end='')
	print('\n')

def userGeneratePuzzle2():
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
def userGeneratePuzzle():
	#prompt for user input
	print("Enter your puzzle, using zero to represent the blank and enter to represent end of a row")
	row1 = input("\nEnter 1st row, with space/tab between numbers\t")
	row2 = input("\nEnter 2nd row, with space/tab between numbers\t")
	row3 = input("\nEnter 3rd row, with space/tab between numbers\t")
	#split each input string into string lists
	row1 = row1.split()
	row2 = row2.split()
	row3 = row3.split()
	#turn string lists into int lists, assuming totally valid input
	for i in range(3):
		row1[i] = int(row1[i])
		row2[i] = int(row2[i])
		row3[i] = int(row3[i])

	return [row1, row2, row3]

if __name__ == '__main__':
	main()
