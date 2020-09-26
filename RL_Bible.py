# Red Letter Bible
''' Search Bible by topic
Preference to things Jesus said
Categorize remainder by OT, Paul letters, disciple letters
'''

# Rev 0.0.1 - Dev

import pandas as pd
import json
from language_utils import Nat_Lang_Proc
from language_utils import Text_Utilities


class Red_Letter_Bible():
    def __init__(self, spaCy_core='small'):
        self.NLP = Nat_Lang_Proc(spaCy_core)
        self.text_util = Text_Utilities()

        # get red letter DF
        redline_file = './Bible_texts/RedLetter_text.csv'
        redline_grouped_file = './Bible_texts/RL_grouped_text.csv'
        self.RedLetterDF = self.get_RedLetters(redline_file)
        self.RedLetterDF_grouped = self.get_RedLetters_grouped(redline_grouped_file)

        self.score_dict = {
            'full phrase': 20,
            'entity_PERSON': 5,
            'entity_GPE': 3,
            'PROPN': 2,
            'NOUN': 1,
            'VERB': 1,
        }

    def reference_parser(self, reference):
        '''returns chapter and verse from reference
        of form -   chapter:verse
        '''
        reference = reference.split(':')
        return int(reference[0]), int(reference[1])

    def get_RedLetters(self, redline_file):
        '''create DF of Red Letter verses with reference
        Made for specific file
        '''
        redlineDF = pd.read_csv(redline_file, header=None, error_bad_lines=False)

        # drop column 3 as is non-used from header

        ### this required when using the Red_Letter_text file
        redlineDF = redlineDF.iloc[:, :-1]

        redlineDF.columns = ['book', 'reference', 'verse']

        pd.set_option('display.expand_frame_repr', False)
        
        return redlineDF

    def get_RedLetters_grouped(self, redline_file):
        '''create DF of Red Letter verses with reference
        Specifically for grouped file
        '''
        redline_groupDF = pd.DataFrame(columns=['book', 'reference', 'verse'])
        with open(redline_file, 'r') as file:
            lines = file.readlines()

        for line in lines:
            line_list = line.split(',')
            separator = ','
            passage = separator.join(line_list[2:])
            #print(line_list[0], ':', line_list[1], '   ', passage)
            redline_groupDF = redline_groupDF.append({'book' : line_list[0] , 'reference' : line_list[1], 'verse': passage} , ignore_index=True)

        return redline_groupDF

    def advanced_word_search(self, phrase, word_dict, result='', max_results=10):
        '''Ranks search results based on words in word list
        Each word must have a ranking integer
        '''
        if result == 'grouped':
            searchDF = self.RedLetterDF_grouped
        else:
            searchDF = self.RedLetterDF

        results_list = []
        exact_match_list = []

        for index, row in searchDF.iterrows():
            this_score = 0

            # test for exact match
            find_phrase = self.text_util.find_word(row[2], phrase)
            if find_phrase is not None:
                ### found full phrase (returns score)
                # convert pandas series to list
                _verse = row.tolist()
                #add to exact match list
                exact_match_list.append(_verse)
            else:
                #### Word Search
                for word, word_score in word_dict.items():
                    word_return = self.text_util.find_word(row[2], word)
                    if word_return is not None:
                        this_score = this_score + word_score

                # place in list if greater than at least one
                if len(results_list) < max_results:
                    # add to results list
                    results_list = self.verse_to_list(row, this_score, results_list) 
                else:
                    scores_list = [i[3] for i in results_list]
                    lowest_score = min(scores_list)
                    if this_score > lowest_score:
                        # remove the lowest score
                        for result in results_list:
                            if result[3] == lowest_score:
                                results_list.remove(result)
                                break
                        #add to results list
                        results_list = self.verse_to_list(row, this_score, results_list)
                        
        results_list = self.organize_by_score(results_list)

        return exact_match_list, results_list

    def verse_to_list(self, row, this_score, results_list):
        '''support method for advanced word search
        Converts DF row (pandas series) to list
        Adds score as 4th element (position 3)
        '''
        # convert pandas series to list
        _verse = row.tolist()
        # add score to the list in position 3
        _verse.append(this_score)
        # append to results list
        if _verse[3] > 0:
            results_list.append(_verse)

        return results_list

    def organize_by_score(self, results_list):
        '''organize list in descending order
        '''
        start_flag = True
        sorted_list = []

        for item in results_list:
            insert_index = 0
            if start_flag == True:
                # add first item to sorted_list
                sorted_list.append(item)
                start_flag = False
            else:
                # find sorted_item that is greater than
                for count, sorted_item in enumerate(sorted_list):
                    if item[3] >= sorted_item[3]:
                        insert_index = count
                        break
                sorted_list.insert(insert_index, item)

        return sorted_list


    def create_scored_dict(self, phrase):
        '''create a list of words for searching
        '''
        # dictionary with word and ranking score
        search_dict = {}

        entities = self.NLP.get_entities(phrase)
        for entity in entities:
            if entity[1] == 'PERSON':
                if entity[0].text not in search_dict:
                    search_dict[entity[0].text] = self.score_dict['entity_PERSON']
            elif entity[1] == 'GPE':
                if entity[0].text not in search_dict:
                    search_dict[entity[0].text] = self.score_dict['entity_GPE']

        tokenized = self.NLP.return_sentence_list(phrase, tokenize=True)
        for token_list in tokenized:
            for token in token_list:
                print(token[0], ' - ', token[2])
                if token[2] == 'PROPN':
                    if token[0].text not in search_dict:
                        search_dict[token[0].text] = self.score_dict['PROPN']
                elif token[2] == 'NOUN':
                    if token[0].text not in search_dict:
                        search_dict[token[0].text] = self.score_dict['NOUN']
                elif token[2] == 'VERB':
                    if token[0].text not in search_dict:
                        search_dict[token[0].text] = self.score_dict['VERB']
                        # add lemma for verb
                        word_lemma = self.NLP.get_lemma(token[0].text)
                        search_dict[word_lemma] = self.score_dict['VERB']


        print(json.dumps(search_dict, indent=2))

        return search_dict



    
    def word_search(self, word, word2=None, search='and', result=''):
        print('\nSTART RESULTS:')
        if result == 'grouped':
            searchDF = self.RedLetterDF_grouped
        else:
            searchDF = self.RedLetterDF

        verse_count = 0
        if word2 == None:
            for index, row in searchDF.iterrows():
                word_return = self.text_util.find_word(row[2], word)
                if word_return is not None:
                    print(f'{row[2]} ({row[0]} {row[1]})')
                    print('\n')
                    verse_count +=1
            print(f'found {verse_count} verses with {word}')
        else:
            if search == '':
                for index, row in searchDF.iterrows():
                    word_return = self.text_util.find_word(row[2], word)
                    if word_return is not None:
                        word2_return = self.text_util.find_word(row[2], word2)
                        if word2_return is not None:
                            print(f'{row[2]} ({row[0]} {row[1]})')
                            print('\n')
                            verse_count +=1
                print('\nSummary of Red Letter verses:')
                print(f"Found {verse_count} passage with '{word}' and '{word2}'")
            elif search == 'one':
                pass
            else:
                pass            
                

if __name__ == '__main__':
    print('start Red Letter app')
    RLapp = Red_Letter_Bible('small')

    while True:
        result_type = input('grouped for passage or return for single verse: ')
        phrase = input("input phrase (or exit): ")
        if phrase == 'exit' or phrase =='Exit':
            break

        # create scored word list
        scored_dict = RLapp.create_scored_dict(phrase)

        #### advanced search
        exact_match_list, results_list = RLapp.advanced_word_search(phrase, scored_dict, result_type)

        #### if insufficient results, check similarities


        #### print results to console
        print('\nresults for: ', phrase)
        if len(exact_match_list) == 0:
            print('No exact matches')
        elif len(exact_match_list) >= 20:
            print(len(exact_match_list), ' exact matches')
            print('narrow search for results')
        else:
            print(len(exact_match_list), ' exact matches')
            print('EXACT MATCHES:')
            for result in exact_match_list:
                print(f'{result[2]} ({result[0]} {result[1]})')
                print('\n')

        if len(results_list) == 0:
            print('\nno results')
        else:
            print('\nResults:')
            for result in results_list:
                print(f'score: {result[3]}: {result[2]} ({result[0]} {result[1]})')
                print('\n')

    print('complete')

