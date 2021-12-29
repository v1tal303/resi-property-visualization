from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import datetime as dt

today = dt.date.today()
yesterday = today - dt.timedelta(days=1)
yesterday_str = yesterday.strftime("%d-%m-%Y")
today_str = today.strftime("%d-%m-%Y")

# Selenium URL setup

s = Service("C:\Development\chromedriver.exe")
browser = webdriver.Chrome(service=s)
url = "https://www.rightmove.co.uk/properties/87265649#/?channel=RES_BUY"
browser.get(url)

# Let the user input the search criteria in the browser.


# Preset the list of items to be stored



# Run this loop when user have specified the search criteria and stop when there are no pages left.

sleep(2)
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
detailed_type = browser.find_element(By.XPATH, "//*[@id='root']/main/div/div[2]/div/article[2]/div[2]/div[1]/div[2]/div[2]/div").text
try:
    property_keys = browser.find_element(By.XPATH, "//*[@id='root']/main/div/div[2]/div/article[3]/ul").text
    print(property_keys)
except:
    print("no keys")

try:
    no_beds = browser.find_element(By.XPATH, "//*[@id='root']/main/div/div[2]/div/article[2]/div[2]/div[2]/div[2]/div[2]/div").text
    print(no_beds)
except:
    print("No beds")

try:
    no_bathrooms = browser.find_element(By.XPATH, "//*[@id='root']/main/div/div[2]/div/article[2]/div[2]/div[3]/div[2]/div[2]/div").text
    print(no_bathrooms)
except:
    print("No bathrooms")



readmore_button = browser.find_element(By.XPATH, "//*[@id='root']/main/div/div[2]/div/article[3]/div[3]/button[2]")
readmore_button.click()
property_desc = browser.find_element(By.XPATH, "//*[@id='root']/main/div/div[2]/div/article[3]/div[3]/div").text




print(property_desc)






