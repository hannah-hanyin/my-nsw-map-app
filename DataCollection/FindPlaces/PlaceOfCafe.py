import requests
import json
import time

api = 'AIzaSyCtJX62_ArOb0kpUTGh_Spl03Af4YsvVyg'  # your google api-key

query = 'cafes in sydney'  # keywords for searching

url = "https://maps.googleapis.com/maps/api/place/textsearch/json?" +"query=" + query + "&key=" + api  # editing url

page = 0  # number counter
while True:
    r = requests.get(url)

    x = r.json()
    y = x['results']

    with open("./cafes" + str(page) + ".json", 'w', encoding='utf-8') as json_file:
        json.dump(x, json_file, ensure_ascii=False)

    if 'next_page_token' not in x:
        break
    else:
        next_page_token = x["next_page_token"]

        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?key={0}&pagetoken={1}".format(api, next_page_token)
        page += 1

    time.sleep(3)  # preventing from requesting too fast
    print(page)

