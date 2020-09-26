
from language_utils import Nat_Lang_Proc, Text_Utilities
from RL_Bible
import json

NLP = Nat_Lang_Proc(spaCy_core='small')

test_sentence = 'Jesus is Lord of Israel. He loves us'

# dictionary with word and ranking score
search_dict = {}

entities = NLP.get_entities(test_sentence)
for entity in entities:
    if entity[1] == 'PERSON':
        if entity[0].text not in search_dict:
            search_dict[entity[0].text] = 5
    elif entity[1] == 'GPE':
        if entity[0].text not in search_dict:
            search_dict[entity[0].text] = 3

tokenized = NLP.return_sentence_list(test_sentence, tokenize=True)
for token_list in tokenized:
    for token in token_list:
        print(token[0], ' - ', token[2])
        if token[2] == 'PROPN':
            if token[0].text not in search_dict:
                search_dict[token[0].text] = 1
        elif token[2] == 'VERB':
            if token[0].text not in search_dict:
                search_dict[token[0].text] = 1


print(json.dumps(search_dict, indent=2))



print('end script')

