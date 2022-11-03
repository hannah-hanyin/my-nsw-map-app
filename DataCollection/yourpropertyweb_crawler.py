import csv
import random
from datetime import datetime

from bs4 import BeautifulSoup
import requests

base_link = 'https://www.yourinvestmentpropertymag.com.au'

home_link = f'{base_link}/top-suburbs/nsw/'
home_response = requests.get(home_link, allow_redirects=False)
assert home_response.status_code == 200


def get_suburbs(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    container = soup.select("#container ul.suburbs li a")
    return [(i.text, i.attrs["href"]) for i in container]


def get_suburb_data(suburb):
    link = base_link + suburb[1]
    response = requests.get(link, allow_redirects=False)
    data = {'Name': suburb[0]}

    if response.status_code != 200:
        print(f"Error loading {suburb}")
        return data

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.select_one(".content table")

    if not table:
        return data

    rows = table.select("tr")[1:]

    for index, row in enumerate(rows):
        if index == 0 and not row.select_one("td.House"):
            return data

        label = row.select_one("th label").getText().strip()
        value = row.select_one("td.House").getText().strip()
        data[label] = value

    return data


def get_all_suburb_data(suburbs):
    data = []
    total = len(suburbs)
    print(f"Total {total} suburbs")
    one_percent = total / 100

    for index, suburb in enumerate(suburbs):
        # if (index + 1) % one_percent == 0:
        percentage = 100 * (index + 1)/total
        suburb_data = get_suburb_data(suburb)
        data.append(suburb_data)
        print(f"{index + 1}/{total} finished", suburb_data)

    return data


def write_csv(data):
    time_str = datetime.now().isoformat()
    f = open(f"data {time_str}.csv", "w+")

    writer = csv.DictWriter(
        f, fieldnames=[
            "Name", "Median price", "Quarterly growth", "12-month growth", "Average Annual Growth",
            "Weekly median advertised rent", "Number of sales", "Gross rental yield", "Days on market"
        ])
    writer.writeheader()
    writer.writerows(data)
    f.close()


suburbs = get_suburbs(home_response)
all_suburb_data = get_all_suburb_data(suburbs)
write_csv(all_suburb_data)
