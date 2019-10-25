import sys
import copy
from pprint import pprint
import random

class NQueenBoard:
    """
    Class that contains all the methods and variables for working with 
    the generated board. 
    
    Variables:
        -numQueens: Number of queens currently on board. It is also the number of
                rows and columns on the board.
        -currentBoard: Generated board which contains all Queens' current location.
        -pieceLocations: X and Y coordinates of all the Queens on the board.
        -targetPiece: Queen that is selected for moving to a new location.
        -targetPieceLocation: location of target piece/Queen on the pieceLocations list.
        -heuristicBoard: Board which contains all the Queens plus the heuristic for moving 
                the target piece/Queen into any other available space on currentBoard.
        -totalHeuristic: Sum of of how many Queens are in contact with another 
                Queen (same row or column)

    Methods:
        -setNumberQueens: Get number of queens for puzzle and assign to numQueens variable.
        -setInitialBoard: Generate new board and save it into currentBoard
        -setRandomTarget: Set random target queen for moving.
        -setTotalHeuristic: Save total heuristic for current board.
        -printBoard: Print board sent as parameter.
        -generateBoard: Generate board based on size entered by user (numQueens variable),
                by going through the rows.
        -generateEmptyRow: Generate a template empty row for generating a new board.
        -generateHeuristic: Generate total heuristic of how many Queens are in 
                contact with another Queen (same row or column).
        -generateHeuristicBoard: Generate a Board where every available space/move 
                contains the heuristic if the target piece is moved there.

    """

    def __init__(self):
        """Initialize class variables."""
        self.numQueens = 0
        self.currentBoard = []
        self.pieceLocations = []
        self.targetPiece = (0,0)
        self.targetPieceLocation = 0
        self.heuristicBoard = []
        self.totalHeuristic = 0
        self.attempts_to_solve = 0
        self.attempt_limit = 0
        self.lowerHeuristic = -1
        self.lowerHeuristicLocation = (0,0)

    def set_solving_limit(self,attempt_limit):
        self.attempt_limit = attempt_limit

    def inc_attempt_counter(self):
        self.attempts_to_solve += 1
        
    def reset_attempt_counter(self):
        self.attempts_to_solve = 0
        
    def setNumberQueens(self, aNumber):
        self.numQueens = int(aNumber)

    def setInitialBoard(self):
        """Generate new board and save it into currentBoard"""
        self.currentBoard = self.generate_new_board()

    def setRandomTarget(self):
        """Set random target queen for moving."""
        randNum = self.targetPieceLocation
        while randNum == self.targetPieceLocation:
            randNum = random.randint(0,(self.numQueens-1))
        #print ("Random number generated: " + str(randNum))
        self.targetPieceLocation = randNum
        self.targetPiece = self.pieceLocations[randNum]
        print ("This is the target piece: " + str(self.targetPiece))
        
    def setTotalHeuristic(self):
        """Save total heuristic for current board."""
        totalH = self.generateHeuristic()
        self.totalHeuristic = totalH
        self.lowerHeuristic = self.totalHeuristic

    def printBoard(self, board):
        # Goes through each row printing all the columns
        for x in range(len(board)):
            print (board[x])
            if (x + 1) % self.numQueens == 0:
                print()
        print("Heuristic Value: %s" %(self.totalHeuristic))
        print("\n")
            
    def generate_new_board(self):
        """Generate board based on size entered by user (numQueens variable),
        by going through the rows."""
        
        aList = []
        random.seed()
        randomY = 0

        for x in range(self.numQueens):
            # Get random location for Queen
            randomY = random.randint(0, (self.numQueens-1))
            tempList = ['-']*self.numQueens #self.generateEmptyRow()
            # Sets Queen in random location in Row.
            tempList[randomY] = "Q"
            tempPosition = (x,randomY)
            # Saves location of piece in pieceLocations
            self.pieceLocations.append(tempPosition)
            print(tempList[:])
            aList.append(tempList[:])
            
        print ("Piece location: " + str(self.pieceLocations[:]))
        return aList
        
    
    def generateEmptyRow(self):
        """Generate a template empty row for generating a new board."""
        aList = []
        for x in range(self.numQueens):
            aList.append("-")
            
        return aList
    
    def generateHeuristic(self, pieces=None):
        """Generate total heuristic of how many Queens are in contact with another Queen (same row or column)."""
        totalH = 0
        
        if (pieces == None):
            #pieces = self.pieceLocations[:]
            pieces = list(self.pieceLocations)
        
        # Run through the pieceLocations array n^2 times, checking if
        # any of the other pieces have the same row or column as tempPiece.
        for t in pieces:
            tempPiece = t
            for x in pieces:
                if (tempPiece != x):
                    # Check if the row or column of t piece is the same as x piece.
                    if (tempPiece[0] == x[0] or tempPiece[1] == x[1]):
                        totalH+=1
        
        return totalH

    def moveToLowerHeuristic(self):
        """Set target piece in best location, and check if this location is final location (puzzle solved)."""

        if (self.totalHeuristic == 0):
            print ("Target piece already in solution location.")
            return False 

        newX = self.lowerHeuristicLocation[0]
        newY = self.lowerHeuristicLocation[1]
        oldX = self.pieceLocations[self.targetPieceLocation][0]
        oldY = self.pieceLocations[self.targetPieceLocation][1]
        
        print ("Moving target piece from (" + str(oldX) +","+ str(oldY) + "); to (" + str(newX) +","+ str(newY) + ")")
        # Move Queen to new location on the board.
        self.currentBoard[oldX][oldY] = "-"
        self.currentBoard[newX][newY] = "Q"
        # Save new location for target Queen on pieceLocations.
        self.pieceLocations[self.targetPieceLocation] =  self.lowerHeuristicLocation
        # Get the new heuristic for the currentBoard.
        self.setTotalHeuristic()
        print ("Updated Board: ")
        self.printBoard(self.currentBoard)
        if self.totalHeuristic == 0:
            # Game has been won, return False, ie. search has stopped and solution is found.
            return False
        
        # Game not finished, return True, ie. search is still ongoing, end hasn't been found.
        return True
        
    def generateHeuristicBoard(self):
        """Generate a Board where every available space/move contains the heuristic if the target piece is moved there."""
        #self.heuristicBoard = self.currentBoard[:]
        self.heuristicBoard = copy.deepcopy(self.currentBoard)
        #print("This is the heuristic board copy:")
        #self.printBoard(self.heuristicBoard)
        
        # If the board is already solved, return True
        if (self.totalHeuristic == 0):
            print ("Board already solved!")
            return True 

        #tempList = self.pieceLocations[:]
        tempList = list(self.pieceLocations)
        lowerHeurFound = False
        lowerHeurLocation = (0,0)
        
        # Generates a new targetLocation list where the target piece is moved to every other location in the board, and its
        # heuristic generated. A new heurisitcBoard is generated for this iteration of currentBoard.
        for x in range(0,self.numQueens):
            for y in range(0,self.numQueens):
                if (self.heuristicBoard[x][y] != "Q"):
                    tempList[self.targetPieceLocation] = (x,y)
                    # Get heuristic from that specific place in the board for target piece.
                    aHeuristic = self.generateHeuristic(tempList)
                    # Assign heuristic in heuristicBoard.
                    self.heuristicBoard[x][y] = str(aHeuristic)
                    # Check if a new lower heuristic was found, ie. a find the best move.
                    if (aHeuristic < self.lowerHeuristic):
                        # If true, save location.
                        lowerHeurFound = True
                        self.lowerHeuristic = aHeuristic
                        self.lowerHeuristicLocation = (x,y)
                    #print ("This is the new target piece location: " + str(tempList[self.targetPieceLocation]) + "\n" + str(tempList[:]))
                #else:
                    #print ("Queen found in location")
        print  ("This is the lowest heuristic found: " + str(self.lowerHeuristic))
        self.printBoard(self.heuristicBoard)
        #self.printBoard(self.currentBoard)
        # Return if a new location was found that is better.
        return lowerHeurFound


def get_number_of_queens():
    aNumber = 0
    while True:
        aNumber = int(input("Enter the number of Queens to be used in this puzzle: "))
        if aNumber > 0:
            break
        else:
            print("Number has to be higher than 0. Enter again >\n")
    return aNumber

def solve_game(game_board, solve_method):
    betterMoveFoundBool = False
    analysis_is_ongoing = True 
    numFailed = []
    numSuccess =[]
    maxSteps = 100
    print("Run: " + str(game_board.attempts_to_solve +1))
    #TODO: stepcounter always in 0. currentboard being pointer to heuristicboard both updating same time.
    if(solve_method=="hc"):
        print('Hill Climbing:')
        while(analysis_is_ongoing): #and game_board.attempts_to_solve < game_board.attempt_limit):
            #stepCounter = 0
            #for i in range(game_board.attempt_limit):
            for i in range(maxSteps):
                betterMoveFoundBool = game_board.generateHeuristicBoard()
                if (betterMoveFoundBool == True):
                    analysis_is_ongoing = game_board.moveToLowerHeuristic()
                    if (analysis_is_ongoing == False):
                        numSuccess.append(i+1) 
                        break
                    elif (i == (maxSteps-1)):
                        # If we are breaking from the for loop and a solution hasn't been found,
                        # and the limit of steps has been reached, add as a failed attempt.
                        game_board.inc_attempt_counter()
                        numFailed.append(i+1)
                        analysis_is_ongoing = False
                else:
                    # Only increase attempts in failure, as in success, we finish.
                    game_board.inc_attempt_counter()
                    numFailed.append(i+1)
                    analysis_is_ongoing = False
                    break
                
    elif(solve_method=='hcwsm'):
        print("Hill Climing With Sideways Movement")
        #TODO: If i reached maxSteps, then add to failed.
        while(analysis_is_ongoing and game_board.attempts_to_solve < game_board.attempt_limit):
            for i in range(maxSteps):
                betterMoveFoundBool = game_board.generateHeuristicBoard()
                if (betterMoveFoundBool == True):
                    analysis_is_ongoing = game_board.moveToLowerHeuristic()
                    if (analysis_is_ongoing == False):
                        numSuccess.append(i+1) 
                        break
                    elif (i == (maxSteps-1)):
                        # If we are breaking from the for loop and a solution hasn't been found,
                        # and the limit of steps has been reached, add as a failed attempt.
                        game_board.inc_attempt_counter()
                        numFailed.append(i+1)
                else:
                    # Only increase attempts in failure, as in success, we finish.
                    game_board.inc_attempt_counter()
                    numFailed.append(i+1)
                    # Get a new target piece to check for possible moves.
                    game_board.setRandomTarget()
                    break
    
    elif(solve_method=='hcwrr'):
        print("Hill Climbing With Random Restart")
        while(analysis_is_ongoing and game_board.attempts_to_solve < game_board.attempt_limit):
            for i in range(maxSteps):
                betterMoveFoundBool = game_board.generateHeuristicBoard()
                if (betterMoveFoundBool == True):
                    analysis_is_ongoing = game_board.moveToLowerHeuristic()
                    if (analysis_is_ongoing == False):
                        numSuccess.append(i+1) 
                        break
                    elif (i == (maxSteps-1)):
                        # If we are breaking from the for loop and a solution hasn't been found,
                        # and the limit of steps has been reached, add as a failed attempt.
                        game_board.inc_attempt_counter()
                        numFailed.append(i+1)
                else:
                    # Only increase attempts in failure, as in success, we finish.
                    game_board.inc_attempt_counter()
                    numFailed.append(i+1)
                    # Create a new board.
                    aBoard.setInitialBoard()
                    aBoard.setRandomTarget()
                    aBoard.setTotalHeuristic()
                    break
    elif(solve_method=="hcwrrwsm"):
        print("Hill Climbing With Random Restart and Random Movement")
        while(analysis_is_ongoing and game_board.attempts_to_solve < game_board.attempt_limit):
            for i in range(maxSteps):
                betterMoveFoundBool = game_board.generateHeuristicBoard()
                if (betterMoveFoundBool == True):
                    analysis_is_ongoing = game_board.moveToLowerHeuristic()
                    if (analysis_is_ongoing == False):
                        numSuccess.append(i+1) 
                        break
                    elif (i == (maxSteps-1)):
                        # If we are breaking from the for loop and a solution hasn't been found,
                        # and the limit of steps has been reached, add as a failed attempt.
                        game_board.inc_attempt_counter()
                        numFailed.append(i+1)
                else:
                    # Only increase attempts in failure, as in success, we finish.
                    game_board.inc_attempt_counter()
                    numFailed.append(i+1)
                    
                    break
    
    print ("====================================================")
    print ("====================================================\n")
    print ("Attempts finished.")
    print ("Number of attempts: " + str(game_board.attempt_limit))
    anAvg = 0
    if (len(numSuccess) > 0):
        print ("Number of attemps succesful: " + str(len(numSuccess)))
        print ("Number of steps for each one: " + str(numSuccess))
        
        for i in range(len(numSuccess)):
            anAvg += numSuccess[0]
        anAvg = anAvg/len(numSuccess)

        print ("Average: " + str(anAvg))
    elif (len(numFailed) > 0):
        print ("Number of attemps failed: " + str(len(numFailed)))
        print ("Number of steps for each one: " + str(numFailed))
        
        for i in range(len(numFailed)):
            anAvg += numFailed[0]
        anAvg = anAvg/len(numFailed)

        print ("Average: " + str(anAvg))
    print ("\n")
    print ("====================================================")
    print ("====================================================")


def start_program(num_of_queens, attempt_limit):
    #analysis_is_ongoing = True
    methods_to_attempt = ["hc", "hcwsm", "hcwrr", "hcwrrwsm"]
    game_board = initialize_board(num_of_queens, attempt_limit)
    for method in methods_to_attempt:
        game_board_copy = copy.deepcopy(game_board)
        solve_game(game_board_copy,method)
        
    #game_board.inc_attempt_counter()


def main():
    """Main function of program."""

    arg_length = len(sys.argv)

    if(arg_length == 1):
        num_of_queens = get_number_of_queens()
        attempt_limit = 5
    elif(arg_length > 1):
        print("Starting Import with the following parameters:\nNumber of Queens: " + str(sys.argv[1]) + "\nNumber of Solving Attempts: "+ str(sys.argv[2]))
        num_of_queens = int(sys.argv[1])
        attempt_limit = int(sys.argv[2])
    else:
        print("Not expecting this type of input")
    start_program(num_of_queens, attempt_limit)

def initialize_board(num_of_queens, attempt_limit):
    aBoard = NQueenBoard()
    aBoard.setNumberQueens(num_of_queens)
    aBoard.set_solving_limit(attempt_limit)
    aBoard.setInitialBoard()
    aBoard.setRandomTarget()
    aBoard.setTotalHeuristic() 
    return aBoard

if __name__ == "__main__":
    main()
