#!/usr/bin/env python
# coding: utf-8

from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from webdriver_manager.chrome import ChromeDriverManager
import time

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

#URL of page to be scraped
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
response = browser.html

#Create BeautifulSoup object; parse with 'html.parser'
soup = bs(response, 'html.parser')


# ## Step 1 - Scraping

# ### Latest Mars News

#Collecting the latest news title
news_title = soup.find_all('div', class_='content_title')[0].text

#Collecting the latest news paragraph
news_p = soup.find_all('div', class_='rollover_description_inner')[0].text

print (f'{news_title}: {news_p}')


# ### JPL Mars Space Images

jpl_url = 'https://webcache.googleusercontent.com/search?q=cache:gFCwbhsgFQsJ:https://www.jpl.nasa.gov/images/+&cd=1&hl=en&ct=clnk&gl=us'
browser.visit(jpl_url)


# ### Mars Facts


fact_url = 'https://space-facts.com/mars/'
planet_table = pd.read_html(fact_url)

planet_table


mars_table = planet_table[0]
mars_table = mars_table.rename(columns={0:'Description',1:'Value'})

mars_table


#Converting the data to a HTML table string.
html_table = mars_table.to_html()
html_table = html_table.replace('\n','')

html_table


# ### Mars Hemispheres


#Url to scrape
usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(usgs_url)
usgs_html = browser.html
soup = bs(usgs_html,'html.parser')


#Extracting hemispheres 
hemispheres = soup.find('div',class_='collapsible results')
mars_hs = hemispheres.find_all('div',class_= 'item')
image_info = []


base_url = 'https://astrogeology.usgs.gov'

#Looping through each hemisphere
for hs in mars_hs:
    try:
        #Title
        hemisphere = hs.find('div',class_= 'description')
        title = hs.h3.text
        
        #Image url
        hs_url = hs.a['href']
        browser.visit(f'{base_url}{hs_url}')
        
        html = browser.html
        soup = bs(html,'html.parser')
        image_url = soup.find('li').a['href']
        if (title and image_url):
            # Print results
            print('======================')
            print(title)
            print(image_url)
            
        # Create dictionary for title and url
        hemisphere_dict={
            'title':title,
            'image_url':image_url
        }
        image_info.append(hemisphere_dict)
        
    except Exception as e:
        print(e)


image_info


# ## Step 2 - MongoDB and Flask Application

#Dictionary containing all of the information that was scraped from the URLs above.

mars_dict={
    "News Title": news_title,
    "News Paragraph": news_p,
    "Mars Fact Table": html_table,
    "Hemisphere Images": image_info
}


mars_dict

#Quitting the browser
browser.quit()
return mars_dict




