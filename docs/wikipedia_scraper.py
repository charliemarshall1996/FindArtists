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

import inventory
from tqdm import tqdm
from iptk_data import Normalize
from iptk_data import Present
from pywikibot import exceptions
import pywikibot

normalize = Normalize()
present = Present()



class WikipediaScraper:
    def __init__(self):
        self.site = pywikibot.Site("en", "wikipedia")
        self.artist_page = {'id': '', 'name': ''}
        self.artist_page_list = []
        
    def scrape(self, artists):
        
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
                self.artist_page_list.append(artist_page.copy())
                
                # INCREASE COUNTER BY 1
                counter += 1
                tqdm.write(f'Artists found: {counter}/{total_searches}')

            
            except pywikibot.exceptions.NoPageError:
                continue
            
            except (pywikibot.exceptions.InvalidTitleError) as err:
                print(err)
                continue
        
        return self.artist_page_list

    def id_cleaner(self, item):
        item_str = str(item)
        item_items = item_str.split(":")
        id_half = item_items[1]
        clean_id = id_half.replace("]", "")
        self.artist_page['wiki_id'] = id
        return clean_id 
    
