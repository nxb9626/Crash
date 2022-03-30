from pprint import pp
import ui
import chess as ch
import random
import logging
import requests
################################################################################
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
        print(current_player.name,end="'s next move\n")
        fancyPrint = ui.Board(game)
        fancyPrint.pp()
        # input()
        # clear old board
        # print(chr(27) + "[2J")

        if current_player == ui.Team.white and not autogame:
            move = white_move(game.fen())
        else:
            move = black_move(game.fen())
        # print(count)
        # print(game.generate_legal_moves())
        game.push(move) 
        # print(move.uci())
        count+=1
        # fancyPrint = ui.Board(game)
        # fancyPrint.pp()
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
    # print("white's move")
    move = requests.get(WHITE_BOT_URL,json={'fen':fen})
    chosen_move = move.json()['move']
    # game = ch.Board(fen)
    # x = list(game.legal_moves)
    return chosen_move

def black_input(fen):
    # print("blacks's move")

    move = requests.get(BLACK_BOT_URL,json={'fen':fen})
    chosen_move = move.json()['move']
    return ch.Move.from_uci(chosen_move)
    # return chosen_move

def random_input(fen):
    print("random's move")
    return random.choice(list(ch.Board(fen).legal_moves))
    
def user_input(game) -> str:
    move = ch.Move.from_uci(input("Your Move:"))
    return move

def main():
    autogame = True
    x = gameLoop(autogame, black_move=black_input, white_move=random_input)
    
    return (x[0], {
        '0-1':'Pink', #black
        '1/2-1/2':'stalemate',
        '1-0':'Blue', # white
        '1-1':'tie'
    }[x[1]])



if __name__ == '__main__':    
    i = 0
    results = []
    while i < 1:
        results.append(main())
        i+=1

    pp(results)
