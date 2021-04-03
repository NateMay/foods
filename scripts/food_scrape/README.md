# Food Metadata and Nutrition Aggregator

## Required Packages

- requests
- bs4 (BeautifulSoup)
- sqlite3
- flask

## Instructions for Use

### Scraping

- Open `scrape_wikipedia.py`
- Set all values in the `SHOULD` dictionary to `True`
- Run `python scrape_wikipedia.py` from the project root directory

### Flask Application

- Obtain a Food Data Central [API key](https://fdc.nal.usda.gov/api-key-signup.html)
- Create `fdc/secrets.py` and add `FDC_API = 'XXXXXX'` replace your API Key
- Run `python app.py` from the project root directory
- Open `localhost:5000` in a web browser
- Type a food name in the search bar
- Select the item you're looking for from the resulting table
- Select the fdc item from the resulting table
- Click "Connect" if you wish to make a connection

## Inventory

| Variable | Description |
|----------|-------------|
| /fdc | USDA nutrition database requests and caching |
| /page_scripts | Wikipedia scraping logic |
| /templates | flask HTML and templating files |
| /wikipedia | Wikipedia requests and caching |
| app.py | Entry point and routing logic for the Flask app |
| db.py | SQL database interactions |
| models.py | Data models file |
| pages.py | Organizes Wikipedia page urls to be scraped by type |
| scrape.py | Entry point into the scraping flow |
