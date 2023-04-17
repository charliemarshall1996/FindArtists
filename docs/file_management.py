# FindArtists - Python app to find information on artists and export to a spreadsheet
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

dire = str(common.os.getcwd())

input_filename = f'\\docs\\names_of_artists.csv'
input_filepath = dire
output_filename = 'FindArtists'
output_filepath = dire

class ReadFile:
    def read(self, sample=False, sample_size=None):

        if '.xlsx' in input_filename: #If '.xlsx' is in the filename
            extracted_file = common.pandas.read_excel(f'{input_filepath}\\{input_filename}', index_col=False) #Extract as excel file
            print("file extracted")
        
        elif '.csv' in input_filename: #If '.csv' is in the filename
            extracted_file = common.pandas.read_csv(f'{input_filepath}\\{input_filename}', index_col=False, engine='python') #Extract as csv
            print("file extracted")
        
        #If user wants to choose a random sample
        if sample:
            extracted_file = extracted_file.sample(n=sample_size)

        artist_names = extracted_file['NAME'].tolist()
        
        return artist_names
        

        

class WriteFile:
    def write(self, data):
        self.create_df(data)
        self.format_df()
        self.export()

    def create_df(self, data):
        print("Creating output dataframe.")
        self.df = common.pandas.DataFrame(data)

    def export(self):
        #Get datetime as string
        date_string = str(common.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        full_filename = f'{output_filename}_{date_string}.csv'
        self.formatted_df.to_csv(f'{output_filepath}\{full_filename}', encoding='UTF-8')
        print(full_filename + " exported successfully.")

    def format_df(self):
        def join_list(lst):
            return ','.join(map(str, lst))
        self.formatted_df = self.df.applymap(lambda x: join_list(x) if isinstance(x, list) else x)