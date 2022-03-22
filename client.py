import grequests

things_to_get = []
for i in range(500):
    things_to_get.append(grequests.get("http://127.0.0.1:5000"))

print(grequests.map(things_to_get))