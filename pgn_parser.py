from numpy import true_divide
import pandas
import re
from pprint import pprint

def parse_moves(line):
    i = 0
    w_moves = []
    b_moves = []
    result = ""
    made_moves = re.sub(r'[^a-zA-Z0-9#://\- ]', '', line).split(' ')
    for move in made_moves:
        if re.match("\d-\d",move):
            result = move
            break
        if i % 3 == 1:
            w_moves.append(str(move))
        elif i % 3 == 2:
            b_moves.append(str(move))
        i+=1

    return w_moves, b_moves, result
        

def read_file_to_dataframe(file_name):
    x = pandas.DataFrame()
    with open(file_name) as file:
        #build dictionary
        piece = {}
        at_moves = False
        for un_formatted_line in file:
            if un_formatted_line=='\n':
                at_moves = True
                continue
            if at_moves:
                moves = parse_moves(un_formatted_line)
                piece['moves'] = moves
            else:
                formatted_line = re.sub(r'[^a-zA-Z1-9 ]', '', un_formatted_line).split(' ', 1)
                try:
                    piece[formatted_line[0]] = formatted_line[1]
                except:
                    print("ERROR: " + str(formatted_line))
        
        pprint(piece)

    return None
            

if __name__ == "__main__":
    file_name = "example.pgn"
    read_file_to_dataframe(file_name=file_name)
