'''utilities for working with lists and dictionaries
in the form of lists
'''


def cleanDuplicates(listIn):
    '''returns new list without duplicates
    Return: Python list
    '''
    print('Eliminating Duplicates')
    print('start length: ', len(listIn))
    newList = []
    for word in listIn:
        if word not in newList:
            newList.append(word)

    if len(newList) == len(set(newList)):
        print('all duplicates eliminated')
    else:
        print('oops, still duplicates')

    print('end length: ', len(newList))
    return newList


def writeListToFile(fileName, listIn):
    '''writes list input to file
    .txt is typical fileName
    No return
    '''
    with open(fileName, 'w') as file:
        for item in listIn:
            file.write(item + '\n')


def findListFileLength(fileName):
    '''returns length of a list that has been saved as a file
    Essentially counts number of lines
    Returns integer
    '''
    with open(fileName) as file:
        wordList = file.read().split()
    print('length of ', fileName, ' is ', '{:,}'.format(len(wordList)), ' words')

    return len(wordList)


def removeWordsFromDictionary(dictFileName, wordsFileName, newDictionaryName):
    '''removes words in wordsFileName from dictFileName
    and returns a new dictionary list in the form of a list of words
    Note: 'dictionary' refers to an English dictionary, not a python one
    Saves new list as newDictionaryName.txt
    Return: Python list
    '''

    with open(dictFileName) as file:
        dictionaryList = file.read().split()

    with open(wordsFileName) as file:
        nameList = file.read().split()

    for name in nameList:
        if name.lower() in dictionaryList:
            dictionaryList.remove(name.lower())

    writeListToFile(newDictionaryName, dictionaryList)

    return dictionaryList












