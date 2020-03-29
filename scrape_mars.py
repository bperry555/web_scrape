from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time
import requests

def scrape_info():
    browser = Browser()

    html = requests.get('https://mars.nasa.gov/news')  
    soup = bs(html.text,'html.parser')

    nasa_headline = []
    nasa_text = []

    for headline in soup.find_all('div', class_='content_title'):
        nasa_headline.append(headline.get_text(strip=True))
    for text in soup.find_all('div', class_='rollover_description_inner'):
        nasa_text.append(text.get_text(strip=True))

    nasa_news = dict(zip(nasa_headline, nasa_text))


    executable_path = {'executable_path': '/'}
    browser = Browser('chrome', executable_path)
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    soup = bs(browser.html, 'html.parser')
    result = soup.find('article')['style']
    full_featured_img = "https://www.jpl.nasa.gov" + result.split(' ')[1].strip("url('');")
    browser.quit()

    featured_img = {'Feature Image': full_featured_img}
    
    
    html = requests.get('https://twitter.com/marswxreport?lang=en')
    soup = bs(html.text, 'html.parser')

    import re

    mars_weather = []
    tweets = soup.find_all('div', {'class':'tweet'})
    for tweet in tweets:
        # context = tweet.find('div',{'class':'context'}).text.replace("\n"," ").strip()
        content = tweet.find('div',{'class':'content'})
        # header = content.find('div',{'class':'stream-item-header'})
        # user = header.find('a',{'class':'account-group js-account-group js-action-profile js-user-profile-link js-nav'}).text.replace("\n"," ").strip()     
        # time = header.find('a',{'class':'tweet-timestamp js-permalink js-nav js-tooltip'}).find('span').text.replace("\n"," ").strip()
        message = content.find('div',{'class':'js-tweet-text-container'}).text.replace("\n"," ").strip()
        
        match = re.search('InSight', message)
        if match:
            mars_weather.append(message)

    df = pd.read_html('https://space-facts.com/venus/')

    mars_table = {'table': df[0].to_html()}


    html_list = ['https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced',
             'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced',
             'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced',
             'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced']
             

    for html in html_list:
        response = requests.get(html)
        soup = bs(response.text, 'html.parser')
        title_result = soup.find('h2', class_='title').text
        pic_result = str(soup.find('a',text='Original')).split()[1].lstrip('href=').strip('""')
        pict_title = {'pic_title': title_result}
        pict_html = {'pic_html': pic_result}
    
    scrape_info = {{'news': nasa_news},
                    {'img': featured_img},
                    {'table': mars_table},
                    {'pict title': pict_title},
                    {'pict html' : pict_html}}
    
    return(scrape_info)