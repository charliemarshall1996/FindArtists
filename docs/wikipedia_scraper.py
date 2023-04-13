# FindArtist - Python app to find information on artist and export to a spreadsheet
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

import common
import data_handler
from tqdm import tqdm
from normalize import normalize as normal
from pywikibot import exceptions



class WikipediaScraper:
    def __init__(self):
        self.artist = data_handler.artist_names
        self.site = common.pywikibot.Site("en", "wikipedia")
        self.artist_page = {'id': '', 'name': ''}
        
    def scrape(self):
        counter = 0
        total_searches = len(self.artist)
        for artist in tqdm(self.artist, desc="Searching for artist pages: ", unit="Artists"):
            try:
                site = common.pywikibot.Site("en", "wikipedia")
                page = common.pywikibot.Page(site, f"{artist}")
                item = common.pywikibot.ItemPage.fromPage(page)
                clean_id = self.id_cleaner(item)
                artist = normal(artist)
                artist_page = {'name': artist, 'id': clean_id}
                data_handler.artist_pages.append(artist_page.copy())
                counter += 1
                tqdm.write(f'Artists found: {counter}/{total_searches}')
                #print(f'Found {counter} of {total_searches} artists')
            
            except common.pywikibot.exceptions.NoPageError:
                continue
            
            except (common.pywikibot.exceptions.InvalidTitleError) as err:
                print(err)
                continue

    def id_cleaner(self, item):
        item_str = str(item)
        item_items = item_str.split(":")
        id_half = item_items[1]
        clean_id = id_half.replace("]", "")
        self.artist_page['wiki_id'] = id
        return clean_id
                
    
        
        
