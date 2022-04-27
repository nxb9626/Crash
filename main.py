from pprint import pp
import ui
import chess as ch
import random
import logging
import requests
import chess.engine

import bot_server

################################################################################
WHITE_BOT_URL = 'http://127.0.0.1:5000'
BLACK_BOT_URL = 'http://127.0.0.1:5000'
################################################################################

def logGame(game):
    moves = ""
    for move in game.move_stack:
        moves += move.uci()+" "
    logging.info(str(game.fen()), moves)

class FakeMove:
    def uci(self):
        return None

 
def white_input(fen,move:ch.Move,game_depth=0):
    # print("white's move")
    move = requests.get(WHITE_BOT_URL, json={'fen':fen,'move':move})
    chosen_move = move.json()['move']
    # game = ch.Board(fen)
    # x = list(game.legal_moves)
    return ch.Move.from_uci(chosen_move)

def black_input(fen,move:ch.Move,game_depth=0):
    # print("blacks's move")

    move = requests.get(BLACK_BOT_URL, )
    chosen_move = move.json()['move']
    return ch.Move.from_uci(chosen_move)
    # return chosen_move

def bot_input(fen,move:ch.Move,game_depth=0):
    print(fen)
    move = bot_server.bot(request={'fen':fen,'move':move,'smart':False,'move_count':game_depth})

    # chosen_move = move.json()['move']
    return ch.Move.from_uci(move['move'])

def smart_bot_input(fen,move:ch.Move,game_depth=0):
    request={'fen':fen,'move':move,'smart':True,'move_count':game_depth}
    move = bot_server.bot(request=request)
    return ch.Move.from_uci(move['move'])

def gameLoop(fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        black_move=black_input, white_move=white_input):
    game = ch.Board(fen)
    next_turn={ ui.Team.white: ui.Team.black,
            ui.Team.black:ui.Team.white
        }

    current_player = ui.Team.white
    count = 0
    move = FakeMove()
    while game.is_game_over() is False:
        # print(chr(27) + "[2J")
        print("=========================================================")
        print(current_player.name,end="'s next move\n")
        fancyPrint = ui.Board(game)
        fancyPrint.pp()
        # print(game)
        # input()
        # clear old board

        if count%2 == 0:
            move = white_move(game.fen(), move.uci(),count)
        else:
            move = black_move(game.fen(), move.uci(),count)
        # print(count)
        # print(game.generate_legal_moves())

        game.push(move) 
        print(move.uci())
        count+=1
        # fancyPrint = ui.Board(game)
        # fancyPrint.pp()
        # print(game,'\n')
        # print(count)
        # print('Player turn: ', current_player, '\n')
        current_player = next_turn[current_player]
        
    print(current_player.name,end="'s next move\n")
    fancyPrint = ui.Board(game)
    fancyPrint.pp()
    return "Winner: ", game.result()

def print_move(move,board):
    print(board.piece_at(move.from_square), end='')
    print(str(move)[0:2], end=', ')

def print_move_list(move_list, board):
    for i in move_list:
        print_move(i,board)
    print()

def random_input(fen,move,game_depth=0):
    print("random's move")
    return random.choice(list(ch.Board(fen).legal_moves))
    
def user_input(fen,move,game_depth=0) -> ch.Move:
    try:
        move = ch.Move.from_uci(input("Your Move:"))
    except:
        return user_input(fen,move)
    return move

STOCKFISH_ENGINE = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
def stockfish_input(fen,move,game_depth=0)->ch.Move:
    return STOCKFISH_ENGINE.play(ch.Board(fen),chess.engine.Limit(time=.0001)).move


def main():
    fen_1="r1b2b1r/pp3Qp1/2nkn2p/3ppP1p/P1p5/1NP1NB2/1PP1PPR1/1K1R3q w - - 0 1"
    fen_2="kbK5/pp6/1P6/8/8/8/8/R7 b - - 0 1"
    fen_3="8/1Kn1p3/1p5N/4p1q1/4k1N1/3R2p1/Qn2B3/7R w - - 0 1"
    # fen_3 = "1k5r/pP3ppp/3p2b1/1BN1n3/1Q2P3/P1B5/KP3P1P/7q w - - 1 0"
    fen_k="8/1K6/8/1k6/8/8/p7/8 w - - 0 1"

    x = gameLoop( black_move=bot_input, white_move=smart_bot_input)

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
    exit(1)
    # main()
