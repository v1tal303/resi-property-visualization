# import requests
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import datetime as dt


# Get SF properties from Zillow - Address/Price/Link (depreciated as zillow is difficult to webscrape)


today = dt.date.today()
yesterday = today - dt.timedelta(days=1)
yesterday_str = yesterday.strftime("%d-%m-%Y")
today_str = today.strftime("%d-%m-%Y")


s = Service("C:\Development\chromedriver.exe")
browser = webdriver.Chrome(service=s)
url = "https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E443&insId=1&radius=0.0&minPrice=&maxPrice=&minBedrooms=&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=&_includeSSTC=on&sortByPriceDescending=&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&newHome=&auction=false"
browser.get(url)

no_of_pages_raw = browser.find_element(By.XPATH, "//*[@id='l-container']/div[3]/div/div/div/div[2]/span[3]")
# pages_remaining = int(no_of_pages_raw.text)
pages_remaining = 0
print(pages_remaining)



type_raw = []
type_list = []
address_list = []
price_list = []
agency_list = []
number_list = []
link_list = []

while pages_remaining >= 0:
    sleep(2)
    property_type = browser.find_elements(By.CSS_SELECTOR, ".propertyCard-title")

    for i in property_type:
        type_raw.append(i.text)
        if "apartment" in i.text.lower():
            type_list.append("apartment")
        elif "detached" in i.text.lower():
            type_list.append("detached")
        elif "semi" in i.text.lower():
            type_list.append("semi")
        elif "terrace" in i.text.lower():
            type_list.append("terrace")
        elif "bungalow" in i.text.lower():
            type_list.append("bungalow")
        elif "land" in i.text.lower():
            type_list.append("land")
        elif "plot" in i.text.lower():
            type_list.append("plot")
        elif "off-plan" in i.text.lower():
            type_list.append("off-plan")
        elif "park" in i.text.lower():
            type_list.append("park home")
        elif "mobile" in i.text.lower():
            type_list.append("mobile home")
        else:
            type_list.append("other")


    property_address = browser.find_elements(By.CSS_SELECTOR, ".propertyCard-address")
    for i in property_address:
        address_list.append(i.text)

    property_price = browser.find_elements(By.CSS_SELECTOR, ".propertyCard-priceValue")
    for i in property_price:
        price_list.append(int(i.text.replace("£", "").replace(",", "")))

    property_agent = browser.find_elements(By.CSS_SELECTOR, ".propertyCard-branchSummary")
    for i in property_agent:
        agency_list.append(i.text)

    property_number = browser.find_elements(By.CSS_SELECTOR, ".propertyCard-contactsPhoneNumber")
    for i in property_number:
        number_list.append(i.text)

    property_link = browser.find_elements(By.CSS_SELECTOR, ".propertyCard-link")
    for i in property_link[::2]:
        link_list.append(str(i.get_attribute("href")))
        print(i.get_attribute("href"))






    print(type_raw)
    print(address_list)
    print(price_list)
    print(number_list)
    print(agency_list)
    print()

    next_button = browser.find_element(By.CSS_SELECTOR, ".pagination-button.pagination-direction.pagination-direction--next")
    next_button.click()
    pages_remaining -= 1
    print(pages_remaining)
    print(len(type_raw))
    print(len(link_list))

# for i in agency_list:
#     i.replace("Added today", f"Added on {today_str}")
#     i.replace("Reduced today", f"Reduced on {today_str}")
#     i.replace("Added yesterday", f"Added on {yesterday_str}")
#     i.replace("Reduced yesterday", f"Reduced on {yesterday_str}")
#
# for i in price_list:
#     i.replace("Â", "")

data = {
    "propertyLink": link_list,
    "propertyTypeRaw": type_raw,
    "propertyType": type_list,
    "propertyAddress": address_list,
    "propertyPrice": price_list,
    "propertyAgency": agency_list,
    "propertyNumber": number_list,
}

df = pd.DataFrame(data)
df.to_csv("properties.csv")

print(df)


# def submit_form(data):
#     address = data[0]
#     prices = data[1]
#     links = data[2]
#     s = Service("C:\Development\chromedriver.exe")
#     browser = webdriver.Chrome(service=s)
#     url = 'https://docs.google.com/forms/d/e/1FAIpQLSdZQCTqZP4Xa50_WgGESoSjZnFC12pM_EgSO3fPpRCsHH63OQ/viewform?usp=sf_link'
#     browser.get(url)
#
#     for i in range(0, len(address)-1):
#         sleep(2)
#         address_input = browser.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")
#         address_input.send_keys(address[i])
#         price_input = browser.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")
#         price_input.send_keys(prices[i])
#         link_input = browser.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")
#         link_input.send_keys(links[i])
#         submit_button = browser.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div/span")
#         submit_button.click()
#         new_button = browser.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[4]/a")
#         new_button.click()
#
# submit_form(get_properties())