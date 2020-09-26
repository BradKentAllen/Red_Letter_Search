# Bible tool

import nltk

# import different varieties of tokenizers
from nltk.tokenize import word_tokenize   # words
from nltk.tokenize import sent_tokenize   # sentences
from nltk.tokenize import WordPunctTokenizer   # word punctuation

# stemmers convert words to basic forms
from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.snowball import SnowballStemmer

# Lemmanization is similar to stemming but more thorough
from nltk.stem import WordNetLemmatizer

OTbooks = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges',
    'Ruth', '1 Samuel', '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles',
    'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon',
    'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos',
    'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi']

NTbooks = ['Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians',
    'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians',
    '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter',
    '1 John', '2 John', '3 John', 'Jude', 'Revelation']    

ignoreNoteList = [' a ', ' b ',  'c ', ' d ', ' e ', ' f ', ' g ', ' h ', ' i ',
    ' j ', ' k ', ' l ', ' m ', ' n ', ' o ', ' p ', ' q ', ' r ', ' s ', ' t ', ' u ', ' v ', ' w ', ' x ', ' y ', 'z']


print('start Bible Tool 1')

# read Bible text
BibleFile = 'ESVtestTEXT.txt'
file = open(BibleFile)
Bible = file.read()
print(Bible)


# word tokenize
tokenizer = WordPunctTokenizer()
tokenList = tokenizer.tokenize(Bible)

# sentence tokenize
print(sent_tokenize(Bible))

grammar = "NP:{<DT>?<JJ>*<NN>}"
parser_chunking = nltk.RegexpParser(grammar)

#parsedText = parser_chunking.parse(tokenList)



print('done')