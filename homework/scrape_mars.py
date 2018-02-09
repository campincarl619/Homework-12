from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:/Users/Chrome/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
	news = {}

	#Gather Mars News
	newsurl = "https://mars.nasa.gov/news/"
	response = requests.get(newsurl)
	soup = BeautifulSoup(response.text, 'html.parser')
	news["Title"] = soup.find_all('div', class_="content_title")[0].text.strip()
	news["Paragraph"] = soup.find_all('div', class_="rollover_description_inner")[0].text.strip()
	
	#Gather Featured Image
	browser = Browser('chrome',headless = False)
	picurl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(picurl)
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
	picDest = soup.find_all('a', class_="button fancybox")[0]
	featured_image_url = picDest["data-fancybox-href"]
	featured_image_url = "https://www.jpl.nasa.gov" + featured_image_url
	news["featImg"] = featured_image_url

	#Gather Twitter Post
	twitturl = "https://twitter.com/marswxreport?lang=en"
	responseT = requests.get(twitturl)
	soup = BeautifulSoup(responseT.text, 'html.parser')
	mars_weather = soup.find_all('p', class_="TweetTextSize")[0].text
	news["twit"] = mars_weather

	#Gather Mars Table
	factsurl = "https://space-facts.com/mars/"
	response = requests.get(factsurl)
	soup = BeautifulSoup(response.text, 'lxml')
	table = soup.find_all('table')[0] 
	Marsdf = pd.read_html(str(table))[0]
	Marsdf.columns = ["Information","Values"]
	news["marsTable"] = Marsdf.to_html(index=False)

	#Gather Hemisphere 1
	hemiurl = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser.visit(hemiurl)
	browser.click_link_by_partial_text('Cerberus')
	browser.click_link_by_partial_text('Open')
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
	hemi1 = soup.find_all('img', class_="wide-image")[0]
	hemi1 = hemi1["src"]
	news["hemi1"] = "https://astrogeology.usgs.gov" + hemi1

	#Gather Hemisphere 2
	browser.back()
	browser.click_link_by_partial_text('Schiaparelli')
	browser.click_link_by_partial_text('Open')
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
	hemi2 = soup.find_all('img', class_="wide-image")[0]
	hemi2 = hemi2["src"]
	news["hemi2"] = "https://astrogeology.usgs.gov" + hemi2

	#Gather Hemisphere 3
	browser.back()
	browser.click_link_by_partial_text('Syrtis Major')
	browser.click_link_by_partial_text('Open')
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
	hemi3 = soup.find_all('img', class_="wide-image")[0]
	hemi3 = hemi3["src"]
	news["hemi3"] = "https://astrogeology.usgs.gov" + hemi3

	#Gather Hemisphere 4
	browser.back()
	browser.click_link_by_partial_text('Valles Marineris')
	browser.click_link_by_partial_text('Open')
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
	hemi4 = soup.find_all('img', class_="wide-image")[0]
	hemi4 = hemi4["src"]
	news["hemi4"] = "https://astrogeology.usgs.gov" + hemi4

	return news


#	hemisphere_image_urls = [
#	    {"title": "Valles Marineris Hemisphere", "img_url": hemi1},
#	    {"title": "Cerberus Hemisphere", "img_url": hemi2},
#	    {"title": "Schiaparelli Hemisphere", "img_url": hemi3},
#	    {"title": "Syrtis Major Hemisphere", "img_url": hemi4},
#	]