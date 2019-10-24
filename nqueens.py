import sys
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

    def set_solving_limit(self,attempt_limit):
        self.attempt_limit = attempt_limit

    def inc_attempt_counter(self):
        self.attempts_to_solve += 1
        
    def setNumberQueens(self, aNumber):
        self.numQueens = int(aNumber)

    def setInitialBoard(self):
        """Generate new board and save it into currentBoard"""
        self.currentBoard = self.generate_new_board()

    def setRandomTarget(self):
        """Set random target queen for moving."""
        randNum = random.randint(0,(self.numQueens-1))
        #print ("Random number generated: " + str(randNum))
        self.targetPiece = self.pieceLocations[randNum]
        self.targetPieceLocation = randNum
        print ("This is the target piece: " + str(self.targetPiece))
        
    def setTotalHeuristic(self):
        """Save total heuristic for current board."""
        totalH = self.generateHeuristic()
        self.totalHeuristic = totalH

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
            aList.append(tempList)
            
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
            pieces = self.pieceLocations.copy()
        
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
        
    def generateHeuristicBoard(self):
        """Generate a Board where every available space/move contains the heuristic if the target piece is moved there."""
        self.heuristicBoard = self.currentBoard.copy()
        print("This is the heuristic board copy:")
        self.printBoard(self.heuristicBoard)

        tempList = self.pieceLocations.copy()
        
        # Generates a new targetLocation list where the target piece is moved to every other location in the board, and its
        # heuristic generated. A new heurisitcBoard is generated for this iteration of currentBoard.
        for x in range(0,self.numQueens):
            for y in range(0,self.numQueens):
                if (self.heuristicBoard[x][y] != "Q"):
                    tempList[self.targetPieceLocation] = (x,y)
                    aHeuristic = self.generateHeuristic(tempList)
                    self.heuristicBoard[x][y] = str(aHeuristic)
                    #print ("This is the new target piece location: " + str(tempList[self.targetPieceLocation]) + "\n" + str(tempList[:]))
                #else:
                    #print ("Queen found in location")
        self.printBoard(self.heuristicBoard)


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
    print("Run: " + str(game_board.attempts_to_solve +1))
    if(solve_method=="hc"):
        print('Hill Climbing:')
    elif(solve_method=='hcwsm'):
        print("Hill Climing With Sideways Movement")
    elif(solve_method=='hcwrr'):
        print("Hill Climbing With Random Restart")
    elif(solve_method=="hcwrrwsm")
        print("Hill Climbing With Random Restart and Random Movement")


def start_program(num_of_queens, attempt_limit):
    analysis_is_ongoing = True
    while(analysis_is_ongoing and game_board.attempts_to_solve < game_board.attempt_limit):
        initialize_board(num_of_queens, attempt_limit)
        


        game_board.inc_attempt_counter()


def main():
    """Main function of program."""

    arg_length = len(sys.argv)

    if(arg_length == 1):
        num_of_queens = get_number_of_queens()
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
