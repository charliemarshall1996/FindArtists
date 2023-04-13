import unicodedata
from unidecode import unidecode


def normalize(string):
    #Put all letters to lower case
    string = string.lower()
    #Remove Whitespace
    string = string.strip()
    #Unidecode string
    string = unidecode(string)
    #Normalize unicode
    string = unicodedata.normalize('NFKD', string)
    return string

def tidy(string):
    title_exceptions = ['of', 'and', 'but', 'or', 'for', 'yet', 'so', 'a', 'an', 'the']
    
    string = normalize(string)

    words = string.split()
    new_string = ''

    for word in words:
        
        if title_exceptions.find(word):
            continue
        else:
            word = word.title()

        new_string.append(word + ' ')

    return new_string.strip()
