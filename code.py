#!/usr/bin/env python3
"""
Created on Fri Feb 07 11:24:38 2020

@author: ajb0ss

"""

import numpy as np
import random
import math

class GenGameBoard: 
    # Constructor method - initializes each position variable and the board size
    def __init__(self, boardSize):
        self.boardSize = boardSize  # Holds the size of the board
        self.marks = np.empty((boardSize, boardSize),dtype='str')  # Holds the mark for each position
        self.marks[:,:] = ' '

    # Prints the game board using current marks
    def printBoard(self): 
        # Print column numbers
        print(' ',end='')
        for j in range(self.boardSize):
            print(" "+str(j+1), end='')

        # Print rows with marks
        print("")
        for i in range(self.boardSize):
            # Print line separating the row
            print(" ",end='')
            for j in range(self.boardSize):
                print("--",end='')
            
            print("-")

            # Print row number
            print(i+1,end='')
            
            # Print marks on self row
            for j in range(self.boardSize):
                print("|"+self.marks[i][j],end='')
            
            print("|")

        # Print line separating the last row
        print(" ",end='')
        for j in range(self.boardSize):
            print("--",end='')
        
        print("-")

    # Attempts to make a move given the row,col and mark
    # If move cannot be made, returns False and prints a message if mark is 'X'
    # Otherwise, returns True
    def makeMove(self, row, col, mark):
        possible = False  # Variable to hold the return value
        if row==-1 and col==-1:
            return False
        
        # Change the row,col entries to array indexes
        row = row - 1
        col = col - 1
        
        if row<0 or row>=self.boardSize or col<0 or col>=self.boardSize:
            print("Not a valid row or column!")
            return False
        
        # Check row and col, and make sure space is empty
        # If empty, set the position to the mark and change possible to True
        if self.marks[row][col] == ' ':
            self.marks[row][col] = mark
            possible = True    
        
        # Prout the message to the player if the move was not possible
        if not possible and mark=='X':
            print("\nself position is already taken!")
        
        return possible
    
    #Checks if a move is valid or not
    def checkMove(self,row,col):
        possible = False  # Variable to hold the return value
        if row==-1 and col==-1:
            return False
        
        # Change the row,col entries to array indexes
        row = row - 1
        col = col - 1
        
        if row<0 or row>=self.boardSize or col<0 or col>=self.boardSize:
            return False
        
        # Check row and col, and make sure space is empty
        # If empty change possible to True
        if self.marks[row][col] == ' ':
            possible = True   
        
        return possible
        
    # Determines whether a game winning condition exists
    # If so, returns True, and False otherwise
    def checkWin(self, mark):
        won = False # Variable holding the return value
        
        # Check wins by examining each combination of positions
        
        # Check each row
        for i in range(self.boardSize):
            won = True
            for j in range(self.boardSize):
                if self.marks[i][j]!=mark:
                    won=False
                    break        
            if won:
                break
        
        # Check each column
        if not won:
            for i in range(self.boardSize):
                won = True
                for j in range(self.boardSize):
                    if self.marks[j][i]!=mark:
                        won=False
                        break
                if won:
                    break

        # Check first diagonal
        if not won:
            for i in range(self.boardSize):
                won = True
                if self.marks[i][i]!=mark:
                    won=False
                    break
                
        # Check second diagonal
        if not won:
            for i in range(self.boardSize):
                won = True
                if self.marks[self.boardSize-1-i][i]!=mark:
                    won=False
                    break

        return won
    
    # Determines whether the board is full
    # If full, returns True, and False otherwise
    def noMoreMoves(self):
        return (self.marks!=' ').all()

    # def checkEquals(self,str1,str2,str3):
    #     return str1 == str2 and str2 == str3 and str1 != ' '

    #Checks if 2 spots are equal and is not empty
    def checkEquals(self, str1,str2):
        return str1 == str2 and str1 !=' '

    #Function to help with minimax algorithm
    #Checks the state of the board.
    # Returns 
    # +1 if X has won.
    # -1 if O has won.
    # 0 if its a draw.
    # 2 if the game can still continue.

    def checkWinner(self):
        #Initial status set to 2 as game can still continue.
        status = 2

        #Checks if there's a winning postion horizontally
        for i in range(self.boardSize):
            hflag = True
            for j in range(1,self.boardSize):
                if not self.checkEquals(self.marks[i][j-1],self.marks[i][j]):
                    hflag = False
                    break
            if hflag:
                return (1 if 'X' == self.marks[i][j-1] else -1)

        #Checks if there's a winning postion vertically
        for i in range(self.boardSize):
            vflag = True
            for j in range(1,self.boardSize):
                if not self.checkEquals(self.marks[j-1][i],self.marks[j][i]):
                    vflag=False
                    break
            if vflag:
                return (1 if 'X' == self.marks[j-1][i] else -1)
        
        #Checks if there's a winning postion on the main diagonal
        for i in range(1,self.boardSize):
            if not self.checkEquals(self.marks[i][i], self.marks[i-1][i-1]):
                break
            elif i == self.boardSize-1:
                return (1 if 'X' == self.marks[0][0] else -1)

        #Checks if there's a winning postion on the antidiagonal
        temp = self.boardSize
        for i in range(1,self.boardSize):
            if not self.checkEquals(self.marks[i][(temp-1)-i], self.marks[i-1][temp-i]):
                break
            elif i == temp-1:
                return (1 if 'X' == self.marks[0][temp-1] else -1)

        #Checks if there are no more possible moves.
        if self.noMoreMoves():
            return 0
        else:
            return status
        
    #MaxValue function in the minimax algorithm
    def maxValue(self, alpha, beta):
        # checks if there are possible moves
        result = self.checkWinner()
        if result != 2:
            return result
        bestScore = -2
        for i in range(1,boardSize+1):
            for j in range(1,boardSize+1):
                if self.checkMove(i,j):
                    self.marks[i-1][j-1] = 'X'
                    #calls Minvalue function
                    score = self.minValue(alpha, beta)
                    #resets the position
                    self.marks[i-1][j-1] = ' '
                    #Checks if the score was any better than the best score for 1st player and saves the bestscore.
                    bestScore = max(bestScore,score)
                    #Alpha beta pruning for maxValue function
                    if bestScore >= beta:
                        return bestScore
                    if bestScore > alpha:
                        alpha = bestScore
        return bestScore

    #MinValue function in the minimax algorithm
    def minValue(self,alpha,beta):
        # checks if there are possible moves
        result = self.checkWinner()
        if result != 2:
            return result
        bestScore = 2
        for i in range(1,boardSize+1):
            for j in range(1,boardSize+1):
                if self.checkMove(i,j):
                    self.marks[i-1][j-1] = 'O'
                    #calls Maxvalue function
                    score = self.maxValue(alpha, beta)
                    #resets the position
                    self.marks[i-1][j-1] = ' '
                    #Checks if the score was any better than the best score for 2nd player and saves the bestscore.
                    bestScore = min(score,bestScore)
                    #Alpha beta pruning for minValue function
                    if bestScore <= alpha:
                        return bestScore
                    if bestScore < beta:
                        beta = bestScore
        return bestScore

    #This method finds the best possible move for 'O'. ie. The computer! 
    def alphaBetaSearch(self):
        bestScore = 2
        row = -1
        col = -1
        #fetches the score for every possible outcome and finds the move to make.
        for i in range(1,boardSize+1):
            for j in range(1,boardSize+1):
                if self.checkMove(i,j):
                    self.marks[i-1][j-1] = 'O'
                    score = self.maxValue(-2,2)
                    self.marks[i-1][j-1] = ' '
                    if score < bestScore :
                        bestScore = score
                        row = i
                        col = j
        self.makeMove(row,col,'O')
        return

    #This method assists in fetching players position and checking whether it is valid or not
    def playerPrompt(self):
        row, col = -1, -1
        while True:
            print("Player's Move:")
            temp = input("Choose your move (row, column): ")
            row, col = temp.split(',')
            row = int(row)
            col= int(col)
            #checks if a move is valid
            if self.checkMove(row,col):
                self.marks[row-1][col-1] = 'X'
                return
            else:
                print("Invalid move! Try again!") 

print("\nTic-Tac-Toe\n")

LOST = 0
WON = 1
DRAW = 2    
wrongInput = False
boardSize = int(input("Please enter the size of the board n (e.g. n=3,4,5,...): "))
        
# Create the game board of the given size
board = GenGameBoard(boardSize)
        
board.printBoard()  # Print the board before starting the game loop

# Game loop
while True:
    # *** Player's move ***        
    
    # Try to make the move and check if it was possible
    # If not possible get col,row inputs from player
    board.playerPrompt()
    # Display the board again
    board.printBoard()
            
    # Check for ending condition
    # If game is over, check if player won and end the game
    if board.checkWin('X'):
        # Player won
        result = WON
        break
    elif board.noMoreMoves():
        # No moves left -> draw
        result = DRAW
        break         
    # *** Computer's move ***
    print("Computer's Move:\nPlease wait...")
    board.alphaBetaSearch()
    # Print out the board again
    board.printBoard()    
    
    # Check for ending condition
    # If game is over, check if computer won and end the game
    if board.checkWin('O'):
        # Computer won
        result = LOST
        break
    elif board.noMoreMoves():
        # No moves left -> draw
        result = DRAW
        break
        
# Check the game result and print out the appropriate message
print("GAME OVER")
if result==WON:
    print("You Won!")            
elif result==LOST:
    print("You Lost!")
else: 
    print("It was a draw!")
