import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver

class ebayScrapper:
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        sleep(2)

        self.driver.find_element_by_xpath("//span[contains(text(), 'Best Match')]").click()
        sleep(2)

        self.driver.find_element_by_xpath("//a[contains(text(), 'Price: highest first')]").click()
        sleep(2)
        page = self.driver.current_url

        self.getPhoneList(page)
    
    def getPhoneList(self,url):
        headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

        page = requests.get(url, headers = headers)
        
        phoneList = {}

        soup = BeautifulSoup(page.content, 'html.parser')

        phones = soup.findAll('table',attrs = {'class':'gallery'})

        for phone in phones:
            phoneDetails = phone.find('td',attrs ={'class':'details'})
            title = phoneDetails.find('a',href=True).get_text()
            price = phoneDetails.find('span',attrs={'class':'bin g-b','itemprop':'price'}).get_text()
            price = float(price[1:].translate({ord(','): None})) * 102

            phoneList['name']= title.encode('utf-8').strip()
            phoneList['price'] = round(price)
            print(phoneList)      



ebayScrapper('http://www.ebaystores.com/BidAllies-Store/_i.html?_nkw=unlocked%20-tablet')