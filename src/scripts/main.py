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

import argparse
from file import File
from cache import Cache

def main():
    parser = argparse.ArgumentParser(description='Find artists in a file')
    parser.add_argument('filename', metavar='filename', type=str, help='File containing artist names')
    parser.add_argument('filepath', metavar='filepath', type=str, help='Path to file containing artists names')
    parser.add_argument('output_filename', metavar='output_filename', type=str, help='Desired name for output file')
    parser.add_argument('output_filepath', metavar='output_filepath', type=str, help='Desired output path')
    args = parser.parse_args()

    artist_names = File.read(args.filename, args.filepath)
    # Call your package function to search for artists based on the input file
    artist_results = find_artists(artist_names)

    if args.cache:
        save_artists_to_cache(artist_results)

def find_artists(artist_names):
    
    pass
