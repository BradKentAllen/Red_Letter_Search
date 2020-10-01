
import re

phrase = 'the scriptures say this'
print(type(phrase))
_word = 'scriptures'
_text = phrase.lower()
if re.search(_word, _text):
    print(phrase)
print('end script')

