# Word Checker

# rev 0 - DEV
# rev 0.0.1 - reconfigure classes, filled out methods
# rev 0.0.2 - add get_lemma using spaCy


import re
import spacy
from spacy.lang.en import English
from spacy_wordnet.wordnet_annotator import WordnetAnnotator


class Nat_Lang_Proc:
    def __init__(self, spaCy_core='small'):
        # load spaCy English model
        if spaCy_core == 'large':
            # includes vectors & entities
            self.nlp = spacy.load('en_core_web_lg')
            self.model_flag = 'large'
        else:
            # includes entities
            self.nlp = spacy.load('en_core_web_sm')
            self.model_flag = 'small'

        ### set up wordnet
        self.nlp.add_pipe(WordnetAnnotator(self.nlp.lang), after='tagger')
        self.token = self.nlp('prices')[0]

        # wordnet object link spacy token with nltk wordnet interface by giving acces to
        self.token._.wordnet.synsets()
        self.token._.wordnet.lemmas()

        # And automatically tag with wordnet domains
        self.token._.wordnet.wordnet_domains()

    def return_sentence_list(self, text, tokenize=False):
        '''returns list of sentences
        Sentences are spacy span objects (spacy.tokens.span.Span)
        To use the individual tokens in the span:
        [(token, token.lemma_) for token in sentences[0]]

        tokenize=True returns a list of lists
        One list per sentence
        Each sentence list contians a list of attributes for each
        token in that sentence (token, lemma, part of speech)
        '''
        sentences = [i for i in self.nlp(text).sents]

        if tokenize == False:
            # return just sentences as span objects
            return sentences
        else:
            tokenized_list = []
            for sentence in sentences:
                tokenized_list.append([(token, token.lemma_, token.pos_) for token in sentence])
            return tokenized_list


    def convert_sentence_list(self, line_list):
        '''Converts all sentences to nlp objects
        Return is list of nlp sentences
        '''
        return_list = []
        for line in line_list:
            return_list.append(self.nlp(line))

        return return_list

    ### word similarities
    def get_similar_list(self, word, max_matches=5):
        '''returns list of similar words up to max match
        '''
        lemma_set = self.find_synset_strings(word)

        # initialize dictionary with test word
        lemma_dict = {word: 1.0}

        for lemma in lemma_set:
            similarity_score = self.word_similarity(word, lemma)
            if lemma != word:
                if len(lemma_dict) <= max_matches and similarity_score > .1:
                    lemma_dict[lemma] = similarity_score
                else:
                    # find smallest similarity within full dict
                    smallest_lemma = ''
                    smallest_value = 1
                    for key in lemma_dict:
                        if lemma_dict[key] < smallest_value:
                            smallest_value = lemma_dict[key]
                            smallest_lemma = key

                    # remove smallest and replace if applicable
                    if similarity_score > smallest_value:
                        lemma_dict.pop(smallest_lemma)
                        lemma_dict[lemma] = similarity_score

        lemma_list = list(lemma_dict.keys())

        return lemma_list

    def word_similarity(self, word1, word2):
        '''returns vector similarities of two words
        Requires large model
        '''
        if self.model_flag != 'large':
            print('need to load large model')
            return

        token1 = self.nlp(word1)
        token2 = self.nlp(word2)

        # do not compare if no vector for both words
        if token1.vector_norm > 0 and token2.vector_norm > 0:
            similarity_score = float(token1.similarity(token2))
        else:
            similarity_score = 0
        
        return similarity_score


    ### synsets and lemmas using wordnet
    def find_synset(self, word):
        token = self.nlp(word)[0]
        synset = token._.wordnet.synsets()
        return synset

    def get_lemma(self, word):
        '''Use spaCy to get lemma for a word
        '''
        token = self.nlp(word)[0]
        return token.lemma_


    def find_lemmas(self, word):
        '''Use Wordnet to get lemmas for word
        '''
        token = self.nlp(word)[0]
        lemmas = token._.wordnet.lemmas()
        return lemmas

    def get_domains(self, word):
        token = self.nlp(word)[0]
        domains = token._.wordnet.wordnet_domains()
        return domains

    def find_synset_strings(self, word, domains=[]):
        # create nlp token for word
        token = self.nlp(word)[0]

        # find synset based on domains designated
        if domains == []:
            synset = token._.wordnet.synsets()
        else:
            synset = token._.wordnet.wordnet_synsets_for_domain(domains)

        # find lemmas
        lemmas = token._.wordnet.lemmas()

        # organize set of lemmas without duplicates
        lemmas_for_synset = {lemma for s in synset for lemma in s.lemma_names()}

        return lemmas_for_synset

    ### Entities

    def get_entities(self, sentence):
        '''Returns list of entities for a sentence
        Sentence can be one or more words
        '''
        sentence_tokens = self.nlp(sentence)
        entities=[(i, i.label_, i.label) for i in sentence_tokens.ents]

        return entities



class Text_Utilities:
    def make_lower_case(self, text):
        '''Make all text lower case
        '''
        return text.lower()

    def find_word(self, text, word):
        '''Return text if it contains word or phrase
        Word is not case sensitive
        Word can be multiple words (phrase)
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
    print('start language_utils script ')



