
from language_utils import Nat_Lang_Proc, Text_Utilities
import json

#NLP = Nat_Lang_Proc(spaCy_core='small')
Text_Util = Text_Utilities()

test_phrase = 'this is the truth'
test_text = 'this is the whole truth about all of us'

result = Text_Util.find_word(test_text, test_phrase)

if result is not None:
    print('found: ', test_phrase)
else:
    print('no')


print('end script')

