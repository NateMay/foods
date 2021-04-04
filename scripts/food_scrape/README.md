# Food Metadata and Nutrition Aggregator

## Required Packages

- requests
- bs4 (BeautifulSoup)
- sqlite3
- flask

## Instructions for Use

### Scraping

- Open `../scrape_wikipedia.py`
- Set all values in the `SHOULD` dictionary to `True`
- Run `python3 manage.py runscript scrape_wikipedia`
- the output goes to `scraped_data.sqlite`

## Inventory

| Variable | Description |
|----------|-------------|
| /page_scripts | Wikipedia scraping logic |
| /wikipedia | Wikipedia requests and caching |
| db.py | SQL database interactions |
| models.py | Data models file |
| pages.py | Organizes Wikipedia page urls to be scraped by type |
| ../scrape_wikipedia.py | Entry point into the scraping flow |
