import requests as rq
import json
import pandas as pd
import os
import pywikibot
from pywikibot import exceptions
from datetime import datetime

dire = str(os.getcwd())
print(dire)
default_input_path = dire + '.\\Test_Data'
default_output_path = dire + '.\\FindArtists Exported Files'
default_suppression_path = dire + '.\\Suppression File'


#in_filepath = "/Users/charliemarshall/Desktop/"
in_filename = "names_of_artists.csv"
out_filename = "test"
#out_filepath = ""

class artist_finder:
    def __init__(self, input_filename, output_filename, input_filepath=default_input_path, output_filepath=default_output_path):
        self.input_filename = input_filename
        self.input_filepath = input_filepath
        self.output_filename = output_filename
        self.output_filepath = output_filepath
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
        
        self.data = {"input_name": [], "name": [], "given_name": [], "occupation":  [], 
                           "genre": [], "gender": [], "date_of_birth": [],
                            "year_active_start": [], "year_active_end": [],
                           "native_language": [], "location": [], "album": [],
                           "song": [], "influenced_by": [], "spotify_id": [],
                           "origin": [], "collaborations": [], "allmusic_id": [],
                           "discogs_id": [], "place_of_birth": [], "residence": [], "education": [],                                           
                           "field_of_work": [], "employer": [], "website": [], 
                           "twitter_id": [], "instagram_username": [], 
                           "facebook_id": [], "youtube_id": [], "members": [], 
                           "label": [], "instrument_played": [], "associated_acts": 
                           [], "awards_recieved": [], "notable_work": 
                           [], "musical_group_membership": [], "role_in_musical_group": [],
                            "income": [], "net_worth": [], "income_range": [], 
                           "salary": [], "tax_bracket": [], "net_income": [], 
                           "earnings_per_share": [], "total_assets": [], "revenue": [],
                           "total_equity": []}
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

    def get(self):
        file = self.extract_file()
        self.get_artists(file)
        self.get_artist_wiki_id()
        self.get_wikidata()
        output_df = self.export_main_file()
        self.export_file(output_df, "main")

    def extract_file(self):
        print('extracting file')
        try:
            if '.xlsx' in self.input_filename: #If '.xlsx' is in the filename
                extracted_file = pd.read_excel(f'{self.input_filepath}\\{self.input_filename}', index_col=False) #Extract as excel file
            elif '.csv' in self.input_filename: #If '.csv' is in the filename
                extracted_file = pd.read_csv(f'{self.input_filepath}\\{self.input_filename}', index_col=False, engine='python') #Extract as csv
            print("file extracted")
            return extracted_file #Return the file
        except pd.errors.EmptyDataError:
            print("No data to extract in file:" + self.input_filename)
        except FileNotFoundError as err: #Need to define exception type
            print(err)
            #print('Invalid file. Please check name or filepath:' + self.input_filename)
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
        print('finding artists')
        artists_df = pd.DataFrame(file)
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

    def export_main_file(self):
        print("Creating output file.")
        #Define dictionary
        try:
            for i in self.data:
                print(i + " length: " + str(len(self.data[i])))
            
            #Create Dataframe
            print("Creating output dataframe.")
            df = pd.DataFrame.from_dict(self.data)
            #Export Dataframe
            print("Exporting file.")
            output_type = "main"
            self.export_file(df, output_type)
            return df
        except ValueError as err:
            print("Incorrect value input " + str(err))
    
    def export_file(self, df, output_type):
        try:
            #Get datetime as string
            date_string = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
            if output_type == "main":
                #Create full output filename, using output_filename and date
                full_filename = f'{self.output_filename}_{date_string}.csv'
            elif output_type == "error":
                #Create full output filename, using output_filename and date
                full_filename = f'{self.output_filename}_ERROR_{date_string}.csv'
                #Export to .csv
            df.to_csv(f'{self.output_filepath}\{full_filename}', encoding='UTF-8')
            print(full_filename + " exported successfully.")
        except UnicodeEncodeError as err:
            print("Failed to encode file " + err)
        except ValueError as err:
            print("Incorrect value input. " + err)
            print("Export terminated.")
        except FileExistsError as err:
            print("File Named:" + full_filename + " Already Exists " + err)
        except PermissionError as err:
            print("You do not have permission to save file:" + full_filename + " please check." + err)
        except UnicodeWarning as err:
            print("Unicode Warning:" + err)
        
        


finder = artist_finder(in_filename, out_filename)
print(finder.get())