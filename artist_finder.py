# FindArtists - Python app to find information on artists and export to a spreadsheet
# Copyright (C) 2023 Charlie Marshall

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pywikibot
import pandas as pd
import json

class artist_finder:
    def __init__(self, file):
        self.properties = {"name": "P2561", "given_name": "P735", "occupation":  "P106", 
                           "genre": "P136", "gender": "P21", "date_of_birth": "P569",
                           "year_active_start": "P2031", "year_active_end": "P2032",
                           "native_language": "P103", "location": "P276", "album": "P366",
                           "song": "P439", "influenced_by": "P737", "spotify_id": "P1952",
                           "origin": "P495", "collaborations": "P1629", "allmusic_id": "P434",
                           "discogs_id": "P1902", "place_of_birth": "P19", "residence": "P551", "education": "P69", 
                           "employer": "P108", "website": "P856", 
                           "twitter_id": "P2002", "instagram_username": "P2003", 
                           "facebook_id": "P2013", "youtube_id": "P2397", "members": "P527", 
                           "label": "P264", "instrument_played": "P1303", "associated_acts": 
                           "P527", "awards_recieved": "P166", "notable_work": 
                           "P800", "musical_group_membership": "P463", "role_in_musical_group": "P863",
                           "income": "P3529", "net_worth": "P2067", "income_range": "P3530", 
                           "salary": "P2211", "tax_bracket": "P2215", "net_income": "P2129", 
                           "earnings_per_share": "P1082", "total_assets": "P2219", "revenue": "P2131",
                           "total_equity": "P2140"}
        self.data = {
            "input_name": [], 
            "name": [], 
            "given_name": [],
            "gender": [],
            "date_of_birth": [],
            "place_of_birth": [],
            "location": [],
            "origin": [],
            "native_language": [],
            "occupation":  [],
            "musical_group_membership": [],
            "role_in_musical_group": [],
            "members": [], 
            "year_active_start": [], 
            "year_active_end": [],
            "genre": [],
            "influenced_by": [],
            "label": [],
            "instrument_played": [], 
            "associated_acts": [],
            "album": [],
            "song": [],  
            "spotify_id": [], 
            "collaborations": [], 
            "allmusic_id": [],
            "discogs_id": [],  
            "residence": [], 
            "education": [],                                           
            "field_of_work": [], 
            "employer": [], 
            "website": [],
            "facebook_id": [],
            "twitter_id": [],
            "instagram_username": [],
            "youtube_id": [],
            "awards_recieved": [], 
            "notable_work": [],  
            "income": [], 
            "net_worth": [], 
            "income_range": [], 
            "salary": [], 
            "tax_bracket": [], 
            "net_income": [], 
            "earnings_per_share": [], 
            "total_assets": [], 
            "revenue": [],
            "total_equity": []
        }
        self.labels = []
        self.wiki_id = []
        self.artists = []
        self.year_start = []
        self.year_end = []
        self.genres = []
        self.instruments = []
        self.name = []
        self.place_of_birth = []
        self.site = pywikibot.Site("en", "wikipedia")
        self.file = file

    def get(self):
        self.find_artists()
        self.get_artist_wiki_id()
        self.get_wikidata()
        return self.data


    def find_artists(self):
        print('finding artists')
        artists_df = pd.DataFrame(self.file)
        for row in artists_df.itertuples():
            artist = row[1]
            self.artists.append(artist)
            self.data["input_name"] += artist
        print("artists found")

    def get_artist_wiki_id(self):
        for artist in self.artists:
            try:
                site = pywikibot.Site("en", "wikipedia")
                page = pywikibot.Page(site, f"{artist}")
                item = pywikibot.ItemPage.fromPage(page)
                code = self.get_wiki_id(item)
                self.wiki_id.append(code)
                print(f"Page for {artist} found: {code}")
            except pywikibot.exceptions.NoPageError:
                print("Artist Not Found: " + artist)
                pass

    def get_wiki_id(self, item):
        item_str = str(item)
        item_items = item_str.split(":")
        code_half = item_items[1]
        code = code_half.replace("]", "")
        return code
    
    def get_wikidata(self):
        for id in self.wiki_id:
            site = pywikibot.Site("wikidata", "wikidata")
            repo = site.data_repository()
            item = pywikibot.ItemPage(repo, f"{id}")
            print(item)
            item_dict = item.get()
            clm_dict = item_dict["claims"]
            for key in self.properties:
               prop = self.properties[key]
               self.get_property(prop, key, clm_dict)
                
    def get_property(self, property, key, dict):
        values_list = []
        try:
            clm_list = dict[f"{property}"]   
            try:
                for clm in clm_list:
                    clm_trgt = clm.getTarget()
                    labels = clm_trgt.toJSON()
                    languages = labels['labels']
                    english = languages['en']
                    value = english['value']
                    values_list.append(value)

            except AttributeError:
                try:
                    for clm in clm_list:
                        clm_trgt = clm.getTarget()
                        print(dir(clm_trgt))
                        timestamp = clm_trgt.toTimestamp()
                        timestring = str(timestamp)
                        date_split = timestring.split('T')
                        value = date_split[0]
                        values_list.append(value)
                except AttributeError:
                    try:
                        for clm in clm_list:
                            clm_trgt = clm.getTarget()
                            values_list.append(clm_trgt)
                    except:
                        values_list.append('NULL')
                        pass
        except KeyError:
            values_list.append('NULL')
            pass
        
        print(values_list)
        self.data[key] += values_list
        
        
