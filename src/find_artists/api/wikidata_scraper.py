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
        # INIT PROPERTIES DICT WITH CORRESPONDING DATA PROPERTY IDS
        self.properties = {
            # properties dictionary
        }

    def scrape(self, artist_pages):
        values = 0
        for page in tqdm(artist_pages, desc="Searching Artist Data: "):
            id = page['id']
            artist = page['name']
            record = self._search_artist_data(id, artist)
            tqdm.write(f'Total values found {values}.')
            inventory.data.append(record)

    def _search_artist_data(self, id, artist):
        site = pywikibot.Site("wikidata", "wikidata")
        repo = site.data_repository()
        item = pywikibot.ItemPage(repo, id)
        item_dict = item.get()
        record = {'Searched Artist': artist}

        for key, property_id in self.properties.items():
            try:
                clm_list = item_dict["claims"].get(str(property_id), [])
                values += len(clm_list)
                self._process_claims(clm_list, key, record)
                tqdm.write(f'Property {key}, for {artist} found.')
            except (KeyError, AttributeError):
                tqdm.write(f'Property not found {key}')
                record[key] = None

        return record

    def _process_claims(self, clm_list, key, record):
        for clm in clm_list:
            data = self._get_claim_data(clm)
            record[key] = present.title(data)

    def _get_claim_data(self, clm):
        clm_trgt = clm.getTarget()

        if isinstance(clm_trgt, pywikibot.WbTime):
            return self._process_wb_time(clm_trgt)
        elif isinstance(clm_trgt, pywikibot.WbQuantity):
            return self._process_wb_quantity(clm_trgt)
        elif isinstance(clm_trgt, str):
            return normalize.normalize(clm_trgt)
        elif isinstance(clm_trgt, pywikibot.WbMonolingualText):
            return self._process_wb_monolingual_text(clm_trgt)
        else:
            clm_dict = clm_trgt.toJSON()
            return normalize.normalize(clm_dict['labels']['en']['value'])

    def _process_wb_time(self, clm_trgt):
        clm_time = clm_trgt.toTimestamp()
        return normalize.normalize(str(clm_time).split('T')[0], data_type='date')

    def _process_wb_quantity(self, clm_trgt):
        return normalize.normalize(clm_trgt.amount)

    def _process_wb_monolingual_text(self, clm_trgt):
        return normalize.normalize(clm_trgt.text)
