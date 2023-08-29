# I) Adding Library And Package

import re
import psycopg2
import requests
import time
import random
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys



# II) Functions

# 1.Clicking On An Element
# This function operates by obtaining the XPath of a designated element and then employing a waiting 
# period of 40 seconds to ensure the full loading of the said element. Subsequently, it proceeds to 
# execute the clicking action on the targeted element.

def clicking(xpath):
    button = WebDriverWait(driver, 40).until(EC.presence_of_element_located
                                         ((By.XPATH, xpath)))
    driver.execute_script("arguments[0].click();", button)


# 2.Scroll To Bottom
# scrolls through a web page section specified by the 'section' parameter, gradually reaching the bottom. 
# It pauses for a specified time, 'scroll_pause_time,' between scrolls. It dynamically adjusts the scroll 
# position until reaching the end by comparing the section's scroll height.

def scroll_to_bottom(scroll_pause_time, section):
    last_height = driver.execute_script("return arguments[0].scrollHeight;", section)

    while True:
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", section)
        time.sleep(scroll_pause_time)

        new_height = driver.execute_script("return arguments[0].scrollHeight;", section)
        if new_height == last_height:
            break
        last_height = new_height
        
        
        
# 3.Hover Mouse Action
# This function operates by obtaining the XPath of a designated element and then employing a waiting 
# period of 40 seconds to ensure the full loading of the said element. Subsequently, it proceeds to 
# execute the mouse hovering action on the targeted element.

def hover(xpath):
    section = WebDriverWait(driver, 40).until(EC.presence_of_element_located
                                         ((By.XPATH, xpath)))
    hover = ActionChains(driver).move_to_element(section)
    hover.perform()



# 4. Checking Element Existence

def element_existence(xpath):
    try:
        element  = WebDriverWait(driver, 10).until(EC.presence_of_element_located
                                         ((By.XPATH, xpath)))
        return True
    except:
        return False




# 6. Collecting Names

def name():
    xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[1]/h1'
    if element_existence(xpath):
        return driver.find_element(By.XPATH, xpath).text
    else:
        return None
    


# 7. Collecting rating

def rate():
    xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[1]/span[1]'
    if element_existence(xpath):
        return float(driver.find_element(By.XPATH, xpath).text)
    else:
        return None




# 8. Collecting Review Counts
def review():
    xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[2]/span/span'
    if element_existence(xpath):
        return driver.find_element(By.XPATH, xpath).text
    else:
        return None
    


# 9. Collecting Type
def type():
    xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/span/span/button'
    if element_existence(xpath):
        return driver.find_element(By.XPATH, xpath).text
    else:
        return None
    


# 10. Collecting Location

def location():
    xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[9]/div[3]/button/div/div[2]/div[1]'
    if element_existence(xpath):
        return driver.find_element(By.XPATH, xpath).text
    else:
        return None
    
    
    
# III) Connecting Database

conn = psycopg2.connect(database='rafsanjan',
                        host="localhost",
                        port=5432,
                        user="postgres",
                        password="1234")
conn.autocommit = True
cursor = conn.cursor()



# IV) Connecting To Google map

user_agents = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
service = Service("D:/SnappFood/chromedriver.exe")
options = webdriver.ChromeOptions() 
options.add_argument(f"user-agent' = {user_agents}")
options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
driver = webdriver.Chrome(options=options, service=service)
driver.get('https://www.google.com/maps?authuser=0')
driver.maximize_window()


# V) Creating Table

cursor.execute('''CREATE TABLE IF NOT EXISTS restaurant (
            name            VARCHAR(200),
            rate            FLOAT,
            review_count    VARCHAR(10),
            type            VARCHAR(100),
            location        VARCHAR(200)
            );''')




# VI) Scraping Data
# a) Seraching The City

search_bar = WebDriverWait(driver, 40).until(EC.presence_of_element_located
                                        ((By.XPATH, '//*[@id="searchboxinput"]')))
search_bar.send_keys('Rafsanjan Kerman Province')
clicking('//*[@id="cell0x0"]')
time.sleep(10)



# b) Finding The Restaurants

clicking('//*[@id="assistive-chips"]/div/div/div/div[1]/div/div/div/div/div[2]/div[2]/div[1]/button/span')
time.sleep(10)



# c) Crawling Data
# c-1) Restaurant Elements
name_list = []
rate_list = []
review_list = []
type_list = []
location_list = []
restaurants_sections = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]')
scroll_to_bottom(5, restaurants_sections)
i = 3
while True:
    RE = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[{}]/div/a'.format(i)
    if element_existence(RE):
        clicking(RE)
        time.sleep(5)
   
# c-2) Restaurant Names

        name_list.append(name())
    
# c-3) Restaurant Rate

        rate_list.append(rate())
    
# c-4) Restaurant Review Count

        review_list.append(review())

# c-5) Restaurant Type

        type_list.append(type())
       
# c-6) Restaurant Location

        location_list.append(location())
        i += 2
         
    else:
        break
    




# D) Adding Data To Database

for (i, j, k, l, m) in zip(name_list, rate_list, review_list, type_list, location_list):
    cursor.execute(
        '''INSERT INTO restaurant (name, rate, review_count, type, location) VALUES (%s, %s, %s, %s, %s);''', (i,j,k,l,m))