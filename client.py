import requests

things_to_get = []
resp = requests.get("http://127.0.0.1:5000",
  json={'fen':'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'})
print(resp.json())
