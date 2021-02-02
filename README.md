#Summary
Create a database of wine/spirit collection by scraping the web for each bottle and extracting information. Then produce an interactive Bokeh application that geographically maps data from the wine database to analyze location, price, ratings...etc., by producer.

To see the resulting wine map, download the html file titled 'winemap', which contains an interactive Bokeh application that will open up in your browser. Once the application opens, click the zoom tool on the right hand side to activate the zoom wheel, so you can zoom in to greater detail. You can also click and drag to move the map and hover over the circles for data.

There are two conda environments used, one for each python script



# Steps of the two programs:

# Prep
Create an interactive bokeh application that geographically maps data from a wine collection (organized by producer) to analyze location, price, ratings...etc., of the wine collection. A circle corresponds to the producer/vineyard.

Needs a CSV file 'wine_text_to_search.csv' with as much relevant text as possible from the wine bottle (i.e. label)

# Run wine-scraper.py
Run 'wine-scraper.py': uses a google chrome driver (need to install seperately) powered by Selenium to search google for each text string in 'wine_text_to_search.csv'. This program clicks on the first google link (which should be a wine-searcher.com url) to find the most relevant wine bottle product. It then scrapes the product page for 6 data points and writes to 'wine_bottles.csv'

# Run winemap.py
The next .py file loads 'wine_bottles.csv' and, using geopandas, pandas and bokeh libraries, creates an interactive bokeh geographical map of the relevant data, with zoom, and hover tools. Each circle is a wine producer, and the countries with wine are color coordinated per the color bar

'wine_bottles.csv' also serves as a database for a wine collection. Opening it up as an excel file, write a hyperlink command using the filepath of the images downloaded in 'wine-scraper.py' to link a picture of each wine bottle, add tastings notes etc. in additional columns to the right
