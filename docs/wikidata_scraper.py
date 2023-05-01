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



import inventory
from tqdm import tqdm
from iptk_data import Normalize
from iptk_data import Present
import pywikibot

normalize = Normalize()
present = Present()

class WikidataScraper:
    
    def __init__(self):
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
        values = 0
        
        # Iterate through artist pages
        for page in tqdm(artist_pages, desc="Searching Artist Data: "):
            
            id = page['id']
            artist = page['name']
            
            site = pywikibot.Site("wikidata", "wikidata")
            repo = site.data_repository()
            item = pywikibot.ItemPage(repo, id)
            item_dict = item.get()
            clm_dict = item_dict['claims']
            
            record = {}
            record['Searched Artist'] = artist
            
            # Iterate through and retrieve each of the defined properties
            for key, property_id in self.properties.items():
    
                try:

                    item_dict = item.get()
                    clm_dict = item_dict["claims"]  
                    clm_list = clm_dict[str(property_id)]
                    values += 1
                    
                    for clm in clm_list:

                        clm_trgt = clm.getTarget()
                        
                        #Set the appropriate data type and format for the received value
                        
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

                        # Otherwise    
                        else:
                            clm_dict = clm_trgt.toJSON()
                            data = normalize.normalize(clm_dict['labels']['en']['value'])
                            record[key] = present.title(data)

                        
                    
                    tqdm.write(f'Property {key}, for {artist} found.')
                    
                
                #If property can't be found, or is otherwise erronious, set value in record dict to None
                except (KeyError, AttributeError):
                    tqdm.write(f'Property not found {key}')
                    record[key] = None
                    continue
            
            tqdm.write(f'Total values found {values}.')
            inventory.data.append(record)
