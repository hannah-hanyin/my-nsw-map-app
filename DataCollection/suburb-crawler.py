import requests
import csv
from bs4 import BeautifulSoup


url = 'https://auspost.com.au/locate/post-office/nsw#tab-a'
r = requests.get(url)
file = open('suburb_list.csv', 'w')
writer = csv.writer(file)
soup = BeautifulSoup(r.text, 'lxml')
for items in soup.find_all('a', {'class': 'link-chevron pol-suburb-index-link js-pol-suburb-index-link'}):
    writer.writerow([items.text])
    # fo.write(items.text + '\n')


