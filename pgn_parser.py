from itertools import count
from pprint import pp
from pandas import DataFrame
import analysis
import chess.pgn
import chess
import pickle
import signal
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt # 3.5.1
import pandas # 1.4.1

measurements = []
def measure_positions(board:chess.Board, is_good):
    data = analysis.get_piece_counts(board)
    data['w_pieces_count'] = sum({
        data['p'],
        data['r'],
        data['k'],
        data['b'],
        data['q'],
        data['n'],
        }) * is_good
    data['b_pieces_count'] = sum({
        data['P'],
        data['R'],
        data['K'],
        data['B'],
        data['Q'],
        data['N'],
        }) * is_good

    data['check'] = 0
    if board.is_check(): 
        data['check'] = 1 
    data['check'] = data['check'] * is_good

    # data["piece_counts"] =   analysis.get_piece_counts(board), 
    data["legal_moves"]  =   len(list(board.legal_moves)) * is_good
    data["game_depth"]  = len(board.move_stack)
    data['central_control'] = analysis.get_central_squares_control(board) * is_good
    # print('\t',data)
    return data

def measure_game(game:chess.pgn.Game):
    board = game.board()
    results = []
    
    move_count = 0
    for move in x.mainline_moves():
        # print(move_count)
        board.push(move)
        move_count +=1
        if board.turn != chess.WHITE:
            continue

        is_good = -1
        if game.headers['Result'] == '1-0':
            is_good = 1

        score = measure_positions(board, is_good)
        
        # score['result']=won
        # print(score)
        results.append(score)

    return results

def add_plot_data(x, y, x_label="",y_label=""):
    plt.plot(x,y, 'o')
    if x_label != "":
        plt.xlabel(x_label)
    if y_label != "":
        plt.ylabel(y_label)
    return plt
    
if __name__ == "__main__":
    file_name = open("lichess_db_standard_rated_2013-01.pgn")
    measurements = []
    i=0
    x = chess.pgn.read_game(file_name)

    while x is not None:
        if x.headers['Result'] not in {'1-0','0-1'}:
            x = chess.pgn.read_game(file_name)
            continue
        if i > 1000:
            break
        measurements.extend(measure_game(x))
        i+=1
        print(i,"games analyzed")
        x = chess.pgn.read_game(file_name)

    # with open("measurements.obj",'wb') as measurements_file:
    #         pickle.dump(measurements,measurements_file,-1)
    ocd = organized_chess_data = DataFrame(measurements)
    print(organized_chess_data)
    LR = linear_model.LinearRegression()
    # with open("ocd.obj",'wb') as measurements_file:
        # pickle.dump(ocd,measurements_file,-1)
    # y_data = ocd['central_control']
    # x_data = ocd['game_depth']#.drop('legal_moves',axis=1)
    
    # ocd.drop('winner')
    # x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.3, random_state = 37)

    # LR.fit(x_data,y_data)
    # y_pred = LR.predict(x_test)
    # r = r2_score(y_test, y_pred)
    # mse = mean_squared_error(y_test, y_pred)

    # print("r^2:               ", r)
    # print("mean square Error: ", mse)
    # # 5 analyze Coefficients
    # b = LR.intercept_
    # m = LR.coef_
    # print(LR.feature_names_in_)
    # print("Coefficients:      ", m)
    # print("Intercept:         ", b)

    x = 'game_depth'
    y = 'central_control'
    
    plt.plot(ocd[x], ocd[y],'o')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.show()

    
