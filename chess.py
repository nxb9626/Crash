import math
from logging import *
import enum

class Piece:
    def __init__(self, team) -> None:
        """
        team should be "0" or "1 #todo update docstring
        """
        self.team = team
    
class Pawn(Piece):
    value = 1
    moves = {}
    def __repr__(self) -> str:
        if self.team == 0:
            return "wP"
        return "bP"

class Bishop(Piece):
    value = 3
    moves = {}
    color = ''
    def __repr__(self) -> str:
        if self.team == 0:
            return "wB"
        return "bB"

class Knight(Piece):
    value = 3
    moves = {}
    color = ''
    def __repr__(self) -> str:
        if self.team == 0:
            return "wK"
        return "bK"

class Rook(Piece):
    value = 5
    moves = {}
    def __repr__(self) -> str:
        if self.team == 0:
            return "wR"
        return "bR"

class Queen(Piece):
    value = 9
    moves = {}
    def __repr__(self) -> str:
        if self.team == 0:
            return "wQ"
        return "bQ"

class King(Piece):
    value = math.inf
    move = {}
    def __repr__(self) -> str:
        if self.team == 0:
            return "wK"
        return "bK"

class Empty():
    def __repr__(self) -> str:
        return "⬛"

class Turn(enum.Enum):
    white = 0
    black = 1

class Move():
    
    def __init__(self,notation):
        self.location = notation[-2:]
        if len(notation)>2:
            self.piece = notation[0]
        else:
            self.piece = ""
        

    def __repr__(self) -> str:
        return str(self.piece) + str(self.location)
    
   


class Board:
    moves = []
    moves_without_caputres = 0
    currentMove = Turn.white
    grid = [
        [Rook(1),   Knight(1),  Bishop(1),  Queen(1),   King(1),    Bishop(1),  Knight(1),  Rook(1)],
        [Pawn(1),   Pawn(1),    Pawn(1),    Pawn(1),    Pawn(1),    Pawn(1),    Pawn(1),    Pawn(1)],
        [Empty(),   Empty(),    Empty(),    Empty(),    Empty(),    Empty(),    Empty(),    Empty()],
        [Empty(),   Empty(),    Empty(),    Empty(),    Empty(),    Empty(),    Empty(),    Empty()],
        [Empty(),   Empty(),    Empty(),    Empty(),    Empty(),    Empty(),    Empty(),    Empty()],
        [Empty(),   Empty(),    Empty(),    Empty(),    Empty(),    Empty(),    Empty(),    Empty()],
        [Pawn(0),   Pawn(0),    Pawn(0),    Pawn(0),    Pawn(0),    Pawn(0),    Pawn(0),    Pawn(0)],
        [Rook(0),   Knight(0),  Bishop(0),  Queen(0),   King(0),    Bishop(0),  Knight(0),  Rook(0)]
        ]

    def is_valid(self, move):
        #check correct player is moving correct piece
        #check is not same player playing twice
        #check is not putting their king in check
        #check is not a draw
        return True
    
    def execute(self, move):
        pass
    
    def printBoard(self):
        # print("Move: "+ str(self.moveCount))
        print('   a  b  c  d  e  f  g  h')
        rows = ['a','b','c','d','e','f','g','h']
        count = 8
        for i in self.grid:
            print(count, end='')
            count -=1
            for j in i:
                print(' ' + str(j), end='')
            print()

    def getSpot():
        pass

    def checkMate():
        return False
        
