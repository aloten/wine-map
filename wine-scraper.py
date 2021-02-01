#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Aidan Loten, asloten@gmail.com, 12/31/2020

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re
import csv
import urllib.request


# In[2]:



# Create list to store the text on the wine bottles to search
google_list = []

# Open wine_text_to_search csv and read text into google_list
with open("C:\\Users\\aslot\\miniconda3\\envs\\winemap\\winedata\\wine_text_to_search.csv", 'r') as in_file:
    reader = csv.reader(in_file, delimiter=',')
    for row in reader:
        for cell in row:
            google_list.append(cell)

# Create a dictionary to store data
data = {}
product_list = []
vintage_list = []
producer_list = []
region_list = []
country_list = []
price_list = []
score_list = []
style_list = []
grape_list = []
latitude_list = []
longitude_list = []
img_src_list = []


# Create a new chromedriver
chrome_path = 'C:\\Users\\aslot\\miniconda3\\envs\\winescraper\\chromedriver.exe'
driver = webdriver.Chrome(executable_path=chrome_path)


# In[3]:



def web_scraper(search_string):
    ''' Runs a google search of the search_string, goes to a relevant wine-searcher.com webpage and extracts the relevant text. 
    Appends text to relevant lists.
    '''
    
    # Google Search the text
    driver.get("https://www.google.com")
    search = driver.find_element_by_name('q')
    search.send_keys(search_string)
    search.send_keys(Keys.RETURN) # hit return after you enter search text
    # 5 seconds to manually choose relevant link before next element search runs
    time.sleep(5)
    
#     # Auto-Click on first link, exception below deals with Google Ad interference
#     try:
#         WebDriverWait(driver,10).until(
#        EC.presence_of_element_located((By.XPATH, "(//h3)[1]"))).click() # Click on 1st URL, if no Google ad
#     except:
#         WebDriverWait(driver,10).until(
#        EC.presence_of_element_located((By.XPATH, "(//h3)[2]"))).click() # Click on 1st URL, if yes Google ad


    #################################################
    # Try and navigate to profile tab, except all data = N/A
    try:
        # Navigate to Profile tab
        WebDriverWait(driver,10).until(
           EC.presence_of_element_located((By.XPATH, "//a[@id='find-tab-info']"))).click()

        # Get image of product and append to list
        try:
            img = WebDriverWait(driver,10).until(
               EC.presence_of_element_located((By.XPATH, "//picture[@class='img-fluid rounded']//img")))
            src = img.get_attribute('src')
        except:
            src = 'N/A'

        # Get Product
        try:
            product = WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.XPATH, "//h1/span[@class='text-truncate-2lines']"))).text
        except:
            product = 'N/A'

        # Extract vintage from product if vintage exists
        vint_search = re.search(r'(\d+)\s', product)
        if vint_search:
            vintage = vint_search.group(1)
        else:
            vintage = 'N/A'

        # Get Region
        try:
            region = WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.XPATH, "//h1/span[@class='product-details__product-region-name d-flex align-items-center pt-2']"))).text
        except:
            region = 'N/A'

        # Extract region and country from region text if country is included
        region_search = re.search(r'(.+),\s(.+)', region)
        if region_search:
            region = region_search.group(1)
            country = region_search.group(2)
        else:
            country = region
            region = 'N/A'

        # Get Price
        try:
            price = WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='smaller']/b"))).text
        except:
            price = 'N/A'

        # Get Score
        try:
            score = WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='mr-3 mr-md-4 d-none d-md-block']//span[@class='text-burgundy']/b"))).text
        except:
            score = 'N/A'

        # Get Style
        try:
            style = WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='d-none d-lg-block']//div[@class='text-muted smallish text-uppercase']"))).text[8:]
        except:
            style = 'N/A'

        # Get Producer
        try:
            producer = WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.XPATH, "//a[@class='btn_link']/b"))).text
        except:
            producer = 'N/A'       

        # Add data to respective list
        product_list.append(product)
        producer_list.append(producer)
        vintage_list.append(vintage)
        region_list.append(region)
        country_list.append(country)
        price_list.append(price)
        score_list.append(score)
        style_list.append(style)
        img_src_list.append(src)


        #################################################
        # Navigate to Producer page
        try:
            WebDriverWait(driver,10).until(
               EC.presence_of_element_located((By.XPATH, "//a[@class='btn_link']"))).click()
            # Get vineyard address from producer page
            vineyard_address = driver.find_element_by_xpath('//span[@class="merc-contact"]/span[@itemprop="address"]').text
        except:
            vineyard_address = 'N/A'

        #################################################
        # Navigate to https://www.gps-coordinates.net/, enter address and get gps coordinates
        try:
            driver.get('https://www.gps-coordinates.net/')
            driver.execute_script("window.scrollTo(0, 600)")
            time.sleep(2) # Need time to load auto-address map to clear input_address element properly
            input_address = WebDriverWait(driver,10).until(
                   EC.presence_of_element_located((By.ID,'address')))
            input_address.clear()
            input_address.send_keys(vineyard_address + ', ' + country)
            time.sleep(2)
            input_address.send_keys(Keys.RETURN)
            time.sleep(0.5)
            driver.find_element_by_css_selector('.btn.btn-primary').click()
            time.sleep(2)
            lat_long_text = WebDriverWait(driver,5).until(
                   EC.presence_of_element_located((By.ID,"iwcontent"))).text
            lat_long_search = re.search(r'Latitude: (.+)\s(.)\sLongitude: (.+)\n', lat_long_text)
            lat = lat_long_search.group(1)
            long = lat_long_search.group(3)
        except:
            lat = 'N/A'
            long = 'N/A'

        # Append data to respective lists
        latitude_list.append(lat)
        longitude_list.append(long)
    
    # If can't find profile tab, then the page is wrong and all data = N/A
    except:
        product_list.append('N/A')
        producer_list.append('N/A')
        vintage_list.append('N/A')
        region_list.append('N/A')
        country_list.append('N/A')
        price_list.append('N/A')
        score_list.append('N/A')
        style_list.append('N/A')
        grape_list.append('N/A')
        img_src_list.append('N/A')
        latitude_list.append('N/A')
        longitude_list.append('N/A')


# In[11]:



# Call Web_Scraper(search_string) for wine_text in google_list
for wine_text in google_list:
    search_string_addition = "Wine-Searcher" # hopefully ensures url is of wine-searcher.com
    search_string = search_string_addition + ' ' + wine_text
    web_scraper(search_string)

    
# Quit driver
driver.quit()

# Create a dict of country codes in wine collection (eventually would want to make this dynamic)
country_codes = {'France':'FRA','Germany':'DEU','Italy':'ITA','USA':'USA',
             'Australia':'AUS','New Zealand':'NZL','South Africa':
            'ZAF','Spain':'ESP','Argentina':'ARG','Portugal':'PRT','Chile':'CHL','Great Britain Scotland Northern Ireland England Wales':'GBR','N/A':'N/A'}

# add to code_list for future work merging pandas dataframes using country codes
code_list = []
for i in range(len(country_list)):
    for code_key in country_codes:
        if code_key in country_list[i]:
            code_list.append(country_codes[code_key])
            country_list[i] = code_key

# Download images corresponding to products
img_path_list = []
for i in range(len(img_src_list)):
    filepath = r'C:\Users\aslot\miniconda3\envs\winescraper\wine_images\%s.png' % (product_list[i])
    urllib.request.urlretrieve(img_src_list[i], filepath)
    img_path_list.append(filepath)

# Populate data dictionary
data["product"] = product_list
data["vintage"] = vintage_list
data["producer"] = producer_list
data["region"] = region_list
data["country"] = country_list
data["code"] = code_list
data["avg_price"] = price_list
data["critics_score"] = score_list
data["style"] = style_list
data["latitude"] = latitude_list
data["longitude"] = longitude_list
data["img_path"] = img_path_list



# Write data to CSV file
with open("C:\\Users\\aslot\\miniconda3\\envs\\winemap\\wine_bottles.csv", 'a', newline='') as out_file:
    writer = csv.writer(out_file)
    writer.writerows(zip(*data.values()))




# In[ ]:




