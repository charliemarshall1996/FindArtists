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
from wikiscraper import Wiki
from file import File
from inventory import data
from tqdm import tqdm
import os

dire = os.getcwd()

# DEFINE INPUT FILE PARAMS
input_filename = f'names_of_artists.csv'
input_filepath = f'{dire}/input'

# DEFINE OUTPUT FILE PARAMS
output_filename = 'FindArtists'
output_filepath = f'{dire}/output'

# DEFINE USER FIELDS

def run(search_by=0):

    if search_by == 0:
        # OPEN THE USER INPUT DATAFRAME
        df = File.read(input_filename, input_filepath, sample=True, sample_size=100)

        # PUT THE COLUMN CALLED 'NAME' TO LIST
        artist_names = df['NAME'].tolist()

    elif search_by == 1:
        artist_names = []
        pass

    elif search_by == 3:
        artist_names = []
        pass

    # SCRAPE WIKIPEDIA TO FIND WIKI IDS
    Wiki.scrape(artist_names)

    # WRITE DATA TO FILE
    File.write(output_filename, output_filepath, data)
    
