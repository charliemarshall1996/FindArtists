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