# Copyright (c) 2023, Charlie Marshall

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


'''
wikidata_scraper.py - This module retrieves data from specified wikidata pages, 
which correspond to specific wikipedia pages as found in wikipedia_scraper.py.

'''

all_valid_properties = {
                "name": "P2561", 
                "given_name": "P735", 
                "occupation": "P106", 
                "genre": "P136", 
                "gender": "P21", 
                "date_of_birth": "P569",
                "year_active_start": "P2031", 
                "year_active_end": "P2032",
                "native_language": "P103",
                "location": "P276", 
                "album": "P366",
                "song": "P439", 
                "influenced_by": "P737", 
                "spotify_id": "P1952",
                "origin": "P495", 
                "collaborations": "P1629", 
                "allmusic_id": "P434",
                "discogs_id": "P1902", 
                "place_of_birth": "P19", 
                "residence": "P551", 
                "education": "P69", 
                "employer": "P108", 
                "website": "P856", 
                "twitter_id": "P2002", 
                "instagram_username": "P2003", 
                "facebook_id": "P2013", 
                "youtube_id": "P2397", 
                "members": "P527", 
                "label": "P264", 
                "instrument_played": "P1303", 
                "associated_acts": "P527", 
                "awards_recieved": "P166", 
                "notable_work": "P800", 
                "musical_group_membership": "P463", 
                "role_in_musical_group": "P863",
                "income": "P3529", 
                "net_worth": "P2067", 
                "income_range": "P3530", 
                "salary": "P2211", 
                "tax_bracket": "P2215", 
                "net_income": "P2129", 
                "earnings_per_share": "P1082", 
                "total_assets": "P2219", 
                "revenue": "P2131",
                "total_equity": "P2140"}


# IMPORT LIBRARIES
import inventory
from tqdm import tqdm
from iptk_data import Normalize
from iptk_data import Present
import pywikibot

# INIT NORMALIZE AND PRESENT CLASSES FROM IPTK_DATA.PY
normalize = Normalize()
present = Present()

# WIKIDATA SCRAPER CLASS
class WikidataScraper:
    
    '''
    wikidata_scraper.py - This module retrieves data from specified wikidata pages, 
    which correspond to specific wikipedia pages as found in wikipedia_scraper.py.

    '''

    def scrape(artist_pages, properties):
        # scrape() - CORE LOGIC OF WIKIDATA SCRAPER CLASS
        # ARGS:
        # - SELF
        # - artist_pages: THE WIKIDATA ID OF THE MUSICAL ARTISTS TO FIND DATA ON
        # 
        # RETURNS: FOUND DATA POINTS, PLACED IN DICT FORMAT AND APPENDED TO LIST WITHIN
        # INVENTORY.PY
        
        # INIT VALUES COUNTER TO ZERO
        values = 0
        
        # ITERATE THROUGH ARTIST PAGE IDS
        for page in tqdm(artist_pages, desc="Searching Artist Data: "):
            
            # DEFINE PAGE ID VARIABLE
            id = page['id']

            # DEFINE ARTIST NAME VARIABLE
            artist = page['name']
            
            # INIT WIKIBOT TO SEARCH WIKIDATA SITE
            site = pywikibot.Site("wikidata", "wikidata")

            # INIT DATA REPO VARIABLE
            repo = site.data_repository()

            # DEFINE THE WIKIDATA PAGE TO FIND
            item = pywikibot.ItemPage(repo, id)

            # RETRIEVE WIKIDATA PAGE
            item_dict = item.get()

            # EXTRACT THE CLAIMS DICT FROM RETURNED DICT
            clm_dict = item_dict['claims']
            
            # INIT ARTIST RECORD DICT
            record = {}

            # SET 'SEARCHED ARTIST' RECORD FIELD TO THE ARTIST NAME
            record['Searched Artist'] = artist
            
            # RETRIEVE WIKIDATA PAGE
            item_dict = item.get()

            # RETRIEVE THE DEFINED PROPERTIES ON THE ARTIST PAGE
            for key, property_id in properties.items():
    
                try:
                    # RETRIEVE CLAIMS DICT FROM WIKIDATA PAGE DICT
                    clm_dict = item_dict["claims"] 

                    # FIND VALUES IN CLAIMS DICT WITH CORRESPONDING PROERTY ID
                    # PUT FOUND VALUES TO LIST
                    clm_list = clm_dict[str(property_id)]

                    # INTEGER THE VALUES COUNTER BY ONE
                    values += 1
                    
                    # ITERATE THROUGH EACH OF THE FOUND CLAIMS
                    for clm in clm_list:

                        # RETRIEVE THE TARGET FROM THE CLAIM
                        clm_trgt = clm.getTarget()
                        
                        # FORMAT DATA BASED ON DATA TYPE
                        
                        # If WbTime
                        if isinstance(clm_trgt, pywikibot.WbTime):
                            clm_time = clm_trgt.toTimestamp()
                            data = str(clm_time).split('T')[0]
                            record[key] = normalize.normalize(data, data_type='date')
                            continue
                        
                        # If WbQuantity
                        elif isinstance(clm_trgt, pywikibot.WbQuantity):
                            data = normalize.normalize(clm_trgt.amount)
                            record[key] = present.title(data)
                        
                        # If String
                        elif isinstance(clm_trgt, str):
                            data = normalize.normalize(clm_trgt)
                            record[key] = present.title(data)
                        
                        # If MonoLingualText
                        elif isinstance(clm_trgt, pywikibot.WbMonolingualText):
                            data = normalize.normalize(clm_trgt.text)
                            record[key] = present.title(data)

                        # Otherwise assume JSON  
                        else:
                            clm_dict = clm_trgt.toJSON()
                            data = normalize.normalize(clm_dict['labels']['en']['value'])
                            record[key] = present.title(data)      
                
                # IF SEARCHING FOR PROPERTY RAISES KEYERROR
                # OR ATTRIBUTEERROR, 
                # SET THE DICTIONARY PROPERTY VALUE TO NONE
                except (KeyError, AttributeError):
                    tqdm.write(f'Property not found {key}')
                    record[key] = None
                    continue

                # PRINT IF PROERTY FOR ARTIST WAS FOUND TO TERMINAL
                tqdm.write(f'Property {key}, for {artist} found.')
            
            # PRINT THE TOTAL VALUES FOUND TO TERMINAL
            tqdm.write(f'Total values found {values}.')
            
            # APPEND THE FULL RECORD PROPERTY TO TERMINAL
            inventory.data.append(record)

# WIKIPEDIA SCRAPER CLASS
class WikipediaScraper:
    
    def __init__(self):
        pass

    def scrape(self, artists):
        
        # INIT ARTIST PAGE DICT
        artist_page = {'id': '', 'name': ''}

        # INIT LIST OF ARTIST PAGE DICTS
        artist_page_list = []

        # COUNTER TO KEEP TRACK OF NUMBER OF ARTISTS FOUND
        counter = 0

        # FIND THE TOTAL NUMBER OF ARTISTS TO FIND WIKIPEDIA PAGES FOR
        total_searches = len(artists)

        # LOOP THROUGH EACH OF THE ARTISTS
        for artist in tqdm(artists, desc="Searching for artist pages: ", unit="Artists"):
            try:
                # NORMALIZE THE ARTIST NAME
                artist = normalize.normalize(artist)
                
                # DEFINE THE PYWIKIBOT SITE TO SEARCH
                site = pywikibot.Site("en", "wikipedia")

                # RECEIVE WIKIPEDIA PAGE FROM PYWIKIBOT, THAT CORRESPONDS TO THE ARTIST
                page = pywikibot.Page(site, f"{artist}")

                # FIND WIKIPEDIA PAGE ID
                item = pywikibot.ItemPage.fromPage(page)

                # CLEAN WIKIPEDIA PAGE ID
                clean_id = self.id_cleaner(item)
                
                # CLEAN ARTIST NAME
                artist = present.title(artist)

                # CREATE DICTIONARY FOR THE ARTIST PAGE
                artist_page = {'name': artist, 'id': clean_id}

                # APPEND THE ARTIST PAGE TO ARTIST PAGES LIST
                artist_page_list.append(artist_page.copy())
                
                # INCREASE COUNTER BY 1
                counter += 1
                tqdm.write(f'Artists found: {counter}/{total_searches}')

            # IF A NOPAGEERROR IS RETURNED FROM PYWIKIBOT, CONTINUE
            except pywikibot.exceptions.NoPageError:
                continue
            
            # IF AN INVALIDTITLEERROR IS RETRUNED FROM PYWIKIBOT, CONTINUE
            except (pywikibot.exceptions.InvalidTitleError) as err:
                print(err)
                continue
        
        # RETURN THE LIST OF ARTIST PAGE DICTIONARIES
        return artist_page_list

    def id_cleaner(self, item):
        
        # TURN THE ITEM TO STRING FORMAT
        item_str = str(item)

        # SPLIT THE STRING ITEMS ON SEMI-COLON INTO LIST
        item_items = item_str.split(":")
        
        # SELECT THE SECOND ITEM IN THE LIST
        id_half = item_items[1]
        
        # REMOVE THE SQUARE BRACKETS FROM LIST
        clean_id = id_half.replace("]", "")

        # RETURN THE CLEANED ID
        return clean_id 
    
# WIKI MAIN LOGIC
class Wiki(WikipediaScraper, WikidataScraper):

    def scrape(artist_names, fields=all_valid_properties):
        wikipedia = WikipediaScraper()
        wiki_pages = wikipedia.scrape(artist_names)
        WikidataScraper.scrape(wiki_pages, fields)