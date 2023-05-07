import wikiscraper

artists = ['deadmau5', 'avicii', 'diplo']

artists_wiki_dict_multi = [{'name': 'Deadmau5', 'id': 'Q49009'}, 
                     {'name': 'Avicii', 'id': 'Q505476'}, 
                     {'name': 'Diplo', 'id': 'Q533781'}]

wikipedia = wikiscraper.WikipediaScraper()

def test_wikipedia_scrape(artist_names, artists_wiki_dict):
    assert wikipedia.scrape(artist_names) == artists_wiki_dict
    print('wikipedia scraper passed test')

def test_wikidata_scrape(artists_wiki_dict_multi):
    assert wikiscraper.WikidataScraper.scrape()

test_wikipedia_scrape(artists, artists_wiki_dict_multi)
