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

import pandas as pd
import os

dire = str(os.getcwd())
default_input_path = dire + '\\import_files'

class import_file:
    def __init__(self, input_filename, input_filepath=default_input_path):
        self.input_filename = input_filename
        self.input_filepath = input_filepath

    def read(self):
        
        print('extracting file')

        if '.xlsx' in self.input_filename: #If '.xlsx' is in the filename
            extracted_file = pd.read_excel(f'{self.input_filepath}\\{self.input_filename}', index_col=False) #Extract as excel file
            print("file extracted")
            return extracted_file #Return the file
        
        elif '.csv' in self.input_filename: #If '.csv' is in the filename
            extracted_file = pd.read_csv(f'{self.input_filepath}\\{self.input_filename}', index_col=False, engine='python') #Extract as csv
            print("file extracted")
            return extracted_file #Return the file