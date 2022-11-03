import lxml
import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.commercialrealestate.com.au/for-lease/nsw/')
soup = BeautifulSoup(r.text, 'lxml')
fo = open('lease-price.txt', 'w')
for item in soup.find_all('table', {'class': 'css-hxuvu4'}):
    # print(item.select('td#data-testid price'))
    fo.write(item.find({'a': 'data-testid address'}).text.replace('<br/>', ' ') + "\n")
    fo.write(item.find({"td": "data-testid price"}).text + "\n")
    fo.write('\n')

