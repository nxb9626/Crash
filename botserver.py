from flask import Flask

app = Flask(__name__)

@app.route("/")
async def hello_world():
    for i in range(50000):
        print(i)
    return "<p>Hello, World!</p>"


if __name__=="__main__":
    app.run(threaded=True)