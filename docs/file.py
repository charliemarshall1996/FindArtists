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
file.py MANAGES ALL FILE RESPONSIBILITIES OF THE FINDARTISTS APP.
'''


import pandas as pd
import os
from datetime import datetime

dire = str(os.getcwd())
        
class WriteFile:

    def create_df(data):
        
        # CREATE DATAFRAME FROM DATA
        df = pd.DataFrame(data)

        return df

    def write(filename, filepath, df):
        
        # GET DATETIME AS STRING
        date_string = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        
        # DEFINE FULL OUTPUT FILENAME
        full_filename = f'{filename}_{date_string}.csv'
        
        # WRITE THE DATAFRAME TO A .CSV FILE
        df.to_csv(f'{filepath}/{full_filename}', encoding='UTF-8')

        # PRINT TO CONSOLE THAT THE FILE EXPORTED SUCCESSFULLY
        print(full_filename + " exported successfully.")

    def format_df(df):
        
        # JOIN LIST INTO SINGLE STRING
        def join_list(lst):
            return ','.join(map(str, lst))
        
        # MAP DATAFRAME
        df = df.applymap(lambda x: join_list(x) if isinstance(x, list) else x)

class File(WriteFile):

    def write(filename, filepath, data):
        
        # write() TURNS DATA RECEIVED FROM FINDARTISTS INTO A DATAFRAME, PROVIDED BY THE USER
        # FOR USE IN FINDARTISTS.

        # ARGS: 
        # - FILENAME: THE NAME OF THE OUTPUT FILE AS A STRING
        # - FILEPATH: THE DIRECTORY PATH OF THE OUTPUT FILE
        # - DATA: THE DATA TO BE PROCESSED AND OUTPUT

        # RETURNS:
        # - THE FILE OUTPUTTED IN .CSV

        df = WriteFile.create_df(data)
        WriteFile.format_df(df)
        WriteFile.write(filename, filepath, df)

    def read(filename, filepath, sample=False, sample_size=None):

        # read() READS AND RETURNS THE VALUES IN A GIVEN DATA SHEET, PROVIDED BY THE USER
        # FOR USE IN FINDARTISTS.

        # ARGS: 
        # - FILENAME: THE NAME OF THE INPUT FILE AS A STRING
        # - FILEPATH: THE DIRECTORY PATH OF THE INPUT FILE
        # - SAMPLE: WHETHER OR NOT THE USER WANTS TO TAKE A RANDOM SAMPLE FROM THE INPUT FILE
        # - SAMPLE_SIZE: THE SIZE OF THE RANDOM SAMPLE FROM THE INPUT FILE TO BE TAKEN.

        # RETURNS:
        # - DF: THE READ INPUT FILE IN A DATAFRAME FORMAT.

        # IF .XLSX IS IN THE INPUT FILENAME, READ AS .XLSX FILE
        if '.xlsx' in filename:
            df = pd.read_excel(f'{filepath}/{filename}', index_col=False)
            print("file extracted")
        
        # IF .CSV IS IN THE INPUT FILENAME, READ AS .CSV FILE
        elif '.csv' in filename: 
            df = pd.read_csv(f'{filepath}/{filename}', index_col=False, engine='python')
            print("file extracted")
        
        # IF THE USER WANTS A RANDOM SAMPLE
        if sample:
            df = df.sample(n=sample_size)
        
        # RETURN THE OPENED DATAFRAME
        return df