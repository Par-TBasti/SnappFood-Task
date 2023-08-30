# I) Adding Library And Package

import re
import psycopg2
import requests
import time
import random 
import pandas
import numpy
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




# 11. Classification
# Determine the thresholds that will define each category (A to D)
def classify_restaurant(css):
    if css > 70:
        return 'A'
    elif 50 < css <= 70:
        return 'B'
    elif 30 < css <= 50:
        return 'C'
    elif 0 <= css <= 30:
        return 'D'


# III) Connecting To Google map

user_agents = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
service = Service("D:/SnappFood/chromedriver.exe")
options = webdriver.ChromeOptions() 
options.add_argument(f"user-agent' = {user_agents}")
options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
driver = webdriver.Chrome(options=options, service=service)
driver.get('https://www.google.com/maps?authuser=0')
driver.maximize_window()



# IV) Scraping Data
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
    




# V) Creating The DataFrame
dataset = pandas.DataFrame()
dataset = dataset.assign(Name=name_list, rate=rate_list, review_count=review_list, type=type_list, location=location_list)



# VI) Data Cleaning
# A) Changing Format
# The 'review_count' row encapsulates numeric values within parentheses '()' that need
# to be removed using regular expressions (regex), followed by a conversion to a float data type.

dataset['review_count'] = dataset['review_count'].str.replace(r'\D', '', regex=True)
dataset['review_count'] = dataset['review_count'].astype(float)




# B) Removing The Outliers
# Within the context of adding restaurants to the database, a verification process is conducted. 
# Specifically, it involves examining the geographical information associated with these restaurants 
# to determine if the location contains 'Kerman.' If it does not meet this criterion, the respective 
# entry is subject to deletion.

contains_kerman = dataset['location'].str.contains('Kerman', case=False, na=False)
dataset = dataset[contains_kerman]



# C) Handling Missing Values
# In the context of filling missing data within the attributes related to ratings and review counts, 
# the procedure involves populating these gaps with the numerical value '0.'

dataset.isnull().sum()
dataset.rate.fillna(0, inplace=True)
dataset.review_count.fillna(0, inplace=True)



# D) Removing Duplicates

duplicate_columns = dataset.columns[dataset.nunique() == 1].tolist()
dataset = dataset.drop(columns=duplicate_columns)



# VII) Data Analysis
# A) Calculating the average rating of all restaurants, sum the total number of reviews 
# for all restaurants and average number of reviews per restaurant.

total_metrics = pandas.DataFrame()
totals = ['Average_Rating', 'Total_Reviews', 'Average Review Count']
value = [dataset.rate.mean(), dataset.review_count.sum(), dataset.review_count.mean()]
total_metrics = total_metrics.assign(Totals=totals, Values=value)



# B)  Calculating 1. the number of restaurants for each restaurant type 
#                 2. average rating for each type of restaurant
#                 3. Sum the total number of reviews for each type of restaurant 
#                 4. the average number of reviews per restaurant type.

# 1.

metrics_by_type = pandas.DataFrame()
restaurant_type_counts = dataset['type'].value_counts()
metrics_by_type = pandas.DataFrame({'Restaurant_Type': restaurant_type_counts.index, 'Frequency': restaurant_type_counts.values})

# 2.

average_ratings = dataset.groupby('type')['rate'].mean().reset_index()
average_ratings.columns = ['Restaurant_Type', 'Average_Rating']
metrics_by_type = pandas.merge(average_ratings, metrics_by_type, on='Restaurant_Type')

# 3.

total_review = dataset.groupby('type')['review_count'].sum().reset_index()
total_review.columns = ['Restaurant_Type', 'Total_Review']
metrics_by_type = pandas.merge(total_review, metrics_by_type, on='Restaurant_Type')

# 4.

average_review = dataset.groupby('type')['review_count'].mean().reset_index()
average_review.columns = ['Restaurant_Type', 'Average_Review']
metrics_by_type = pandas.merge(average_review, metrics_by_type, on='Restaurant_Type')

# C) A composite metric that considers both the rating and review count to assess 
# overall customer satisfaction. using this formula
# CSS = ((Rating * Review Count) / Max(Review Count)) * 100

dataset['CSS'] = ((dataset['rate'] * dataset['review_count']) / (total_metrics.loc[total_metrics['Totals'] == 'Total_Reviews', 'Values'].values[0])) * 100



# D) Creating a new column in dataset to store the assigned categories (A, B, C, D).

dataset['Classification'] = dataset['CSS'].apply(classify_restaurant)



# VIII) Adding new datasets to CSV files

dataset.to_csv('Restaurant.csv', index=False)
total_metrics.to_csv('Total.csv', index=False)
metrics_by_type.to_csv('metrics_by_type.csv', index=False)