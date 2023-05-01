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
    
    def __init__(self):


        # INIT PROPERTIES DICT WITH CORRESPONDING DATA PROERPTY IDS
        self.properties = {
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

    def scrape(self, artist_pages):
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
            for key, property_id in self.properties.items():
    
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
