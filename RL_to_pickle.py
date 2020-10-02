
from RL_Bible import Red_Letter_Bible
import pickle

print('start Sandbox')

app = Red_Letter_Bible()

redline_file = './Bible_texts/RedLetter_text.csv'

with open(redline_file, 'r') as file:
    file_lines = file.readlines()

RL_list = []
for count, line in enumerate(file_lines):
    if count%100 == 0:
        print(2000 - count)

    line_list = line.split(',')
    
    # passage is all parts of list after book and reference
    separator = ','
    passage = separator.join(line_list[2:])

    pos_list = []

    #### Entities
    entities = app.NLP.get_entities(line)
    entities_list = []

    for entity in entities:
        pos_list.append((entity[0].text, entity[1]))
        entities_list.append(entity[0].text)

    # create part of speech
    tokenized = app.NLP.return_sentence_list(passage, tokenize=True)
    for token_list in tokenized:
        for token in token_list:
            if token[0].text not in entities_list:
                if token[2] not in ['PUNCT', 'SPACE', 'PRON', 'AUX', 'DET', 'CCONJ']:
                    word_parts = (token[0].text.lower(), token[2])
                    pos_list.append(word_parts)

    # add to list
    # book, reference, passage (removes leading quotes and ending line break), pos
    RL_list.append((line_list[0], line_list[1], passage[1:-4], pos_list))

with open('RedLetter_text.pkl', 'wb') as file:
    pickle.dump(RL_list, file)

print('pickled')

with open('RedLetter_text.pkl', 'rb') as file:
    retrieved = pickle.load(file)

for count, this_line_list in enumerate(retrieved):
    print(this_line_list)
    if count == 5:
        break

print('end script')

