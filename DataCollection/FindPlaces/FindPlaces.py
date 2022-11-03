import requests
import json
import time
import os
import csv


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:
        os.makedirs(path)
        print('new folder in', path)


api = ''  # add your apikey here
locations = []  # a list to store location
# Types = ['tobacco', 'clothing store', 'restaurant', 'coffee shop', 'computer consultant', 'motor repair', 'orchard', 'dental']
Types = ['restaurant']
# get all the locations
with open("suburb_list.csv") as f:
    csv_reader = csv.reader(f)
    for i in csv_reader:
        locations.append(i[0])

# start searching
for location in locations:
    print(location)
    for Type in Types:
        print(Type)
        query = Type + ' in ' + location

        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?" + "query=" + query + "&key=" + api + '&types' + Type

        page = 0
        while True:

            mkdir("search results" + "/" + Type + "/" + query)

            r = requests.get(url)

            x = r.json()
            y = x['results']

            with open("search results" + "/" + Type + "/" + query + "/" + location + Type + str(page) + ".json", 'w', encoding='utf-8') as json_file:
                json.dump(x, json_file, ensure_ascii=False)

            if 'next_page_token' not in x:
                break
            else:

                next_page_token = x["next_page_token"]

                url = "https://maps.googleapis.com/maps/api/place/textsearch/json?key={0}&pagetoken={1}".format(api,
                                                                                                                next_page_token)

                page += 1

            time.sleep(3)  # time break to prevent request too fast to be baned from google
            print(page)
