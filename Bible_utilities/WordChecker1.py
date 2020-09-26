# Word Checker

# rev 0 - DEV
import re


class Main:
    def __init__(self):
        '''start
        '''
        # create list of English words
        dictionaryFile = 'RefLists/DictLessNames.txt'
        with open(dictionaryFile) as file:
            self.EnglishWordList = file.read().split()  

    def wordListCreator(self, text):
        ''' convert to wordList and clean
        '''

        # convert text file to lower case word list       
        wordList = text.lower().split()

        for index, word in enumerate(wordList):
            # remove punctuation
            word = re.sub(r'[^\w\s]','',word)
            wordList[index] = word

            # remove white space
            if word.isspace():
                wordList.remove(word)

        return wordList

    def findNonDictWords(self, wordList):
        '''method
        '''
        # create list of words not in the dictionary
        nonDictList = []
        for word in wordList:
            # append list if not in dictionary
            if word not in self.EnglishWordList:
                nonDictList.append(word)

        # remove words that have 1 or 2 letters different at end (s, 's, ed)

        return nonDictList
        

    def textFileCleaner(self, fileName):
        '''cleans the following from text file:
        - digits
        - [] which was [digit] prior to remove digits
        - lone letters (footnotes) except 'a'
        XXXX - Problem: this removes all numbers including those
        being used in the text
        '''

        with open(fileName) as file:
            text = file.read()

        #remove digits leading a letter
        text = re.sub(r'[0-9]', '', text)

        #remove [] (this must be after remove digits)
        text = re.sub(r'[[]]', '', text)

        #remove footnote numbers except a
        text = re.sub(r'\s[b-z]\s', ' ', text)
        
        return text


if __name__ == '__main__':
    app = Main()
    text = app.textFileCleaner('ESVJohn3.txt')
    wordList = app.wordListCreator(text)
    nonDictList = app.findNonDictWords(wordList)

    print(text)
  
    print(nonDictList)
    print('')

    print('text file has:', len(wordList), 'words')
    print('nonDictWords has ', len(nonDictList), 'words')




