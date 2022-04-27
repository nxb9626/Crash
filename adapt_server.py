"""
Runs an adaptation server, which receives data from the bot and determines if 
changes should be made for its decision making
"""
import pickle
import chess
import math
# from flask import Flask, request
# app = Flask(__name__)

with open("ocd.obj",'rb') as measurements_file:
    names, m, b = pickle.load(measurements_file)
    print(names)
    print(m)



def adapt(scores,weights):
    """
    responds to a get request with json
    with the next move to be made by the bot
    """
    moves = weights['move_count'] + weights['max_depth']
################################################################################
    i = 0
    while i < len(names):
        scores[names[i]] = scores[names[i]] * ((m[i] * moves) + b)
        i+=1
################################################################################
    
    # print("MAX_DEPTH",max_depth)


    return scores

# if __name__=="__main__":
    # app.run(port=5001)

