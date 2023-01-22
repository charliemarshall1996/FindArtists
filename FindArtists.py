import requests as rq
import json
import pandas as pd
import os
import pywikibot

dire = str(os.getcwd())
default_input_path = dire + '.\\Test Data'
default_output_path = dire + '.\\FindArtists Exported Files'
default_suppression_path = dire + '.\\Suppression File'


#in_filepath = "/Users/charliemarshall/Desktop/"
in_filename = "names_of_artists.csv"
out_filename = ""
out_filepath = ""
properties = ["P495", "P2218", "P1303", "P264", "P856", "P21", "P2301", "P2302", "P19", "P569", "P136", "P2561", ]

class artist_finder:
    def __init__(self, input_filename, output_filename, properties, input_filepath=default_input_path, output_filepath=default_output_path):
        self.input_filename = input_filename
        self.input_filepath = input_filepath
        self.output_filename = output_filename
        self.output_filepath = output_filepath
        self.properties = properties
        self.artists = []
        self.year_start = []
        self.year_end = []
        self.genres = []
        self.instruments = []
        self.name = []
        self.place_of_birth = []
        self.site = pywikibot.Site("en", "wikipedia")

    def get(self):
        file = self.extract_file()
        self.get_artists(file)

    def extract_file(self):
        try:
            if '.xlsx' in self.input_filename: #If '.xlsx' is in the filename
                extracted_file = pd.read_excel(f'{self.input_filepath}\\{self.input_filename}', index_col=False) #Extract as excel file
            elif '.csv' in self.input_filename: #If '.csv' is in the filename
                extracted_file = pd.read_csv(f'{self.input_filepath}\\{self.input_filename}', index_col=False, engine='python') #Extract as csv
            return extracted_file #Return the file
        except pd.errors.EmptyDataError:
            print("No data to extract in file:" + self.input_filename)
        except FileNotFoundError: #Need to define exception type
            print('Invalid file. Please check name or filepath:' + self.input_filename)
        except pd.errors.PerformanceWarning as err:
            print("Potential performance impact:" + self.input_filename + " " + str(err))
        except pd.errors.ParserError as err:
            print("Error parsing file:" + self.input_filename + " " + str(err))
        except pd.errors.DtypeWarning as err:
            print("Input file contains multiple data types in single column:" + self.input_filename + " " + str(err))
        except UnicodeDecodeError as err:
            print("Error extracting file:" + self.input_filename + " " + str(err))
        except:
            print("Unknow Error, please contact developer:" + self.input_filename)

    def get_artists(self, file):
        artists_df = pd.DataFrame(file)
        for row in artists_df.itertuples():
            artist = row[1]
            self.artists.append(artist)

    def get_artist_wiki_id(self, artist):
        for artist in self.artists:
            page = pywikibot.Page(self.site, {artist})
            item = pywikibot.ItemPage.fromPage(page)
            print(item)


finder = artist_finder(in_filename, out_filename, properties, out_filepath)
print(finder.get())