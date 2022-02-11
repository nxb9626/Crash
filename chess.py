import math
from logging import *
import enum

black_color = '\033[04m\033[36m' #cyan
white_color = '\033[95m' #pink
reset_color = '\033[0m'

class Piece:
    def __init__(self, team, board) -> None:
        """
        team should be "0" or "1 #todo update docstring
        """
        self.team = team
        # self.position = position
        self.board = board
    # @abc.abstractclassmethod
    # def get_potential_moves(self):
    #     pass
    
class Pawn(Piece):
    value = 1
    past_positions = []
    
    def __repr__(self) -> str:
        if self.team == Team.black:
            return black_color + "P" + reset_color
        return white_color+ "p"+ reset_color
    
    def get_potential_moves(self):
        # positions = []
        # x = self.position[0]
        # y = self.position[1]
        # opponents = []
        # if self.team ==Team.black:
        #     opponents += [1,3]

        #     if len(self.past_positions) == 0:
        #         if(self.board.getSpace((x, y+2)).team == 1 or 
        #             self.board.getSpace((x, y+2)).team == 3):
        #             positions += (x,y+2)

        return 
        
    def add_move(self, move):
        self.moves += move

class Bishop(Piece):
    value = 3
    moves = {}
    def __repr__(self) -> str:
        if self.team == Team.black:
            return black_color + "B"+ reset_color
        return white_color+ "b"+ reset_color

class Knight(Piece):
    value = 3
    moves = {}
    def __repr__(self) -> str:
        if self.team == Team.black:
            return black_color +"N"+ reset_color
        return white_color+ "n"+ reset_color

class Rook(Piece):
    value = 5
    moves = {}
    def __repr__(self) -> str:
        if self.team == Team.black:
            return black_color +"R"+ reset_color
        return white_color+ "r"+ reset_color

class Queen(Piece):
    value = 9
    moves = {}
    def __repr__(self) -> str:
        if self.team == Team.black:
            return black_color +"Q"+ reset_color
        return white_color+ "q"+ reset_color

class King(Piece):
    value = math.inf
    move = {}
    def __repr__(self) -> str:
        if self.team == Team.black:
            return black_color +"K"+ reset_color
        return white_color+ "k"+ reset_color

class Empty():
    def __repr__(self) -> str:
        return " "

class Team(enum.Enum):
    white = 0
    black = 1
    empty = 2

class Move():
    
    def __init__(self, notation):
        self.location = notation[-2:]
        if len(notation)>2:
            self.piece = notation[0]
        else:
            self.piece = ""
        

    def __repr__(self) -> str:
        return str(self.piece) + str(self.location)
    
class Space():
    def __init__(self, pos, piece) -> None:
        self.piece = piece
        self.piece = pos  

    def __repr__(self) -> str:
        return str(self.piece)
    

class Board():
    def __init__(self, fenstring):
        self.moves_without_caputres = 0
        self.grid = [[]]
        pieces = {
            'r':Rook(Team.black,self),
            'n':Knight(Team.black,self),
            'b':Bishop(Team.black,self),
            'q':Queen(Team.black,self),
            'k':King(Team.black,self),
            'p':Pawn(Team.black,self),

            'R':Rook(Team.white,self),
            'N':Knight(Team.white,self),
            'B':Bishop(Team.white,self),
            'Q':Queen(Team.white,self),
            'K':King(Team.white,self),
            'P':Pawn(Team.white,self)
        }
        state = fenstring.split(' ')
        board_string = state[0]
        x = y = 0
        for i in board_string:
            print(i)
            if i == '/':
                x =  0
                y += 1
                self.grid.append([])
            else:
                try:
                    space_count = int(i)
                    for _ in range((space_count)):
                        self.grid[-1].append(Space(Empty(), (x,y)))
                        x += 1
                except(ValueError):
                    self.grid[-1].append(Space(pieces[i], (x,y)))
                

        if state[1] == 'w': self.current_player = Team.white 
        elif state[1] == 'b': self.current_player = Team.black
        
        self.moves = int(state[-1])
        
    def is_valid(self, move):
        #check correct player is moving correct piece
        #check is not same player playing twice
        #check is not putting their king in check
        #check is not a draw
        return True
        
    def get_current_player(self):
        return self.current_player

    def set_current_player(self, next_player):
        self.current_player = next_player

    def execute(self, move):
        pass
    
    def printBoard(self):
        """
        Returns a string representation of the board
        """
        print('  | a | b | c | d | e | f | g | h |')
        print('--|-------------------------------|--')
        count = 8
        for i in self.grid:
            print(str(count), end=' |')
            
            for j in i:
                print('' +' \033[1m' + str(j)+'\033[0m ', end='|')
            print(' '+str(count),'\n--|-------------------------------|--')
            count -=1
        print('  | a | b | c | d | e | f | g | h |')

    def getSpace(self, position):
        return self.board[position[0]][position[1]]
        

    def checkMate():
        return False
        
