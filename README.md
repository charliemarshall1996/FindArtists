# FindArtists
Finds information on musicians and recording artists using pywikibot.

## Description

FindArtists is a Python application that uses the Pywikibot library to find information on musicians and recording artists from Wikipedia.

## Prerequisites
+ Python 3.6 or higher
+ Pywikibot library
+ Padas Library

## Installation
+ Clone the repository or download the source code.
+ Install Pywikibot library using pip: pip install pywikibot pandas

## How to Use
1. Prepare an input spreadsheet containing the artist names. The spreadsheet should have a header row with a column named "Name".
2. Open a terminal window and navigate to the directory containing the FindArtists.py file.
3. Run the command python FindArtists.py.
4. Enter the filename of the input spreadsheet, or press enter to use the default path.
5. Enter the filename for the output spreadsheet, or press enter to use the default path.
6. The application will search Wikipedia and Wikidata for each artist in the input spreadsheet and export artist information to the output spreadsheet.

## Output Spreadsheet Fields
+ Input Name - the name of the artist searched for, from the initial input file
+ Name
+ Given Name
+ Occupation
+ Genre
+ Gender
+ Date of Birth
+ Year Active Start
+ Year Active End
+ Native Language
+ Location
+ Album
+ Song
+ Influenced By
+ Spotify ID
+ Origin
+ Collaborations
+ AllMusic ID
+ Discogs ID
+ Place of Birth
+ Residence
+ Education
+ Field of Work
+ Employer
+ Website
+ Twitter ID
+ Instagram Username
+ Facebook ID
+ YouTube ID
+ Members
+ Label
+ Instrument Played
+ Associated Acts
+ Awards Recieved
+ Notable Work
+ Musical Group Membership
+ Role in Musical Group
+ Income
+ Net Worth
+ Income Range
+ Salary
+ Tax Bracket
+ Net Income
+ Earnings per Share
+ Total Assets
+ Revenue
+ Total Equity


## Features
+ Imports from CSV
+ Exports to CSV
+ Custom export file location
+ Custom export filename

## License
