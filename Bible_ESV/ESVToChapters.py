''' converts .txt file of ESV to dictionary of this form:
BibleIndexed = {Book : {Chapter : chapter text}}

This uses text ESV converted from epub.

This is a good test:  returnedDict['JOHN'][3]]
'''


def convert(BibleFile):
    '''convert Bible to a dictionary of this format:
    {Book : {Chapter : chapter text}}
    Returns dictionary
    '''
    OTbooks = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges',
            'Ruth', '1 Samuel', '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles',
            'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalm', 'Proverbs', 'Ecclesiastes', 'Song of Solomon',
            'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos',
            'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi']

    NTbooks = ['Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians',
        'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians',
        '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter',
        '1 John', '2 John', '3 John', 'Jude', 'Revelation']

    # combine OT and NT chapters list
    BibleBooks = OTbooks + NTbooks + ['end',]

    thisBookNumber = 0

    # initialize books
    currentBook = BibleBooks[thisBookNumber].upper()
    nextBook = BibleBooks[thisBookNumber + 1].upper()

    BibleIndexed = {currentBook : {}}
    currentChapter = 0
    thisChapterString = ''

    # read Bible text
    with open(BibleFile) as file:
        # iterate through lines in file
        for line in file:
            # create list of words in the line
            wordList = line.split(' ')

            # identify Book change
            try:
                if wordList[1] == nextBook[2:]:
                    checkWord = wordList[0] + ' ' + wordList[1]
                elif wordList[0] == 'SONG':
                    checkWord = wordList[0] + ' ' + wordList[1] + ' ' + wordList[2]
                else:
                    checkWord = wordList[0]
            except IndexError:
                checkWord = wordList[0]

            if checkWord == nextBook:
                thisBookNumber += 1
                currentChapter = 0
                currentBook = BibleBooks[thisBookNumber].upper()
                if currentBook == 'END':
                    break
                nextBook = BibleBooks[thisBookNumber + 1].upper()
                BibleIndexed[currentBook] = {}
                print('reading BOOK: ', currentBook)
                print('nextBook: ', nextBook)

            # identify CHAPTER change
            if wordList[0] == currentBook:
                lastChapter = currentChapter
                currentChapter += 1
                if currentChapter != 1:
                    print('chapter ', lastChapter)
                    BibleIndexed[currentBook][lastChapter] = thisChapterString
                    thisChapterString = ''


            # work with lines that are not blank
            if line.strip():
                # .isdigit() recognizes positive integers wordList[0] catches first
                # verse group in each chapter
                if line[0].isdigit() or wordList[0] == currentBook:
                    thisChapterString = thisChapterString + line

    return BibleIndexed



