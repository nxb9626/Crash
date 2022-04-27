import math
from logging import *
import enum
from typing import List

black_color = ''#\033[36m' #cyan
white_color = ''#\033[95m\033[04m' #pink
reset_color = '\033[0m'

class Piece:
    def __init__(self, team, board) -> None:
     
        self.team = team
        self.board = board
    #  ♛ | ♚ | ♝ | ♞ | ♜ | ♟ 
    #  ♕ | ♔ | ♗ | ♘ | ♖ | ♙  
    
class Pawn(Piece):

    def __repr__(self) -> str:
        if self.team != Team.black:
            return black_color + "P" + reset_color
        return white_color+ "p"+ reset_color

class Bishop(Piece):
    def __repr__(self) -> str:
        if self.team != Team.black:
            return black_color + "B"+ reset_color
        return white_color+ "b"+ reset_color

class Knight(Piece):
    def __repr__(self) -> str:
        if self.team != Team.black:
            return black_color +"N"+ reset_color
        return white_color+ "n"+ reset_color

class Rook(Piece):
    
    def __repr__(self) -> str:
        if self.team != Team.black:
            return black_color +"R"+ reset_color
        return white_color+ "r"+ reset_color

class Queen(Piece):

    def __repr__(self) -> str:
        if self.team != Team.black:
            return black_color +"Q"+ reset_color
        return white_color+ "q"+ reset_color

class King(Piece):
    def __repr__(self) -> str:
        if self.team != Team.black:
            return black_color +"K"+ reset_color
        return white_color+ "k"+ reset_color

class Empty():
    """
    ⬛⬜⬛⬜⬛⬜⬛⬜
    """
    def __repr__(self) -> str:
        return " "

class Team(enum.Enum):
    white = 0
    black = 1
    empty = 2

board_to_coord = {
    'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,
    '1':7,'2':6,'3':5,'4':4,'5':3,'6':2,'7':1,'8':0 
}

    
class Space():
    def __init__(self, pos, piece) -> None:
        self.pos = pos  
        self.piece = piece 

    def set_piece(self, p) -> None:
        self.piece = p

    def get_moves(self):
        return self.piece.get_moves(self.pos, self.board)

    def __repr__(self) -> str:
        return str(self.piece)
    

class Board():
    def __init__(self, game) -> None:
        fenstring = game.fen()
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
            # print(i)
            if i == '/':
                x =  0
                y += 1
                self.grid.append([])
            else:
                try:
                    space_count = int(i)
                    for _ in range((space_count)):
                        self.grid[-1].append(Space((x,y), Empty()))
                        x += 1
                except(ValueError):
                    self.grid[-1].append(Space((x,y), pieces[i]))
                

        if state[1] == 'w': self.current_player = Team.white 
        elif state[1] == 'b': self.current_player = Team.black
                
    def get_current_player(self) -> Team:
        return self.current_player

    def set_current_player(self, next_player) -> None:
        self.current_player = next_player
    
    def get_board(self) -> List[list]:
        return self.grid

    def get_inverse_board(self) -> List[list]:
        inverse_board = []        
        for i in self.grid[::-1]:
            inverse_board.append(i[::-1])

        return inverse_board

    def execute(self, move) -> None:
        space1 = self.get_space((move.x1, move.y1))
        space2 = self.get_space((move.x2, move.y2))        
        space2.set_piece(space1.piece)
        space1.set_piece(Empty())
        
    def get_space(self, space) -> Space:
        return self.grid[space[1]][space[0]]
        
    
    def checkMate() -> bool:
        return False

    def pp(self, flip_board=False) -> None:
        print(self.pretty_format_board(flip_board))

    def __repr__(self) -> str:
        return self.pretty_format_board()

    def pretty_format_board(self, flip_b=False) -> str:
        """
        Returns a string representation of the board
        """
        header = "  | a | b | c | d | e | f | g | h |  "
        row_separater = '--+---+---+---+---+---+---+---+---+--'
        out = "\n"

        if self.current_player == Team.black and flip_b:
            gd = self.get_inverse_board() 
            header = header[::-1]
            side_num = {0:1,1:2,2:3,3:4,4:5,5:6,6:7,7:8}
        else:
            gd = self.get_board()
            side_num = {0:8,1:7,2:6,3:5,4:4,5:3,6:2,7:1}

        out += header + '\n'
        out += row_separater + '\n'
        count = 0
        for row in gd: 
            out += str(side_num[count])+' |'
            
            for col in row:
                out += ' \033[1m' + str(col)+'\033[0m |'

            out += ' '+str(side_num[count])+'\n' 
            out += row_separater + '\n'
            
            count +=1
        out += header
        out +='\n'
        return out
        
