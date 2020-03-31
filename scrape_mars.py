from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time
import requests

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    # browser = Browser()

    html = requests.get('https://mars.nasa.gov/news/')
    soup = bs(html.text,'html.parser')

    nasa_news = soup.find('div', class_='content_title').text.strip('\n')
    nasa_article = soup.find('div', class_='rollover_description_inner').text.strip('\n')


    # browser = Browser('chrome', init_browser())
    # browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    browser = requests.get('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    soup = bs(browser.text, 'html.parser')
    # browser.quit()
    result = soup.find('article')['style']
    featured_img_url = "https://www.jpl.nasa.gov" + result.split(' ')[1].strip("url('');")
    
    
    html = requests.get('https://twitter.com/marswxreport?lang=en')
    soup = bs(html.text, 'html.parser')

    import re

    mars_tweet = []

    tweets = soup.find_all('div', {'class':'tweet'})
    for tweet in tweets:
        # context = tweet.find('div',{'class':'context'}).text.replace("\n"," ").strip()    *Might Use Later*
        content = tweet.find('div',{'class':'content'})
        # header = content.find('div',{'class':'stream-item-header'})   *Might Use Later*
        # user = header.find('a',{'class':'account-group js-account-group js-action-profile js-user-profile-link js-nav'}).text.replace("\n"," ").strip()   *Might Use Later*   
        # time = header.find('a',{'class':'tweet-timestamp js-permalink js-nav js-tooltip'}).find('span').text.replace("\n"," ").strip()    *Might Use Later*
        message = content.find('div',{'class':'js-tweet-text-container'}).text.replace("\n"," ").strip()
        
        match = re.search('InSight', message)
        if match:
            mars_tweet.append(message)
    mars_weather_tweet = mars_tweet[0] 

    df = pd.read_html('https://space-facts.com/venus/')
    mars_table = df[0].to_html()


    html_list = ['https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced',
             'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced',
             'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced',
             'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced']
             
    mars_hemisphere_image_urls = []
    mars_hemisphere_image_urls.clear()
                
    for html in html_list:
        response = requests.get(html)
        soup = bs(response.text, 'html.parser')
        
        title_result = soup.find('h2', class_='title').text
        pic_result = 'https://astrogeology.usgs.gov' + soup.find('img',class_='wide-image')['src']
        pic_dict = {'title': title_result, 'img_url': pic_result}
        mars_hemisphere_image_urls.append(pic_dict)
    
    mars_facts = {'nasa_news': nasa_news,
             'nasa_article': nasa_article,
             'featured_img_url': featured_img_url,
             'mars_weather_tweet': mars_weather_tweet,
             'mars_table': mars_table,
             'mars_hemisphere_image_urls': mars_hemisphere_image_urls}

    return(mars_facts)