import wikidata_scraper
import wikipedia_scraper
import file_management
from data_handler import data
from tqdm import tqdm


wikipedia = wikipedia_scraper.WikipediaScraper()
wikidata = wikidata_scraper.WikidataScraper()
write_file = file_management.WriteFile()

def run():
    wikipedia.scrape()
    #print(artist_pages)
    wikidata.scrape()
    write_file.write(data)
