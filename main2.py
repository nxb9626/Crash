import chess
import chess2
import random
import threading

def pb(board,i='',):
    print(i,chess2.Board(board.fen()))

#random ai example

def randGame(board):
    while board.is_game_over() == False:
        move_list = list(board.legal_moves)
        x = len(move_list)
        if x <= 0:
            break
        x = random.randint(0, len(move_list)-1)
        board.push(move_list[x])
        pb(board,x)
   
    
def main():
    results = {'*':0,'1-0':0,'0-1':0,'1/2-1/2':0}
    i = 0
    count = 1
    while i < count:
        board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        randGame(board)
        results[str(board.result())] += 1
        # print(i)
        i+=1
    # print(results)
    if results['*'] != 0: print('Unfinished', results['*'],(results['*']/count)*100,'%' )
    if results['1-0'] != 0: print('Black', results['1-0'], (results['1-0']/(results['1-0']+results['0-1']))*100,'%' )
    if results['0-1'] != 0: print('White', results['0-1'],(results['0-1']/(results['1-0']+results['0-1']))*100,'%' )
    if results['1/2-1/2'] != 0: print('White', results['1/2-1/2'],(results['1/2-1/2']/count)*100, '%')
    print(random.seed(0))
if __name__ == '__main__':
    main()
