# scrape social media statistics by country from gs.statcounter.com
# Matt Mauer
# 1/11/2020
# Xu Initiative 

from bs4 import BeautifulSoup
import pandas as pd
import requests

countries = []
twitter_rates = []

# Use below lines for selenium: SLOWER than requests
# from selenium import webdriver
# driver = webdriver.Chrome("/Users/matthewmauer/chromedriver")
# driver.get("https://gs.statcounter.com/social-media-stats")
# content = driver.page_source

def get_trate(c, attr='col col-span-2'):
    # scoop the soup from each country page
    r = requests.get('https://gs.statcounter.com' + c.a['href']).content
    soup_c = BeautifulSoup(r, 'lxml')

    # recursively search for twitter usage rate
    c_rates = soup_c.find_all('tr', class_=attr)
    for rate in c_rates:
        if rate.th.text == "Twitter":     
            return float(rate.span.text)
    if attr == 'col col-span-2':        
        return float(get_trate(c, attr='col col-span-2 col-row-2'))
    return 0

# go to page linking to all countries and scoop soup
r = requests.get("https://gs.statcounter.com/social-media-stats").content
soup_m = BeautifulSoup(r, 'lxml')

# create list of country buttons
soup_of_countries = soup_m.find_all('li', class_='col col-span-4')[9:-11]

# for each country button append country name and twitter usage rate to lists
for c in soup_of_countries:
    countries.append(c.text)
    trate = get_trate(c)
    twitter_rates.append(trate)

# convert lists to pandas DataFrame for future manipulation
table = pd.DataFrame({'twitter_usage_rates':twitter_rates}, index=countries)
table = table[table.twitter_usage_rates > 5]

# write final product to csv
table.to_csv(path_or_buf='~/Documents/Harris/Internship_RA/XuInitiative/twit_usage.csv',
    index_label='Countries')

