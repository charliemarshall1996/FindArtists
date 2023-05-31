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

# IMPORT LIBRARIES
from tqdm import tqdm
from iptk_data import Normalize
from iptk_data import Present
import pywikibot

# INIT NORMALIZE AND PRESENT CLASSES FROM IPTK_DATA.PY
normalize = Normalize()
present = Present()


# CREATE WIKIDATA CLASS
class WikipediaScraper:

    def __init__(self):

        # INIT SITE TO SEARCH
        self.site = pywikibot.Site("en", "wikipedia")

        # INIT ARTIST PAGE DICT
        self.artist_page = {'id': '', 'name': ''}

        # INIT LIST OF ARTIST PAGE DICTS
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

            # IF A NOPAGEERROR IS RETURNED FROM PYWIKIBOT, CONTINUE
            except pywikibot.exceptions.NoPageError:
                continue

            # IF AN INVALIDTITLEERROR IS RETRUNED FROM PYWIKIBOT, CONTINUE
            except (pywikibot.exceptions.InvalidTitleError) as err:
                print(err)
                continue

        # RETURN THE LIST OF ARTIST PAGE DICTIONARIES
        return self.artist_page_list

    def id_cleaner(self, item):

        # TURN THE ITEM TO STRING FORMAT
        item_str = str(item)

        # SPLIT THE STRING ITEMS ON SEMI-COLON INTO LIST
        item_items = item_str.split(":")

        # SELECT THE SECOND ITEM IN THE LIST
        id_half = item_items[1]

        # REMOVE THE SQUARE BRACKETS FROM LIST
        clean_id = id_half.replace("]", "")

        # APPEND THE CLEANED ID TO THE 'WIKI_ID' KEY IN ARTIST PAGE LIST
        self.artist_page['wiki_id'] = id

        # RETURN THE CLEANED ID
        return clean_id
