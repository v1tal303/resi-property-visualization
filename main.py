import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep

# Get SF properties from Zillow - Address/Price/Link (depreciated as zillow is difficult to webscrape)

def get_properties():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15",
        "Accept-Language": "en-US"
    }
    response = requests.get(
        "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.69219435644531%2C%22east%22%3A-122.17446364355469%2C%22south%22%3A37.703343724016136%2C%22north%22%3A37.847169233586946%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D",
        headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    list_of_links = soup.find_all(class_="list-card-link list-card-link-top-margin", href=True)
    list_of_prices = soup.find_all(class_="list-card-price")
    list_of_address = soup.find_all(class_="list-card-addr")

    prices = [i.getText() for i in list_of_prices]
    address = [i.getText() for i in list_of_address]
    links = ["www.test.com" for i in list_of_prices]
    return [address, prices, links]

# Submit the information into google forms which can be viewed in an excel spreadsheet

def submit_form(data):
    address = data[0]
    prices = data[1]
    links = data[2]
    s = Service("C:\Development\chromedriver.exe")
    browser = webdriver.Chrome(service=s)
    url = 'https://docs.google.com/forms/d/e/1FAIpQLSdZQCTqZP4Xa50_WgGESoSjZnFC12pM_EgSO3fPpRCsHH63OQ/viewform?usp=sf_link'
    browser.get(url)

    for i in range(0, len(address)-1):
        sleep(2)
        address_input = browser.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")
        address_input.send_keys(address[i])
        price_input = browser.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")
        price_input.send_keys(prices[i])
        link_input = browser.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")
        link_input.send_keys(links[i])
        submit_button = browser.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div/span")
        submit_button.click()
        new_button = browser.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[4]/a")
        new_button.click()

submit_form(get_properties())