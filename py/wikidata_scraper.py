import common
import data_handler
from tqdm import tqdm
from normalize import normalize as normal

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

    def scrape(self):
        values = 0
        
        #Iterate through artist pages
        for page in tqdm(data_handler.artist_pages, desc="Searching Artist Data: "):
            
            id = page['id']
            artist = page['name']
            
            site = common.pywikibot.Site("wikidata", "wikidata")
            repo = site.data_repository()
            item = common.pywikibot.ItemPage(repo, id)
            item_dict = item.get()
            clm_dict = item_dict['claims']
            
            record = {}
            record['Searched Artist'] = artist
            #Iterate through each of the defined properties
            for key, property_id in self.properties.items():
    
                try:
                    item_dict = item.get()
                    clm_dict = item_dict["claims"]  
                    #print(f"Processing property {key}")
                    clm_list = clm_dict[str(property_id)]
                    values += 1
                    
                    for clm in clm_list:
                        clm_trgt = clm.getTarget()
                        
                        #If it's a WbTime data type
                        if isinstance(clm_trgt, common.pywikibot.WbTime):
                            clm_time = clm_trgt.toTimestamp()
                            record[key] = normal(str(clm_time).split('T')[0])
                        
                        elif isinstance(clm_trgt, common.pywikibot.WbQuantity):
                            record[key] = normal(clm_trgt.amount)
                        
                        elif isinstance(clm_trgt, str):
                            record[key] = normal(clm_trgt)
                        
                        elif isinstance(clm_trgt, common.pywikibot.WbMonolingualText):
                            record[key] = normal(clm_trgt.text)

                        else:
                            clm_dict = clm_trgt.toJSON()
                            record[key] = normal(clm_dict['labels']['en']['value'])
                    tqdm.write(f'Property {key}, for {artist} found.')
                    
                
                #If property can't be found, set value in record dict to None
                except (KeyError, TypeError, AttributeError):
                    tqdm.write(f'Property not found {key}')
                    record[key] = None
                    continue
            
            tqdm.write(f'Total values found {values}.')
            data_handler.data.append(record)
