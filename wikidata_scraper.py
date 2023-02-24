import common
import data_handler
from tqdm import tqdm

class WikidataScraper:
    
    def __init__(self):
        self.properties = {"name": "P2561", 
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

        for page in tqdm(data_handler.artist_pages, desc="Searching Artist Data: "):
            id = page['id']
            
            site = common.pywikibot.Site("wikidata", "wikidata")
            repo = site.data_repository()
            item = common.pywikibot.ItemPage(repo, id)
            item_dict = item.get()
            record = {}
        
            values = 0
            for key, property_id in self.properties.items():
                try:
                    if property_id in item_dict["claims"]:
                        claim = item_dict["claims"][property_id][0]
                        
                        if claim.target:
                            values += 1
                            if claim.target.__class__.__name__ == "Time":
                                # Split datetime values on 'T' and extract only the date
                                date_string = claim.target.toTimestr().split('T')[0]
                                record[key] = date_string
                            else:
                                record[key] = claim.target
                            
                    tqdm.write(f'Total values found {values}')
                except (KeyError, TypeError):
                    record[key] = None
       
            data_handler.data.append(record)
