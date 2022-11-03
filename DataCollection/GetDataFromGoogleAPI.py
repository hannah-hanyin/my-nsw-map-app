import requests
import json
import time
import os
import csv
import requests.packages.urllib3.util.ssl_

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:
        os.makedirs(path)
        print('new folder in', path)


api = 'AIzaSyDWi4AVOIDFcYQnE6BAetQKS62CE4T9pjs'  # add your apikey here
locations = []  # a list to store location
# all types
Types = ['tobacco', 'clothing store', 'restaurant', 'coffee shop', 'motor repair', 'orchard', 'dental']
# get all the locations
with open("suburb_list.csv") as f:
    csv_reader = csv.reader(f)
    for i in csv_reader:
        locations.append(i[1])

# start searching
for location in locations:
    print(location)
    for Type in Types:
        print(Type)
        query = Type + ' in ' + location

        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?" + "query=" + query + '&types=train_station' + "&key=" + api

        page = 0
        while True:

            mkdir("search results" + "/" + Type + "/" + query)

            r = requests.get(url, verify=False)

            x = r.json()
            y = x['results']

            with open("search results" + "/" + Type + "/" + query + "/" + location + Type + str(page) + ".json", 'w',
                      encoding='utf-8') as json_file:
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
