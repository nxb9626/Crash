import ui
import chess as ch
import random
import logging
import requests
################################################################################
flip_board = True
WHITE_BOT_URL = 'http://127.0.0.1:5000'
BLACK_BOT_URL = 'http://127.0.0.1:5000'
################################################################################

def logGame(game):
    moves = ""
    for move in game.move_stack:
        moves += move.uci()+" "
    logging.info(str(game.fen()), moves)


def gameLoop(autogame, black_move, white_move):
    game = ch.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    next_turn={ ui.Team.white: ui.Team.black,
            ui.Team.black:ui.Team.white
        }

    current_player = ui.Team.white
    count = 0
    while game.is_game_over() == False:
        # input()
        # clear old board
        # print(chr(27) + "[2J")

        if current_player == ui.Team.white and not autogame:
            move = white_input(game)
        else:
            move = black_input(game.fen())
        print(count)
        # print(game.generate_legal_moves())
        game.push(move) 
        print(move.uci())
        count+=1
        fancyPrint = ui.Board(game)
        fancyPrint.pp()
        # print(game,'\n')
        # print(count)
        # print('Player turn: ', current_player, '\n')
        current_player = next_turn[current_player]

    return "Winner: ", game.result()

def print_move(move,board):
    print(board.piece_at(move.from_square), end='')
    print(str( move)[0:2], end=', ')

def print_move_list(move_list, board):
    for i in move_list:
        print_move(i,board)
    print()

def white_input(fen):
    move = requests.get(WHITE_BOT_URL,json={'fen':fen})
    chosen_move = move.json()['move']
    return ch.Move.from_uci(chosen_move)

def black_input(fen):
    move = requests.get(BLACK_BOT_URL,json={'fen':fen})
    chosen_move = move.json()['move']
    return ch.Move.from_uci(chosen_move)
    # return chosen_move

def user_input(game) -> str:
    move = ch.Move.from_uci(input("Your Move:"))
    return move

def main():
    autogame = True
    b = black_input
    w = white_input
    x = gameLoop(autogame, black_move=b, white_move=w)
    
    print(x[0], {
        '0-1':'Blue', #black
        '1/2-1/2':'stalemate',
        '1-0':'Pink', # white
        '1-1':'tie'
    }[x[1]])



if __name__ == '__main__':    
    while True:
        main()
