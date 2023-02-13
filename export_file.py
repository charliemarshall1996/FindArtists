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
from datetime import datetime
import os


#Define Default Paths
dire = str(os.getcwd())
default_output_path = dire + '\\FindArtists Exported Files'

class export_file:
    def __init__(self, data, output_filename, output_filepath=default_output_path, ):
        self.data = data
        self.output_filepath = output_filepath
        self.output_filename = output_filename

    def export_main_file(self):
        print("Creating output file.")

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
    
    def export_file(self, df, output_type):
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