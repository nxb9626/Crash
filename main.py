from chess import Board, Move, Team
# from logging import *

def gameLoop(white,black):
    game = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    next_turn={ Team.white:Team.black,
            Team.black:Team.white
    }

    get_move={
        Team.white:user_input,
        Team.black:user_input
    }

    while Board.checkMate() == False:
        # clear old board
        print(chr(27) + "[2J")
        print('Player turn: ', game.get_current_player(), '\n')
        # print new board
        game.printBoard()
        print('Next Move: ', end='')
        # get next move
        move = get_move[game.current_player]()
        if game.is_valid(move):
            game.execute(move)
            # game.moves.append(move)
        else:
            continue
        print(game.moves)
        game.set_current_player(next_turn[game.get_current_player()])

    return "Winner: " + game.get_current_player()

def bot_input():
    pass

def user_input():
    str_note = input()
    return Move(str_note)



def main():
    white=0
    black=1
    gameLoop(white, black)


if __name__ == '__main__':
    main()
