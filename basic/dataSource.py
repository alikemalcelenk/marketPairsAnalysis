#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 20:07:36 2021

@author: alikemalcelenk
"""
    
from bs4 import BeautifulSoup
import requests
import cloudscraper
import json
import pandas

# GET BINANCE PAIRS
scraper = cloudscraper.create_scraper()
url = 'https://coinmarketcap.com/tr/exchanges/binance/'
soup = BeautifulSoup(scraper.get(url).text, 'html.parser')

pairsMainClass = soup.find_all("tr", "cmc-table-row")

pairs = [] 
currencies = []
for index, pair in enumerate(pairsMainClass):
    found_pair = pair.find("td", "cmc-table__cell cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__market-pair")
    #Pairlerin Ana divinin classı
    #direk cmc-link olarak alamadım başka yerlerde de cmc-link classı kullanılmıs
    pairName = found_pair.find("a", "cmc-link").text
    pairLeft = pairName.rsplit('/',1)[0]
    pairRight = pairName.rsplit('/',1)[1]
    pairs.append((pairLeft, pairRight))
    currencies.append(pairLeft)
    currencies.append(pairRight)

#PAIRS - BINANCE
pairs = list(set(pairs)) #Dizinin içindeki aynı pairleri sildim.
#Sitede bazı pairlerin spot ve derivatives olarak 2 categorysi var. iksini de almaması için aynı olanları sildim. Weighti arttıyordu.
pairData = pandas.DataFrame(pairs)
pairData.columns = ["Source","Target"]
pairData.index.name = "Id"
pairData.to_csv('edges.csv')

#COINS AND TOKENS - BINANCE
currencies = list(set(currencies)) #Dizinin içindeki aynı elemanları sildim
currencyData = pandas.DataFrame(currencies)
currencyData.columns = ["Label"]
currencyData.index.name = "Id"
currencyData.to_csv('nodes.csv')

