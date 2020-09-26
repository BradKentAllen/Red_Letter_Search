
from language_utils import Nat_Lang_Proc, Text_Utilities
from spacy.tokens import Token
import json



test_word = 'prisoner'
print('word: ', test_word)

print('load model')
NLP = Nat_Lang_Proc(spaCy_core='large')
# Text_Util = Text_Utilities()


token_lemma = NLP.get_lemma(test_word)
print('lemma: ', token_lemma)


similar_list = NLP.get_similar_list(test_word, 5)

print('\nsimilar words: ')
for word in similar_list:
    print(word)


print('end script')

