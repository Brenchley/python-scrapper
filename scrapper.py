import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver

class ebayScrapper:
    def __init__(self, url,pages,taxRate,freightCharges,insuranceCharges):
        self.phoneList = []
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        sleep(2)

        self.driver.find_element_by_xpath("//span[contains(text(), 'Best Match')]").click()
        sleep(2)

        self.driver.find_element_by_xpath("//a[contains(text(), 'Price: highest first')]").click()
        sleep(2)
        
        for _page in range(pages):
            self.driver.find_element_by_link_text(str(_page + 1)).click()
            sleep(3)
            
            page = self.driver.current_url
            self.phoneList.append(self.getPhoneList(page,taxRate,freightCharges,insuranceCharges))        
        print (self.phoneList)


    
    def getPhoneList(self,url,taxRate,freightCharges,insuranceCharges):
        headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

        page = requests.get(url, headers = headers)
        
        pagePhoneList = []

        soup = BeautifulSoup(page.content, 'html.parser')

        phones = soup.findAll('table',attrs = {'class':'gallery'})

        for phone in phones:
            _phone ={}
            phoneDetails = phone.find('td',attrs ={'class':'details'})
            title = phoneDetails.find('a',href=True).get_text()
            price = phoneDetails.find('span',attrs={'class':'bin g-b','itemprop':'price'}).get_text()
            price = price[1:].translate({ord(','): None})
            price = float(price)
            totalPrice = round(price * (taxRate + 100)/100)
            totalPrice = (totalPrice * (insuranceCharges + 100 )/100)  + freightCharges
            totalPrice = float(totalPrice) * 102

            _phone['name']= title.encode('utf-8').strip()
            _phone['price'] = round(totalPrice)
            pagePhoneList.append(_phone)
        return pagePhoneList

ebayScrapper('http://www.ebaystores.com/BidAllies-Store/_i.html?_nkw=unlocked%20-tablet',2,8.25,15.0,5)