# Residential Property Visualization

UK housing market has hit a new record high of £254,822 in December 2021 which is an increase of 10.4% over the year and a largest annual increase since 2006.

<code>Property visualizer</code> is a simple Python interface that allows the user to scrape currently listed properties from a website, store them in Pandas dataframe which can be visualized as a dot map with Google API, Branca and Folium.

## How it works

<img src = "./doc_images/HowitWorks_1.jpg">

## How to use

1) Install <a href="https://chromedriver.chromium.org/getting-started">selenium webdriver for chrome</a> and place it in C:\Development\chromedriver.exe

<img src = "./doc_images/seleniumsetup.jpg">

2) To enable visualization feature, Google Geolocate API key will be required. Please provide a key in <code>geolocate.py</code>

3) Run <code>main.py</code> and select if you want detailed (includes no. bathrooms, bedrooms, keys, descriptions) or quick run.

<img src = "./doc_images/userinput.jpg">

<img src = "./doc_images/quickdata.jpg">

<img src = "./doc_images/longdata.jpg">

4) After the initial setup, a browser will open where you can search for any listings you want. (Please note, currently visualization feature only works with "For Sale" properties)

<img src = "./doc_images/websitesearch.jpg">

5) When the search is complete, the csv (and html file if visualization was requested) will be saved on your computer.

<img src = "./doc_images/visualization.jpg">

## Disclaimer

As per the terms and conditions of some websites such as <a href="https://www.rightmove.co.uk/this-site/terms-of-use.html"> this</a> any use of webscrapers, spiders, crawlers or any automated programs is unauthorised, therefore do not use this script.
