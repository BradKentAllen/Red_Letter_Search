# Word Checker

# rev 0 - DEV
# rev 0.0.1 - reconfigure classes


import re
import spacy
from spacy.lang.en import English


class Nat_Lang_Proc:
    def __init__(self, spaCy_core='small'):
        # spacy english model (large)
        # self.nlp = English()
        if spaCy_core == 'large':
            self.nlp = spacy.load('en_core_web_lg')
        else:
            self.nlp = spacy.load('en_core_web_sm')

    def return_sentence_list(self, text):
        '''returns list of sentences
        '''
        sentences = [i for i in self.nlp(text).sents]

        return sentences

    def convert_sentence_list(self, line_list):
        '''converts all sentences to nlp objects
        '''
        return_list = []
        for line in line_list:
            return_list.append(self.nlp(line))

        return return_list



class Text_Utilities:
    def make_lower_case(self, text):
        '''Make all text lower case
        '''
        return text.lower()

    def find_word(self, text, word):
        '''Return text if it contains word
        Word is not case sensitive
        Word can be multiple words
        '''
        _word = self.make_lower_case(word)
        _text = self.make_lower_case(text)
        if re.search(_word, _text):
            return text
        else:
            return

    def remove_string(self, text, remove_string):
        '''Remove a string from a text
        '''
        text = re.sub(remove_string, '', text)
      
        return text

    def remove_digits(self, text):
        '''removes digits 1-9 from text
        '''
        text = re.sub(r'[0-9]', '', text)

        return text


        #### DEV ####
    def remove_footnotes(self, text):
        '''removes footnotes b to z
        Asks for removal of a (as is indistinguishable from a)
        '''
        #remove footnote numbers except a
        text = re.sub(r'\s[b-z]\s', ' ', text)

        # XXXX - need to make check_a work first
        #self.check_a(text)

        return text

    def check_a(self, text):
        '''XXXX currently does not work
        Iterates through sentences.
        Asks about 'a'
        Removes a
        '''
        sentence_list = text.split('.')
        for sentence in sentence_list:
            if ' a ' in sentence:
                print(sentence)

    def remove_punctuation(self, text):
        ''' remove all punctuation
        '''
        text = re.sub(r'[^\w\s]','',text)

        return text

    


if __name__ == '__main__':
    NLP = nat_lang_proc()
    text_util = text_utilities()
    text = "In the a beginning, God created the heavens and the earth! 2The earth was b without form and void, and darkness was over the face of the deep."

    text = text_util.remove_digits(text)
    text = text_util.remove_footnotes(text)


    sentence_list = NLP.return_sentence_list(text)

    search_word = 'the earTH'

    for count, sentence in enumerate(sentence_list):
        print('test ', count, ': ', end='')

        returned_text = text_util.find_word(str(sentence), search_word)
        if returned_text != None:
            print(returned_text)
        else:
            print('not a match')
  
    print('script complete')



