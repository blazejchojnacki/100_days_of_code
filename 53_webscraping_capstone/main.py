import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

URL_FORM = 'https://docs.google.com/forms/d/e/1FAIpQLSd0KCwn1Du04xLZDoDYTQ6ECthV9WwzJBfPQ7cp94gYbNSmqA/viewform?usp=header'
URL_SCRAPED = 'https://appbrewery.github.io/Zillow-Clone/'

html_page = requests.get(url=URL_SCRAPED)
page_soup = BeautifulSoup(html_page.text, 'html.parser')
parent_elements = page_soup.find_all(class_='ListItem-c11n-8-84-3-StyledListCardWrapper')
links_list, price_list, addresses_list = [], [], []

for element in parent_elements:
    links_list.append(element.find('a').get('href'))
    price_list.append(element.find(class_='PropertyCardWrapper__StyledPriceLine').text.strip('+/mo 1bd'))
    addresses_list.append(element.find('a').text.replace('|', ',').strip())

browser_options = webdriver.EdgeOptions()
browser_options.add_experimental_option("detach", True)
driver = webdriver.Edge(options=browser_options)

for index in range(len(links_list)):
    driver.get(URL_FORM)
    input_elements_list = driver.find_elements(By.CLASS_NAME, "whsOnd")
    data = [addresses_list[index], price_list[index], links_list[index]]
    for answer_field in input_elements_list:
        answer_field.send_keys(data[input_elements_list.index(answer_field)])
    submit_element = driver.find_element(By.CLASS_NAME, 'l4V7wb')
    submit_element.click()
    time.sleep(1)

print('done')
