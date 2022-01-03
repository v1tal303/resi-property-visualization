from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import datetime as dt
from compilation import MapPlotter
from geolocate import GeoLocate


today = dt.datetime.now().strftime("%Y-%m-%d")
name = today + input("Please input the name for this file/dataset: ")


print(f"Your file name will be: {name}")

data_type = input(f"Do you want 'detailed' or 'quick' data? ")

print(f"Please select a search criteria through the browser...")

# Selenium URL setup

s = Service("C:\Development\chromedriver.exe")
browser = webdriver.Chrome(service=s)
url = "https://www.rightmove.co.uk/"
browser.get(url)

# Let the user input the search criteria in the browser.

start_condition = False
pages_remaining = 0

while start_condition == False:
    if "find.html" in browser.current_url:
        start_condition = True
        no_of_pages_raw = browser.find_element(By.XPATH, "//*[@id='l-container']/div[3]/div/div/div/div[2]/span[3]")
        pages_remaining = int(no_of_pages_raw.text)
    else:
        start_condition = False

# Preset the list of items to be stored

type_raw = []
type_list = []
address_list = []
price_list = []
agency_list = []
date_list = []
number_list = []
link_list = []
added_date_list = []

# Run this loop when user have specified the search criteria and stop when there are no pages left.

while pages_remaining > 0 and start_condition:
    sleep(2)
    property_type = browser.find_elements(By.CSS_SELECTOR, ".propertyCard-title")
    for i in property_type:
        type_raw.append(i.text)

    property_address = browser.find_elements(By.CSS_SELECTOR, ".propertyCard-address")
    for i in property_address:
        address_list.append(i.text)

    property_price = browser.find_elements(By.CSS_SELECTOR, ".propertyCard-priceValue")
    for i in property_price:
        if "£" in i.text:
            price_list.append(i.text.replace("£", "").replace(",", ""))
        else:
            price_list.append(i.text)

    property_agent = browser.find_elements(By.CSS_SELECTOR, ".propertyCard-branchSummary")
    for i in property_agent:
        agency_list.append(i.text.split("by ", 1)[1])

    date_added = browser.find_elements(By.CSS_SELECTOR, ".propertyCard-branchSummary")
    for i in date_added:
        added_date_list.append(i.text.split("by ", 1)[0])

    property_number = browser.find_elements(By.CSS_SELECTOR, ".propertyCard-contactsPhoneNumber")
    for i in property_number:
        number_list.append(i.text)

    property_link = browser.find_elements(By.CSS_SELECTOR, ".propertyCard-link")
    for i in property_link[::2]:
        link_list.append(str(i.get_attribute("href")))

    next_button = browser.find_element(By.CSS_SELECTOR, ".pagination-button.pagination-direction.pagination-direction--next")
    next_button.click()
    pages_remaining -= 1

if data_type == 'detailed':

    # Preset the list of items to be stored

    key_list = []
    description_list = []
    beds_list = []
    bathroom_list = []
    detail_type_list = []

    # Runs through each link individually and scrapes property type, bedrooms, bathrooms, keys, descriptions. Image scrape could be added later.

    for i in link_list:
        url = i
        browser.get(url)
        sleep(2)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            detail_type_list.append(browser.find_element(By.XPATH,"//*[@id='root']/main/div/div[2]/div/article[2]/div[2]/div[1]/div[2]/div[2]/div").text)
        except:
            try:
                detail_type_list.append(browser.find_element(By.XPATH, "//*[@id='root']/main/div/div[2]/div/article[2]/div[1]/div/div[2]/div[2]/div").text)
            except:
                detail_type_list.append("None")
        try:
            key_list.append(browser.find_element(By.XPATH, "//*[@id='root']/main/div/div[2]/div/article[3]/ul").text)
        except:
            key_list.append("None")
        try:
            beds_list.append(browser.find_element(By.XPATH, "//*[@id='root']/main/div/div[2]/div/article[2]/div[2]/div[2]/div[2]/div[2]/div").text[1])
        except:
            beds_list.append("None")
        try:
            bathroom_list.append(browser.find_element(By.XPATH, "//*[@id='root']/main/div/div[2]/div/article[2]/div[2]/div[3]/div[2]/div[2]/div").text[1])
        except:
            bathroom_list.append("None")
        try:
            readmore_button = browser.find_element(By.XPATH, "//*[@id='root']/main/div/div[2]/div/article[3]/div[3]/button[2]")
            readmore_button.click()
        except:
            pass
        property_desc = browser.find_element(By.XPATH, "//*[@id='root']/main/div/div[2]/div/article[3]/div[3]/div").text
        description_list.append(property_desc)


    # Check the length of the stored data (useful to know what selenium failed to scrape)

    print(f"Links: {len(link_list)}")
    print(f"Date added: {len(added_date_list)}")
    print(f"Types: {len(detail_type_list)}")
    print(f"Bedrooms: {len(beds_list)}")
    print(f"Bathrooms: {len(bathroom_list)}")
    print(f"Address: {len(address_list)}")
    print(f"Price: {len(price_list)}")
    print(f"Agency: {len(agency_list)}")
    print(f"Number: {len(number_list)}")
    print(f"Keys: {len(key_list)}")
    print(f"Description: {len(description_list)}")

    # Store the data into a dictionary and convert to pandas dataframe. Later the scraped information will be saved as a .csv file

    data = {
        "propertyLink": link_list,
        "dateAdded": added_date_list,
        "propertyType": detail_type_list,
        "propertyBeds": beds_list,
        "propertyBathrooms": bathroom_list,
        "propertyAddress": address_list,
        "propertyPrice": price_list,
        "propertyAgency": agency_list,
        "propertyNumber": number_list,
        "dateScraped": dt.datetime.now(),
        "propertyKeys": key_list,
        "propoertyDescription": description_list
    }

    df = pd.DataFrame(data)

else:
    print(f"Links: {len(link_list)}")
    print(f"Date added: {len(added_date_list)}")
    print(f"Types: {len(type_raw)}")
    print(f"Address: {len(address_list)}")
    print(f"Price: {len(price_list)}")
    print(f"Agency: {len(agency_list)}")
    print(f"Number: {len(number_list)}")

    data = {
        "propertyLink": link_list,
        "dateAdded": added_date_list,
        "propertyType": type_raw,
        "propertyAddress": address_list,
        "propertyPrice": price_list,
        "propertyAgency": agency_list,
        "propertyNumber": number_list,
        "dateScraped": dt.datetime.now(),
    }

    df = pd.DataFrame(data)


visualize = input("Do you want to visualize your data? Yes/No: ")

if visualize == 'Yes':
    try:
        print("Please wait, retrieving locations from Google Maps.")
        # Add latitude and longitude with Google Maps API and save as a csv file
        return_locations = GeoLocate(df)
        geo_located = return_locations.locate(name)
        df_located = pd.read_csv(geo_located)
        # Clean prices, latitude, longitude
        nums = pd.to_numeric(df_located['propertyPrice'], errors='coerce')
        clean_num = df_located[(nums.notnull())]
        lat = pd.to_numeric(clean_num['latitude'], errors='coerce')
        clean_lat = clean_num[(lat.notnull())]
        lon = pd.to_numeric(clean_lat['longitude'], errors='coerce')
        clean_lon = clean_lat[(lon.notnull())]
        clean_data = clean_lon.drop(clean_lon.columns[0], axis=1)
        # Generate a folium and branca HTML visualization
        map = MapPlotter(clean_data)
        map.generate_map(f"{name}.html")
        print(f"Your HTML has been saved: {name}.html")
        print(f"Your dataset has been saved: {name}.csv")
    except Exception as e:
        print("There has been an error.")
        print(e)
        df.to_csv(f"{name}.csv")
        print(f"Your scraped data has been saved as {name}.csv")
else:
    df.to_csv(f"{name}.csv")
    print(f"Your file has been saved as {name}.csv")


