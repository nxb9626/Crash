from chess import Board, Move, Turn
# from logging import *

def gameLoop():
    game = Board()
    currentTurn = Turn.white
    while Board.checkMate() == False:
        print(chr(27) + "[2J")
        game.printBoard()
        move = parseInput(input(), )
        if game.is_valid(move):
            game.execute(move)
            game.moves.append(move)

        print(game.moves)

    return "winner"


def parseInput(str_note):
    return Move(str_note)


def main():
    gameLoop()


if __name__ == '__main__':
    main()
