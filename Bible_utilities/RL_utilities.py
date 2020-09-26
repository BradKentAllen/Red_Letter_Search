import pandas as pd
import json

import RL_Bible as RL

def group_RL_verses():
	'''Groups individual verses into passages
	Uses csv created below in convert_RL_to_csv
	'''
	red = RL.Red_Letter_Bible()
	RedDF = red.RedLetterDF
	#print(RedDF.head())

	start = True
	previous_book = 'Matthew'
	previous_chapter = 1
	previous_verse = 100
	previous_passage = ''
	single_verse = True

	passageDF = pd.DataFrame(columns=['book', 'reference', 'verse'])

	with open('grouped.csv', 'w') as write_file:
		for index, row in RedDF.iterrows():
			chapter, verse = red.reference_parser(row[1])
			book = row[0]
			passage = row[2]

			# print this row
			#print(book, ' ', chapter, ':', verse, ' - ', passage)

			if verse == previous_verse + 1:
				# successive verses (don't print)
				passage = passage + previous_passage
				if single_verse == True:
					# first combining of a multi-verse
					start_verse = previous_verse
					single_verse = False
				else:
					# successive multi-verse
					single_verse = False

				previous_book = book
				previous_chapter = chapter
				previous_verse = verse
				previous_passage = passage

			else:
				if start == True:
					start = False
				else:
					# time to print (remember, we are printing the previous passage)
					previous_passage = fix_quote(previous_passage)

					if single_verse == False:
						# print a multi-verse passage
						print(previous_book, ' ', previous_chapter, ':', start_verse, '-', previous_verse, ' ', previous_passage)
						write_file.write(previous_book + ',' + str(previous_chapter) + ':' + str(start_verse) + '-' + str(previous_verse) + ',' + previous_passage)
						write_file.write('\n')
					else:
						# print a single verse
						print(previous_book, ' ', previous_chapter, ':', previous_verse, ' ', previous_passage)
						write_file.write(previous_book + ',' + str(previous_chapter) + ':' + str(previous_verse) + ',' + previous_passage)
						write_file.write('\n')

				single_verse = True
				previous_book = book
				previous_chapter = chapter
				previous_verse = verse
				previous_passage = row[2]



def fix_quote(passage_in):
	passage = ''
	for count, letter in enumerate(passage_in):
		if count == 0:
			print(letter)
		if count == 0 and letter == '\'':
			# delete leading single quote
			pass
		elif count == 0 and letter == '”':
			# delete leading double quote
			print('HERE1')
			pass
		elif count == 0 and letter == '"':
			print('HERE2')
			# delete leading double quote
			pass
		elif letter == '\'' or letter == '”' or letter == '"':
			passage = passage + '\\' + letter
		else:
			passage = passage + letter

	if letter == '”' or letter == '"':
		print('delete trailing quote')
		# delete trailing quote
		passage = passage[:-1]

	#passage = '"' + passage + '"'
	passage = passage.replace('\'', '"')
	passage = passage.replace('\\', '')


	return passage

def convert_RL_to_csv():
	'''convert Red Letter document
	special purpose for converting red letter list to csv
	- reads by line
	- aligns reference with verse
	- replaces double quotes with single so verse stays in one cell
	'''

	with open('result.csv', 'w') as write_file:
		with open('RedLetter_verses.txt', 'r') as read_file:
			line = 'a'
			ready_flag = False
			while line:
				# read the first line
				line = line.split(' ')
				if '\n' in line:
					# remove separate line breaks
					line.remove('\n')

				# find the verse references
				if len(line) == 2:
					# remove line break from references
					line[1] = line[1].replace('\n', '')
					verse_reference = line
					ready_flag = True
				else:
					verse_list = line
					verse_text = (' ').join(verse_list)
					# replace " with ' for csv
					verse_text.replace('\"', '\'')
					verse_text = "\"" + verse_text + "\""
					if ready_flag == True:
						verse_reference.append(verse_text)
						for item in verse_reference:
							write_file.write(item + ',')
						write_file.write('\n')
						ready_flag = False
				line = read_file.readline()


def read_RL_to_DF():
	redline_file = './Bible_texts/RedLine_text.csv'

	with open(redline_file, 'r') as file:
		line = file.readline()
		print(line)
		print(type(line))

	redlineDF = pd.read_csv(redline_file, header=None, error_bad_lines=False)

	# drop column 3 as is non-used from header
	redlineDF = redlineDF.iloc[:, :-1]

	redlineDF.columns = ['book', 'reference', 'verse']

	pd.set_option('display.expand_frame_repr', False)
	print(redlineDF.head())

	print('complete')


if __name__ == '__main__':
	group_RL_verses()

	print('RL_utilities complete')


