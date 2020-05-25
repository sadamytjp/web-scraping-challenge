import os
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless = False)



def Mars_news():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    #Getting the news title
    news_title = soup.find_all(class_ = 'content_title')
    news_title = news_title[1].text
    #Getting news text
    news_p = soup.find_all(class_ = 'article_teaser_body')
    news_p = news_p[0].text

    latest_news = {'news_title':news_title, 'news_p':news_p}

    browser.quit()

    return latest_news

def featured_image():
    browser = init_browser()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    full_image_button = browser.find_by_id('full_image')
    full_image_button.click()
    more_info_button = browser.find_link_by_partial_text('more info')
    more_info_button.click()
    html = browser.html
    soup = bs(html, 'html.parser')
    relative_image_url = soup.find(class_ = 'main_image').get_attribute_list('src')
    relative_image_url = relative_image_url[0]
    featured_image_url = "https://www.jpl.nasa.gov" + relative_image_url
    featured_image = {'image': featured_image_url}
    
    browser.quit()
    
    return featured_image

def weather():
    browser = init_browser()
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_weather = soup.find('div', class_ = "css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    mars_weather = mars_weather.text.replace('InSight ', '')

    weather = {'weather':mars_weather}

    browser.quit()

    return weather


def hemispheres():
    browser = init_browser()
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    links = soup.find_all('div', class_='item')
    hemisphere_image_urls = []
    for link in links:
        title = link.find('h3').text
        partial_url = link.find('a', class_ = 'itemLink product-item')['href']
        browser.visit('https://astrogeology.usgs.gov' + partial_url)
        partial_img_html = browser.html
        soup5 = bs(partial_img_html, 'html.parser')
        image_url = 'https://astrogeology.usgs.gov' + soup5.find('img', class_ = 'wide-image')['src']
        hemisphere_image_urls.append({'title': title, 'image_url': image_url})

    browser.quit()

    return hemisphere_image_urls


def mars_facts():
    browser = init_browser()
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    facts = pd.read_html(url)[0]

    mars_facts = {'facts':facts}

    browser.quit()

    return mars_facts
