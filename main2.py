import chess
import ui
import random
import logging

def pb(board,i='',):
    print(i,ui.Board(board))

def logGame(game):
    moves = ""
    for move in game.move_stack:
        moves += str(move.uci())+" "
    logging.info(game.fen())
    logging.debug(moves)

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

#random ai example

def randGame(board):
    while board.is_game_over() == False:
        move_list = list(board.legal_moves)
        x = len(move_list)
        if x <= 0:
            break
        x = random.randint(0, len(move_list)-1)
        board.push(move_list[x])
    logGame(board)
    return (len(board.move_stack))
    
def main():
    results = {' * ':0,'1-0':0,'0-1':0,'1/2-1/2':0}
    i = 0
    count = 1000
    total_boards_looked_at = 0
    while i < count:
        board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        total_boards_looked_at += randGame(board)
        results[str(board.result())] += 1
        # print(i)
        i+=1
    results['1/2'] = results['1/2-1/2']
    results.pop('1/2-1/2')
    # if results['*'] != 0: print('Unfinished', results['*'],(results['*']/count)*100,'%' )
    # if results['1-0'] != 0: print('Black', results['1-0'], (results['1-0']/(results['1-0']+results['0-1']))*100,'%' )
    # if results['0-1'] != 0: print('White', results['0-1'],(results['0-1']/(results['1-0']+results['0-1']))*100,'%' )
    # if results['1/2-1/2'] != 0: print('Draw', results['1/2-1/2'],(results['1/2-1/2']/count)*100, '%')
    # print(random.seed(0))
    print("total boards looked at", total_boards_looked_at)
    [print(f'{k}: {results[k]} {(results[k]/count)*100}') for k in results if results[k] != 0]
if __name__ == '__main__':
    main()
