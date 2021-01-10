#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 20:07:36 2021

@author: alikemalcelenk
"""
    
from bs4 import BeautifulSoup
import requests
import json
import pandas
import time
from selenium import webdriver

def getHTML(soup): #Source codeu almak için ekledim. Terminalde hepsini göremiyorum. 
    try:
        codes = open("html.txt", "w")
        codes.write(str(soup))
        codes.close()
        
    except IOError:
        print("File Error!")

#Selenium ayarları. selenium u Load More a bastıp daha fazla data çekmek için kullandım.
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("./chromedriver", chrome_options=options)

# GET BINANCE PAIRS
driver.get("https://coinmarketcap.com/exchanges/binance/")
for y in range(10): #Tüm dataları çekebilmesi için. 10 kere çekse yetiyor. her butonda 100 data geliyor. 
                    #Başlangıç datası değişkenlik gösterebiliyor. En temizi 10 alıp garantiye almak.
    moreButtons = driver.find_elements_by_css_selector("button[class$='wn9odt-0 iGNdpc cmc-button cmc-button--color-default']") #Load More button
    #buttonlar içinde classı->wn9odt-0 iGNdpc cmc-button cmc-button--color-default olanı bul demek.
    for x in range(len(moreButtons)):
        if moreButtons[x].is_displayed():
            driver.execute_script("arguments[0].click();", moreButtons[x])
            time.sleep(0.5)
      
pageSource = driver.page_source
soup = BeautifulSoup(pageSource, 'html.parser')
#getHTML(soup) #Source codeu almak için ekledim. Terminalde hepsini göremiyorum. 
#source code u alma nedenim, chromedriver dan aldığı için class isimleri kendi browserımdan farklı oluyor. 
pairsMainClass = soup.find_all("tr", "cmc-table-row")

pairs = [] 
currencies = []

for index, pair in enumerate(pairsMainClass):
    try:
        # print(pair)
        foundPair = pair.find("td", "cmc-table__cell cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__market-pair") 
        #Pairlerin Ana divinin classı
        #direk cmc-link olarak alamadım başka yerlerde de cmc-link classı kullanılmıs
        pairName = foundPair.find("a", "cmc-link").text
        pairLeft = pairName.rsplit('/',1)[0]
        pairRight = pairName.rsplit('/',1)[1]
        pairs.append((pairLeft, pairRight))
        currencies.append(pairLeft)
        currencies.append(pairRight)
    except AttributeError:
        continue

#PAIRS - BINANCE 
pairs = list(set(pairs)) #Dizinin içindeki aynı pairleri sildim.
#Sitede bazı pairlerin spot ve derivatives olarak 2 categorysi var. iksini de almaması için aynı olanları sildim. Weighti arttıyordu.
pairData = pandas.DataFrame(pairs)
pairData.columns = ["Source","Target"]
pairData.index.name = "Id"
pairData.to_csv('edges.csv')

#CURRENCIES - BINANCE 
currencies = list(set(currencies)) #Dizinin içindeki aynı elemanları sildim
currencyData = pandas.DataFrame(currencies)
currencyData.columns = ["Label"]
currencyData.index.name = "Id"
currencyData.to_csv('nodes.csv')

