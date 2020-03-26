import requests
from bs4 import BeautifulSoup

bidalliesURL = 'http://www.ebaystores.com/BidAllies-Store/_i.html?_nkw=unlocked%20-tablet'

headers = {"User-Agent": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'}

page = requests.get(bidalliesURL, headers = headers)

soup = BeautifulSoup(page.content, 'html.parser')

phones = soup.findAll('table',attrs = {'class':'gallery'})

for phone in phones:
    phoneDetails = phone.find('td',attrs ={'class':'details'})
    title = phoneDetails.find('a',href=True).get_text()
    price = phoneDetails.find('span',attrs={'class':'bin g-b','itemprop':'price'}).get_text()
    # converts price to ksh
    price = float(price[1:]) * 100
    print("{} {}").format(title.encode('utf-8').strip(), price)
    # print(title)
    # print(price)

# print(phone)
