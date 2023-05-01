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

main.py STORES THE CORE LOGIC OF THE FINDARTISTS APP. IT COMPILES ALL OTHER MODULES, IN ORDER TO PROVIDE
A COHEISVE AND EFFICIENT APPLICATION.

IT USES USER-DEFINED INPUTS TO INFORM THE FUNCTIONING OF THE APPLICATION.

ARGS: SEARCH-BY (GENRE, ARTIST NAME, LOCATION, GENRE & LOCATION), 

RETURNS: DATASHEET WITH DESIRED FIELDS

'''

import wikidata_scraper
import wikipedia_scraper
from file import File
from inventory import data
from tqdm import tqdm
import os

dire = os.getcwd()

input_filename = f'names_of_artists.xlsx'
input_filepath = f'{dire}/input'
output_filename = 'FindArtists'
output_filepath = f'{dire}/output'

wikipedia = wikipedia_scraper.WikipediaScraper()
wikidata = wikidata_scraper.WikidataScraper()

def run():

    # OPEN THE USER INPUT DATAFRAME
    df = File.read(input_filename, input_filepath, sample=True, sample_size=100)

    # PUT THE COLUMN CALLED 'NAME' TO LIST
    artist_names = df['NAME'].tolist()

    # SCRAPE WIKIPEDIA TO FIND WIKI IDS
    artist_wiki_pages = wikipedia.scrape(artist_names)

    # SCRAPE WIKIPEDIA TO FIND ARTIST DATA
    wikidata.scrape(artist_wiki_pages)

    # WRITE DATA TO FILE
    File.write(output_filename, output_filepath, data)
    
