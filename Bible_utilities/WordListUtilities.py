'''utilities for working with wordlist files and 
dictionaries saved as wordlist
'''


def checkWords(wordListFileName):
    '''runs loop to check user entered words if in
    the dictionary list file

    'exit' to quite
    '''
    with open(wordListFileName) as file:
        wordList = file.read().split()

    run = True
    while run is True:
        checkWord = input('word: ')
        if checkWord in wordList:
            print(checkWord, ' is in list')
        else:
            print('NOT in list')

        if checkWord == 'exit':
            run = False


def HitchcockToList(fileName):
    '''converts .txt version of Hitchcock Names in Bible
    to python list
    Returns a list of names
    '''
    with open(fileName) as file:
        text = file.readlines()

    nameList = []

    for count, line in enumerate(text):
        if count > 10:
            if line.isspace() is False:
                words = line.split()
                if 20 > len(words[0]) > 1:
                    if words[0].isdigit() is False:
                        nameList.append(words[0][:-1])   

    return nameList

