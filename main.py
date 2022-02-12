from chess import Board, Move, Team

################################################################################
flip_board = True
################################################################################

def gameLoop(white,black):
    # game = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    game = Board("rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2 ")
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
        game.pp(flip_board=flip_board)
        # get next move
        move = get_move[game.current_player]()
        if game.is_valid(move):
            game.execute(move)
            # game.moves.append(move)
        else:
            continue
        # log(game.get_inverse_board())

        game.set_current_player(next_turn[game.get_current_player()])

    return "Winner: " + game.get_current_player()

def bot_input():
    pass

def user_input():
    print('Next Move: ', end='')
    try:
        str_note = input().strip().split(' ')
        if str_note[0] == str_note[1]: return user_input()
        return (Move(str_note[0], str_note[1]))
    except KeyboardInterrupt:
        exit()
    except IndexError:
        # print(Exception.with_traceback())
        return user_input()


def main():
    white=0
    black=1
    gameLoop(white, black)


if __name__ == '__main__':    
    main()
