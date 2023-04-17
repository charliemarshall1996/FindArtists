from unidecode import unidecode
import re
from spellchecker import SpellChecker
import datetime

#Init spell checker
spell = SpellChecker()

class Normalize:
    def __init__(self):
        pass

    def normalize(self, data, data_type='str', encoding_type=None):

        if data_type == 'date':
            data = self.date(data)
        
        else:
            data_type = data.__class__.__name__

        if data_type == 'str':
            data = self.string(data)
        
        elif data_type == 'int':
            data = self.num(data)

        data = self.encode(data, encoding_type)

        return data
    
    def encode(self, data, encoding_type):
        
        if not encoding_type:
            #Unidecode string
            encoded = unidecode(data)
            print('no encoding')
        
        else:
            encoded = data.encode(encoding_type)
            print('encoded')
        
        print(encoded)
        return encoded

    def string(self, string):
        
        #Put all letters to lower case
        string = string.lower()
        
        #Remove Whitespace
        string = string.strip()

        #Remove punctuation
        string = re.sub(r"[^\w\s]", "", string)
        return string
    
    def date(self, date):
        # Check if the date string is empty.
        if not date:
            return None

        # Check if the date string is in the correct format.
        if len(date) != 8:
            return None

        # Convert the date string to a datetime object.
        date = datetime.datetime(
            year=int(date[:4]),
            month=int(date[4:6]),
            day=int(date[6:]))

        # Return the normalized date string.
        return date.strftime("%Y/%m/%d")

    
    def num(num):
        #CUSTOM NUMBER NORMALISATION FUNCTION HERE
        return num

    def flt(flt):
        #CUSTOM FLOAT NUMBER NORMALISATION FUNCTION HERE
        return flt
    
#normalize = Normalize()

class Present(Normalize):
    
    def __init__(self):

        #List of articles, conjunctions and prepositions 
        #not to be put into title case:
        self.title_exceptions = ['of', 
                    'and', 
                    'but', 
                    'or', 
                    'for', 
                    'yet', 
                    'so', 
                    'a', 
                    'an', 
                    'the']
        
    def title(self, title):

        #Normalize title
        title = self.string(title)

        #Split words to list
        words = title.split()
        
        '''
        #Spell check
        misspelled = spell.unknown(words)

        #Assume closest spelling is correct
        for word in misspelled:
            i = words.index(str(word))
            words[i] = spell.correction(word)
        '''

        #Turn non-exception words in title case
        for word in words:

            #Find corresponding index of word in words list
            i = words.index(str(word))

            #If the word is 'and' and there are no ampersands in the words list, 
            #change the word to ampersand

            if word == 'and' and '&' not in words:
                words[i] = '&'

            #If the word is an exception, leave as lower case.
            if word in self.title_exceptions:
                continue

            #Otherwise, change to title case.
            else:
                words[i] = word.title()

        title = ' '.join(words)
        return title
    
    def job_title(self, job_title):
        return job_title

    def name(self, name):
        return name