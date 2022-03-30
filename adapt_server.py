"""
Runs an adaptation server, which receives data from the bot and determines if 
changes should be made for its decision making
"""

from flask import Flask, request
app = Flask(__name__)


@app.route("/")
async def bot():
    """
    responds to a get request with json
    with the next move to be made by the bot
    """
    x = request.get_json()
    fen_string = x['fen']
    print(fen_string)
    return {'max_depth':2,'fen':fen_string}

if __name__=="__main__":
    app.run(port=5001)

