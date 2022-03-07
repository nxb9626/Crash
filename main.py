import ui
import chess as ch
import random
import re
import logging
################################################################################
flip_board = True
################################################################################

def logGame(game):
    moves = ""
    for move in game.move_stack:
        moves += move.uci()+" "
    logging.info(str(game.fen()), moves)

    
    
def gameLoop(white,black):
    game = ch.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    next_turn={ ui.Team.white: ui.Team.black,
            ui.Team.black:ui.Team.white
    }
    # for move in game.move_stack:
        
    

    # get_move={
    #     ui.Team.white:user_input,
    #     ui.Team.black:user_input
    # }
    current_player = ui.Team.white
    count = 0
    while game.is_game_over() == False:
        # clear old board
        print(chr(27) + "[2J")
        fancyPrint = ui.Board(game)
        fancyPrint.pp()
        print('Player turn: ', current_player, '\n')
        # print new board
        # get next move
        # print(list[game.legal_moves])
        # move = input("Move:")
        if current_player == ui.Team.white:
            move = user_input(game)
        else:
            move = bot_input(game.fen())
        # if len(move) <=4 and len(move) >=5 and \
            # ch.Move.from_uci(move) in game.legal_moves:
        game.push(move) 
        # move = get_move[game.current_player]()
        # if game.is_valid(move):
        #     game.execute(move)
        #     # game.moves.append(move)
        # else:
        #     continue
        # log(game.get_inverse_board())
        count+=1
        print(count)

        current_player = next_turn[current_player]

    return "Winner: " + game.result()

def bot_input(fen):
    board = ch.Board(fen)
    move_list = list(board.legal_moves)
    x = len(move_list)
    x = random.randint(0, len(move_list)-1)
    return move_list[x]
    

def user_input(game) -> str:
    # print(list(game.legal_moves))
    move = ch.Move.from_uci(input("Your Move:"))
    # while not re.match(ch, move) and not (move in game.legal_moves):
        # move = str(input("Your Move:"))
    return move
#     print('Next Move: ', end='')
#     try:
#         str_note = input().strip().split(' ')
#         if str_note[0] == str_note[1]: return user_input()
#         return (Move(str_note[0], str_note[1]))
#     except KeyboardInterrupt:
#         exit()
#     except IndexError:
#         # print(Exception.with_traceback())
#         return user_input()


def main():
    white=0
    black=1
    gameLoop(white, black)


if __name__ == '__main__':    
    main()
